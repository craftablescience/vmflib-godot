"""

Utility for importing all of the information in a FGD file into a format that this package understands.

It is assumed that the input FGD uses the typical convention of newline placement: Blank lines are okay, but anything
squished onto one line or broken into two lines is not.

Author: Eli Zupke

Further reading: https://developer.valvesoftware.com/wiki/FGD

"""
import re
#import vmflib2
import datetime
import os.path

DOCSTRING = "\"\"\"{0}\"\"\""
START_DOCSTRING_TEXT = "\nHelper classes for creating maps in any Source Engine game that uses {0}.\n" \
                       "This file was auto-generated by import_fgd.py on {1}.\n"

AUTOGENERATED_TODO_TEXT = "TODO: This class was automatically generated, and may need correction or expansion."

CLASS_TEXT = "class {0}({1}):"
INIT_TEXT = "def __init(self, {0}):"
#IMPORT_TEXT = "import {0}"


def to_camel_case(string: str):
    "Convert an underscore_string to a CamelCaseString."
    out = ""

    upper_next = True

    for c in string:
        if c == "_":
            upper_next = True
        else:
            if upper_next:
                out += c.upper()
            else:
                out += c.lower()
            upper_next = False
    return out

class propertyType:
    """Represents a type of property (such as string, integer, choices, etc.) that can be found in FGD files."""
    def __init__(self, base_type):
        # This is the type of object that this property type represents
        self.base_type = base_type

class propertyInstance:
    """Represents a single property in a single class"""
    def __init__(self, name: str, type: propertyType, short_description: str, default, long_description: str):
        self.name = name
        self.type = type
        self.short_description = short_description
        self.default = default
        self.long_description = long_description

    def represent(self):
        """Represent this property as a string in the output python file."""
        out = ""
        ind2 = "\n" + indent_level(2)
        out += "{0}# {1} : {2}{0}self.{3} = {4}".format(ind2, self.short_description, self.long_description, self.name,
                                                        self.default)

        return out


class propertyFiller(propertyInstance):
    """Prints a blank line in the property list"""
    def __init__(self):
        propertyInstance.__init__(self, "", None, "", "", "")

    def represent(self):
        return "\n"


class fgdClass:
    """Represents a single class found in the FGD file (usually an entity)"""
    def __init__(self, class_name: str, argument_string: str, line_number: int, fgd_name: str, class_lookup:dict):

        # Whether this is a base class that can be safely ignored.
        self.is_base = (class_name == "BaseClass")
        self.is_solid = (class_name == "SolidClass")
        self.is_filter = (class_name == "FilterClass")
        self.properties = []

        self.ent_name = "name_not_found"

        m = re.match(r"([^=]*)= ([^\s:]*)(?: ?: ?\"([^\n]*)\")?", argument_string)
        if m is None:
            raise IOError("Can't match '{0}'\nFile: {1}, Line {2}".format(argument_string, fgd_name, line_number))

        args, self.ent_name, self.description = m.group(1, 2, 3)

        if self.ent_name == "worldspawn":
            # Kind of a hack, as we don't want this one entity to be auto-generated.
            self.is_base = True

        if not self.description:
            self.description = ""

        # Note: The only thing we need to know in the args section is the 'base' property.
        base_match = re.search("base\(([^()]*)\)", args)
        if base_match:
            parents = base_match.group(1).split(",")
            for parent in [class_lookup[p.strip().lower()] for p in parents]:
                self.properties.extend(parent.properties)
                self.properties.append(propertyFiller())

        self.name = to_camel_case(self.ent_name)
        self.parent = "Entity"

        self.fgd_loc = "{0}, line {1}".format(fgd_name, line_number)

    def add_property(self, prop: propertyInstance):

        self.properties.append(prop)

    def represent(self):
        """Represent this class as a string in the output python file."""
        ind1 = "\n" + indent_level(1)
        ind2 = "\n" + indent_level(2)
        ind3 = "\n" + indent_level(3)

        docstring = "{1}Auto-generated from {0}.{1}{2}{1}".format(self.fgd_loc, ind1, self.description)

        out = CLASS_TEXT.format(self.name, self.parent)
        out += ind1
        out += DOCSTRING.format(docstring)

        out += ind1
        out += "def __init__(self, vmf_map):"

        out += "{0}{1}.__init__(self, \"{2}\", vmf_map)".format(ind2, self.parent, self.ent_name)

        out += "\n"
        for p in self.properties:
            p: propertyInstance
            out += p.represent()

        if len(self.properties) > 0:
            out += "\n{0}self.auto_properties.extend([".format(ind2)
            for p in self.properties:
                p: propertyInstance
                if type(p) == type(propertyFiller()):
                    continue
                out += "\"{0}\", ".format(p.name)
            out = out[:-2]
            out += "])\n"


        # TODO: ensure nothing else needs to be added here

        return out



string_type = propertyType(str)
integer_type = propertyType(int)
float_type = propertyType(float)

color255_type = None #propertyType(vmflib2.types.RGB)
origin_type = None #propertyType(vmflib2.types.Origin)

# Which property type to use for each type listed in the file.
property_types = {
    "choices": None,
    "flags": None,
    "axis": None,
    "angle": None,
    "angle_negative_pitch": None,
    "color255": color255_type,
    "color1": None,
    "origin": origin_type,
    "sidelist": None,
    "vecline": None,
    "vector": origin_type,
    "integer": integer_type,
    "node_dest": integer_type,
    "float": float_type,
    "string": string_type,
    "target_source": string_type,
    "sound": string_type,
    "sprite": string_type,
    "studio": string_type,
    "target_destination": string_type,
    "target_name_or_class": string_type,
    "scene": string_type,
    "npcclass": string_type,
    "filterclass": string_type,
    "material": string_type,
    "decal": string_type,
    "instance_file": string_type,
    "instance_variable": string_type,
    "instance_parm": string_type,
    "pointentityclass": string_type,

}

ignore_classes = ["MaterialExclusion", "AutoVisGroup", "mapsize"]
entity_classes = ["BaseClass", "PointClass", "NPCClass", "SolidClass", "KeyFrameClass", "MoveClass", "FilterClass"]

def fgd_name_to_py_name(fgd_path:str):
    """Converts the name of a given FGD file or FGD file path to the name of its corresponding vmflib2 game file."""

    # Ignore file directories
    fgd_name = os.path.split(fgd_path)[1]
    m = re.match(r"([^/\\]*)\.[fF][gG][dD]", fgd_name)

    if m and m.group(1):
        return "{0}.py".format(m.group(1))
    else:
        raise ValueError("FGD path/name {0} does not look like a valid FGD path/name!".format(fgd_name))

def indent_level(level:int):
    """Returns a string containing indentation to the given level, in spaces"""
    return "    " * level

def create_python_file(output_path:str, fgd_name:str, imports:list, classes:list):

    classes.sort(key=lambda x : x.ent_name)

    with open(output_path, "w") as output_file:

        date = str(datetime.datetime.now())

        # Write the starting docstring
        output_file.write(DOCSTRING.format(START_DOCSTRING_TEXT.format(fgd_name, date)))
        output_file.write("\n\n")

        # Write the import statements
        for i in imports:
            output_file.write(i)
            output_file.write("\n")
        output_file.write("\n\n")

        for c in classes:
            c: fgdClass
            output_file.write(c.represent())
            output_file.write("\n\n")



def import_fgd(fgd_path:str):

    output_name = fgd_name_to_py_name(fgd_path)

    output_path = os.path.join("vmflib2", "games", "{0}".format(output_name))

    # A list of all of the files our output file will need to import
    imports = ["from vmflib2.vmf import *"]


    # Just so that we can find other classes, here's all the classes, keyed by their names (what appears in the FGD file)
    class_lookup = dict()

    classes = read_fgd(fgd_path, class_lookup)

    fgd_name = os.path.split(fgd_path)[1]

    create_python_file(output_path, fgd_name, imports, classes)


def read_fgd(fgd_path, class_lookup):

    # A list of all of the classes that we need to add to the file
    classes = []

    loc_prefix = os.path.split(fgd_path)[0]

    with open(fgd_path, "r") as input_file:

        # How many open brackets we've seen minus how many close brackets we've seen
        bracket_level = 0

        # Whether we're currently ignoring the class that we're reading
        ignoring_class = False

        current_class = None

        fgd_name = os.path.split(fgd_path)[1]

        for line_number, line in enumerate(input_file, start=1):

            clean_line = line.strip()
            # Remove comments
            if clean_line.find("//") > -1:
                clean_line = clean_line[:clean_line.find("//")]

            string_match = re.match("\"([^\"]*)\"+?", clean_line)
            property_match = re.match("([^()]*)\(([^()]*)\)( *: *[^\n]*)?", clean_line)
            input_match = re.match("input *([^()]*)\(([^()]*)\)( *: *[^\n]*)?", clean_line)
            output_match = re.match("output *([^()]*)\(([^()]*)\)( *: *[^\n]*)?", clean_line)

            if clean_line.find("@") == 0:
                # We've hit a new class definition
                if bracket_level > 0:
                    raise IOError("FGD file has a class definition inside another other class definition! "
                                  "\nLine: {0}, '{1}'".format(line_number, line))
                class_name, argument_string = re.match("@([\S]*)(?: ([^\n]*))?", clean_line).group(1, 2)
                argument_string: str

                ignoring_class = class_name in ignore_classes
                if class_name == "include":
                    new_path = os.path.join(loc_prefix, argument_string.replace("\"", ""))
                    read_fgd(new_path, class_lookup)
                else:
                    if not class_name in entity_classes:
                        print("Warning: class name {0} not in list of entity class names. tentatively ignoring "
                              "line {1}.".format(class_name, line_number))
                        ignoring_class = True
                    if not ignoring_class:
                        current_class = fgdClass(class_name, argument_string, line_number, fgd_name, class_lookup)
                        # Add current_class to the class list if not a base class
                        if not current_class.is_base:
                            classes.append(current_class)
                        # And to the lookup
                        class_lookup[current_class.ent_name.lower()] = current_class

            elif clean_line.find("[") == 0:
                # TODO: handle open brackets at end of line, like dod.fgd
                bracket_level += 1
            elif clean_line.find("]") == 0:
                bracket_level -= 1
                if bracket_level < 0:
                    raise IOError("FGD file has an errant close bracket! "
                                  "\nFile: {2}, Line: {0}, '{1}'".format(line_number, line, fgd_name))
                elif bracket_level == 0:
                    current_class = None
            elif string_match and current_class and bracket_level == 0:
                # We've got part of the description!
                current_class.description += string_match.group(1)
            else:
                if current_class and bracket_level == 1 and not ignoring_class:
                    if string_match:
                        # TODO add onto last description
                        pass
                    elif input_match:
                        # TODO add inputs
                        pass
                    elif output_match:
                        # TODO add output
                        pass
                    elif property_match:
                        prop_name = property_match.group(1)
                        prop_type = property_types[property_match.group(2).lower().strip()]
                        args = property_match.group(3)
                        prop_short_desc = "TODO: Replace this filler."
                        prop_long_desc = "TODO: Replace this filler."
                        prop_default = "\"\""
                        if not args:
                            # print(clean_line)
                            pass
                        else:
                            property_args_match = re.match("\s*:\s*\"([^\"]*)\"(?:\s*:\s*([^:=]*))?(?:\s*:\s*\"([^\"]*)\")?", property_match.group(3))
                            if property_args_match.group(1):
                                prop_short_desc = property_args_match.group(1)
                            if property_args_match.group(2):
                                prop_default = property_args_match.group(2)
                            if property_args_match.group(3):
                                prop_long_desc = property_args_match.group(3)
                        prop = propertyInstance(prop_name, prop_type, prop_short_desc, prop_default, prop_long_desc)
                        current_class.add_property(prop)
    return classes


"""

Classes that offer abstractions for brushes, etc. that aren't modeled
in the VMF format itself.

"""

from vmflib2 import brush, types
import math


class Block():
    """A class representing a 3D block in terms of world geometry.

    This class allows for the simple creation and manipulation of 3D
    blocks (six-sided rectangular prisms) without having to manage
    the underlying brush (Solid) and its faces (Sides) manually.
    You can think of this as the programatic analog to the Block Tool
    in the Valve Hammer Editor.

    """

    def __init__(self,
                 origin=types.Vertex(),
                 dimensions=(64, 64, 64),
                 material='BRICK/BRICKFLOOR001A'):
        """Create a new Block at origin with dimensions and material."""
        self.origin = origin
        self.dimensions = dimensions

        # Create brush
        self.brush = brush.Solid()

        # Create (un-positioned) sides
        sides = []
        for i in range(6):
            sides.append(brush.Side(types.Plane(), material))
        self.brush.children.extend(sides)

        # Compute initial side planes
        self.update_sides()

        # Apply material
        self.set_material(material)

    def update_sides(self):
        """Call this when the origin or dimensions have changed."""
        x = self.origin.x
        y = self.origin.y
        z = self.origin.z
        w, l, h = self.dimensions
        a = w / 2
        b = l / 2
        c = h / 2

        self.brush.children[0].plane = types.Plane(
            types.Vertex(x - a, y + b, z + c),
            types.Vertex(x + a, y + b, z + c),
            types.Vertex(x + a, y - b, z + c))
        self.brush.children[1].plane = types.Plane(
            types.Vertex(x - a, y - b, z - c),
            types.Vertex(x + a, y - b, z - c),
            types.Vertex(x + a, y + b, z - c))
        self.brush.children[2].plane = types.Plane(
            types.Vertex(x - a, y + b, z + c),
            types.Vertex(x - a, y - b, z + c),
            types.Vertex(x - a, y - b, z - c))
        self.brush.children[3].plane = types.Plane(
            types.Vertex(x + a, y + b, z - c),
            types.Vertex(x + a, y - b, z - c),
            types.Vertex(x + a, y - b, z + c))
        self.brush.children[4].plane = types.Plane(
            types.Vertex(x + a, y + b, z + c),
            types.Vertex(x - a, y + b, z + c),
            types.Vertex(x - a, y + b, z - c))
        self.brush.children[5].plane = types.Plane(
            types.Vertex(x + a, y - b, z - c),
            types.Vertex(x - a, y - b, z - c),
            types.Vertex(x - a, y - b, z + c))

        for side in self.brush.children:
            side.uaxis, side.vaxis = side.plane.sensible_axes()

    def set_material(self, material):
        for side in self.brush.children:
            side.material = material

    def bottom(self):
        """Returns the bottom Side of the Block."""
        return self.brush.children[1]

    def top(self):
        """Returns the top Side of the Block."""
        return self.brush.children[0]

    def __repr__(self, tab_level=-1):
        return self.brush.__repr__(tab_level)


class DisplacementMap:
    """A class representing one upwards-facing mesh, possibly made of multiple displacements sewn together.

    """

    def __init__(self, source, source_alphas=None, origin=types.Vertex(), size=types.Vertex(), x_subdisplacements=4,
                 y_subdisplacements=4,
                 vertical_scale=1.0):

        self.source = source
        self.source_alphas = source_alphas
        self.origin = origin
        self.size = size
        self.sub_displacements = (x_subdisplacements, y_subdisplacements)
        self.vertical_scale = vertical_scale
        self.power = 4

        self.d_x_size = self.size[0] / self.sub_displacements[0]
        self.d_y_size = self.size[1] / self.sub_displacements[1]


        rotation_counts = {
            (True, True): 3,
            (True, False): 0,
            (False, False): 1,
            (False, True): 2
        }

        self.displacement_brushes = []

        for dx in range(x_subdisplacements):
            for dy in range(y_subdisplacements):

                power = 2 ** self.power

                x_offset = power * dx
                y_offset = power * dy

                # The actual position the displacement brush will be in
                x_pos = (dx - (x_subdisplacements / 2) + 0.5) * self.d_x_size + origin.x
                y_pos = (dy - (y_subdisplacements / 2) + 0.5) * self.d_y_size + origin.y


                # The modifications of which order we load the values into the array need to happen for some reason.
                # Source just wants things in a different order depending on which quadrant you're in I guess.

                forward_range = list(range(power + 1))
                backwards_range = list(range(power, -1, -1))

                x_range = forward_range
                y_range = backwards_range

                norms = []
                for i in x_range:
                    row = []
                    for j in y_range:
                        row.append(types.Vertex(0, 0, 1))
                    norms.append(row)
                dists = []
                for x in x_range:
                    row = []
                    for y in y_range:
                        rel_x = x + x_offset
                        rel_y = y + y_offset
                        row.append(source[rel_x, rel_y] * vertical_scale)
                    dists.append(row)
                if self.source_alphas:
                    alphas = []
                    for x in x_range:
                        alphas_row = []
                        for y in y_range:
                            rel_x = x + x_offset
                            rel_y = y + y_offset
                            alphas_row.append(source_alphas[rel_x, rel_y])
                        alphas.append(alphas_row)
                else:
                    alphas = None

                # There's a weird quirk where the displacement gets rotated depending on what quadrant it's origin is
                # in. I'm not sure whether this is something to do with the source engine, or the Block tool.
                # either way, the following StackOverflow-code accounts for it by rotating the displacement back.
                # (it's still wrong sometimes when the displacements' origin x or y are 0, so don't do that)
                rotation_count = rotation_counts[x_pos > 0, y_pos >= 0]
                for i in range(rotation_count):
                    dists = list(zip(*dists[::-1]))
                    norms = list(zip(*norms[::-1]))
                    if alphas:
                        alphas = list(zip(*alphas[::-1]))


                d = brush.DispInfo(self.power, norms, dists, alphas)

                floor = Block(types.Vertex(x_pos, y_pos, origin.z),
                              (self.d_x_size, self.d_y_size, size[2]))
                floor.top().children.append(d)  # Add disp map to the ground

                self.displacement_brushes.append(floor)

    def set_material(self, material: str):
        for b in self.displacement_brushes:
            b.set_material(material)

    def get_height(self, pos):
        """Returns the real z coordinates that the displacementmap takes on at the given x and y coordinates"""
        pos_x, pos_y = pos
        if pos_x < self.origin[0] - (self.size[0] / 2):
            pos_x = self.origin[0] - (self.size[0] / 2)
        elif pos_x > self.origin[0] + (self.size[0] / 2):
            pos_x = self.origin[0] + (self.size[0] / 2)
        if pos_y < self.origin[1] - (self.size[1] / 2):
            pos_y = self.origin[1] - (self.size[1] / 2)
        elif pos_y > self.origin[1] + (self.size[1] / 2):
            pos_y = self.origin[1] + (self.size[1] / 2)

        rel_x = ((pos_x - self.origin[0]) / self.d_x_size + (self.sub_displacements[0] / 2)) * (2 ** self.power)
        rel_y = ((pos_y - self.origin[1]) / self.d_y_size + (self.sub_displacements[1] / 2)) * (2 ** self.power)

        # poll from the four points around this one, and get an average
        poll1 = self.source[math.floor(rel_x), math.floor(rel_y)] * self.vertical_scale
        poll2 = self.source[math.floor(rel_x), math.ceil(rel_y)] * self.vertical_scale
        poll3 = self.source[math.ceil(rel_x), math.floor(rel_y)] * self.vertical_scale
        poll4 = self.source[math.ceil(rel_x), math.ceil(rel_y)] * self.vertical_scale

        return (poll1 + poll2 + poll3 + poll4) / 4 + self.origin[2]

    def __repr__(self, tab_level=-1):
        out = ""
        for b in self.displacement_brushes:
            out += b.__repr__(tab_level)
        return out

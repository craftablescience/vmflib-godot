"""

Classes that offer abstractions for brushes, etc. that aren't modeled
in the VMF format itself.

"""

from vmflib2 import brush, types, utility
import math


class Block:
    """A class representing a 3D block in terms of world geometry.

    This class allows for the simple creation and manipulation of 3D
    blocks (six-sided rectangular prisms) without having to manage
    the underlying brush (Solid) and its faces (Sides) manually.
    You can think of this as the programmatic analog to the Block Tool
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


class HollowBox:
    """A class representing an enclosed space created by 6 brushes.

    You can think of this as the programmatic analog to the Hollow function in the Hammer Editor
    """

    def __init__(self, origin=types.Vertex(), size=types.Vertex(), thickness=32):
        self.origin = origin

        for dim in size:
            if dim <= 0:
                raise ValueError("Solid cannot have negative size!")

        self.size = size
        self.thickness = thickness

        # Left wall
        self.left_wall = Block(
            types.Vertex(-self.thickness / 2 + self.origin[0] - self.size[0] / 2,
                         self.origin[1],
                         self.origin[2]),
            (self.thickness, self.size[1], self.size[2]))
        # Right wall
        self.right_wall = Block(
            types.Vertex(+self.thickness / 2 + self.origin[0] + self.size[0] / 2,
                         self.origin[1],
                         self.origin[2]),
            (self.thickness, self.size[1], self.size[2]))
        # Forward wall
        self.front_wall = Block(
            types.Vertex(self.origin[0],
                         self.thickness / 2 + self.origin[1] + self.size[1] / 2,
                         self.origin[2]),
            (self.size[0] + 2 * self.thickness, self.thickness, self.size[2]))
        # Rear wall
        self.back_wall = Block(
            types.Vertex(self.origin[0],
                         -self.thickness / 2 + self.origin[1] - self.size[1] / 2,
                         self.origin[2]),
            (self.size[0] + 2 * self.thickness, self.thickness, self.size[2]))

        # Ceiling
        self.ceiling = self.get_level_brush(self.size[2] / 2 + self.thickness / 2 + self.origin[2], self.thickness)
        # Floor
        self.floor = self.get_level_brush(-self.size[2] / 2 - self.thickness / 2 + self.origin[2], self.thickness)

        self.brushes = [self.left_wall, self.right_wall, self.front_wall, self.back_wall, self.ceiling, self.floor]


    def get_level_brush(self, z_origin, z_size):
        """Returns a brush the horizontal size of this box, with z_position and z_height given.
        Think of filling the box part way with water, and letting it settle. That's what this function generates."""
        return Block(
            types.Vertex(self.origin[0], self.origin[1], z_origin),
            (self.size[0], self.size[1], z_size)
        )

class DisplacementMap:
    """A class representing one upwards-facing mesh, possibly made of multiple displacements sewn together.

    """

    def __init__(self, source, source_alphas=None, origin=types.Vertex(), size=types.Vertex(), x_subdisplacements=4,
                 y_subdisplacements=4, power=3):
        # This is the data we will use to build our displacements.
        self.source = source
        # This is the data we use to build the alpha map
        self.source_alphas = source_alphas
        # This is the physical location of the DM's center.
        self.origin = origin
        # This is the length, width, and height of the DM
        self.size = size
        # This is the number of displacements we will have along the x and y axis, respectively.
        self.sub_displacements = (x_subdisplacements, y_subdisplacements)

        if power not in (2, 3, 4):
            raise ValueError("Power of a DisplacementMap must be 2, 3, or 4, not {0}.".format(power))

        # The power of each subdisplacement. (2 ^ power) is the number of grid points the displacement will have.
        self.power = power

        self.source_width = (2 ** self.power * self.sub_displacements[0]) + 1
        self.source_height = (2 ** self.power * self.sub_displacements[1]) + 1

        # The actual grid-size of displacement brushes
        self.d_x_size = self.size[0] / self.sub_displacements[0]
        self.d_y_size = self.size[1] / self.sub_displacements[1]

        # The actual grid-distance between points
        self.d_x_p_size = self.d_x_size / (2 ** self.power)
        self.d_y_p_size = self.d_y_size / (2 ** self.power)

        self.material = ""
        self.displacement_brushes = []

    def __getitem__(self, item):
        return self.source[item]

    def set_material(self, material: str):
        self.material = material
        for b in self.displacement_brushes:
            b.set_material(material)

    def get_relative_position(self, pos, round_result=False):
        """Given a 2D position in real space, returns a position in the DM's coordinate, I.E, with (0,0)
        being at the far lower left-hand corner of the displacement. Results will be clamped to be inside the
        DisplacementMap.
        """
        pos_x, pos_y = pos

        # Ensure that we're inside the grid
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
        if round_result:
            rel_x = int(rel_x)
            rel_y = int(rel_y)
        return rel_x, rel_y

    def get_height(self, pos):
        """Returns the real z coordinates that the DisplacementMap takes on at the given real 2D position"""

        rel_pos = self.get_relative_position(pos)

        # poll from the four points around this one, and get an average
        h = utility.bilinear_interp(self, rel_pos)
        # h = self.source[int(rel_pos[0]), int(rel_pos[1])]
        return h + self.origin[2]

    def get_surface_normals(self, pos):
        """Return a vector pointing directly away from the surface at this 2D DM coordinate (NOT the norms
        stored in the displacements themselves)"""

        x_dh = (self[pos[0] + 1, pos[1]] - self[pos])
        y_dh = (self[pos[0], pos[1] + 1] - self[pos])

        a = (self.d_x_p_size, 0, x_dh)
        b = (0, self.d_y_p_size, y_dh)
        c1, c2, c3 = utility.cross(a, b)

        # Normalize the vector!
        n = (c1 ** 2 + c2 ** 2 + c3 ** 2) ** 0.5
        return c1 / n, c2 / n, c3 / n

    def get_slope(self, pos):
        """Return the angle away from verticle that this 2D DM coordinate is facing"""

        return math.acos(utility.dot(self.get_surface_normals(pos), (0, 0, 1)))

    def realize(self):
        """Actually create the displacements that this entity is made out of."""
        if len(self.displacement_brushes) > 0:
            raise ValueError("Displacement map cannot be realized more than once!")

        rotation_counts = {
            (True, True): 3,
            (True, False): 0,
            (False, False): 1,
            (False, True): 2
        }
        for dx in range(self.sub_displacements[0]):
            for dy in range(self.sub_displacements[1]):

                power = 2 ** self.power

                x_offset = power * dx
                y_offset = power * dy

                # The actual position the displacement brush will be in
                x_pos = (dx - (self.sub_displacements[0] / 2) + 0.5) * self.d_x_size + self.origin.x
                y_pos = (dy - (self.sub_displacements[1] / 2) + 0.5) * self.d_y_size + self.origin.y

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
                        row.append(self[rel_x, rel_y])
                    dists.append(row)
                if self.source_alphas:
                    alphas = []
                    for x in x_range:
                        alphas_row = []
                        for y in y_range:
                            rel_x = x + x_offset
                            rel_y = y + y_offset
                            alphas_row.append(self.source_alphas[rel_x, rel_y])
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

                floor = Block(types.Vertex(x_pos, y_pos, self.origin.z),
                              (self.d_x_size, self.d_y_size, self.size[2]))
                if self.material != "":
                    floor.set_material(self.material)
                floor.top().children.append(d)  # Add disp map to the ground
                # Store these in case they're needed.
                floor.x_offset = x_offset
                floor.y_offset = y_offset

                self.displacement_brushes.append(floor)

    def __repr__(self, tab_level=-1):
        out = ""
        for b in self.displacement_brushes:
            out += b.__repr__(tab_level)
        return out

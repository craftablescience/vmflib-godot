#! /usr/bin/env python3
"""Example map generator: Woodbox

This script demonstrates vmflib by generating a map (consisting of a large
empty room) and writing it to "woodbox.vmf".  You can open the resulting file
using the Valve Hammer Editor and compile it for use in-game.

This example is a bit convoluted, since we are manually defining every brush
and each of its sides individually. Thankfully, there is now a higher-level
abstraction (tools.Block) which can be used to more easily create 3D block
shapes like the ones shown here. See the example named "woodbox_blocks" for
a demonstration.

"""

from vmflib2 import *
from vmflib2.games import base
import math
import colorsys

m = vmf.ValveMap()

# Set up brushes for our walls
walls = []
for i in range(6):
    walls.append(brush.Solid())

# Floor
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, -448),
    types.Vertex(512, 512, -448),
    types.Vertex(512, -512, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -512, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, -448),
    types.Vertex(-512, -512, -448),
    types.Vertex(-512, -512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, -512, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, -448),
    types.Vertex(-512, 512, -448),
    types.Vertex(-512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -512, -512),
    types.Vertex(-512, -512, -512),
    types.Vertex(-512, -512, -448))))
for side in sides:
    side.material = 'wood/woodwall009a'
walls[0].children.extend(sides)

# Wall 1
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -448, 512),
    types.Vertex(512, -448, 512),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -512, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, -448, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -448, 512),
    types.Vertex(-512, -512, 512),
    types.Vertex(-512, -512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -448, -512),
    types.Vertex(512, -512, -512),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -448, 512),
    types.Vertex(-512, -448, 512),
    types.Vertex(-512, -448, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -512, -512),
    types.Vertex(-512, -512, -512),
    types.Vertex(-512, -512, 512))))
for side in sides:
    side.material = 'wood/woodwall009a'
walls[1].children.extend(sides)

# Wall 2
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(512, 512, 512),
    types.Vertex(512, 448, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 448, -512),
    types.Vertex(512, 448, -512),
    types.Vertex(512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, 448, 512),
    types.Vertex(-512, 448, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, -512),
    types.Vertex(512, 448, -512),
    types.Vertex(512, 448, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, 512),
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, 512, -512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 448, -512),
    types.Vertex(-512, 448, -512),
    types.Vertex(-512, 448, 512))))
for side in sides:
    side.material = 'wood/woodwall009a'
walls[2].children.extend(sides)

# Wall 3
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 448, 448),
    types.Vertex(-448, 448, 448),
    types.Vertex(-448, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -448, -448),
    types.Vertex(-448, -448, -448),
    types.Vertex(-448, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 448, 448),
    types.Vertex(-512, -448, 448),
    types.Vertex(-512, -448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-448, 448, -448),
    types.Vertex(-448, -448, -448),
    types.Vertex(-448, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-448, 448, 448),
    types.Vertex(-512, 448, 448),
    types.Vertex(-512, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-448, -448, -448),
    types.Vertex(-512, -448, -448),
    types.Vertex(-512, -448, 448))))
for side in sides:
    side.material = 'wood/woodwall009a'
walls[3].children.extend(sides)

# Wall 4
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(448, 448, 448),
    types.Vertex(512, 448, 448),
    types.Vertex(512, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(448, -448, -448),
    types.Vertex(512, -448, -448),
    types.Vertex(512, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(448, 448, 448),
    types.Vertex(448, -448, 448),
    types.Vertex(448, -448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 448, -448),
    types.Vertex(512, -448, -448),
    types.Vertex(512, -448, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 448, 448),
    types.Vertex(448, 448, 448),
    types.Vertex(448, 448, -448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -448, -448),
    types.Vertex(448, -448, -448),
    types.Vertex(448, -448, 448))))
for side in sides:
    side.material = 'wood/woodwall009a'
walls[4].children.extend(sides)

# Wall 5
sides = []
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(512, 512, 512),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, -512, 448),
    types.Vertex(512, -512, 448),
    types.Vertex(512, 512, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, -512, 512),
    types.Vertex(-512, -512, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, 448),
    types.Vertex(512, -512, 448),
    types.Vertex(512, -512, 512))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, 512, 512),
    types.Vertex(-512, 512, 512),
    types.Vertex(-512, 512, 448))))
sides.append(brush.Side(types.Plane(
    types.Vertex(512, -512, 448),
    types.Vertex(-512, -512, 448),
    types.Vertex(-512, -512, 512))))
for side in sides:
    side.material = 'wood/woodwall009a'
walls[5].children.extend(sides)

# Generate u-v axis for each plane
for wall in walls:
    for side in wall.children:
        side.uaxis, side.vaxis = side.plane.sensible_axes()

# Add walls to world geometry
m.add_solids(walls)

spawn = base.InfoPlayerStart(m, origin=types.Origin(0, 0, -512 + 64))

# Generate the oblate-spheroid of light_spots that illuminate this room
for x_ang in range(-75,75, 15):
    x_a = math.radians(x_ang + 90)
    for y_ang in range(0, 360, 15):
        y_a = math.radians(y_ang)
        origin = types.Origin(
            256 * math.cos(y_a) * math.sin(x_a),
            256 * math.sin(y_a) * math.sin(x_a),
            -128 * math.cos(x_a)
        )
        # Get an rgb value from a hsv value
        rgb = colorsys.hsv_to_rgb(y_ang / 360, (x_ang / 180) + 0.5, 1)
        # Convert from [0-1] to [0-255]
        r, g, b = (int(v * 255) for v in rgb)
        light = "{0} {1} {2} 400".format(r, g, b)
        angles = types.Origin(x_ang, y_ang, 0)
        base.LightSpot(m, origin=origin, angles=angles, pitch=x_ang, _light=light)

# Write the map to a file
m.write_vmf('woodbox.vmf')

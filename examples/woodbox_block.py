#! /usr/bin/env python3
"""Example map generator: Woodbox (Block)

This script demonstrates vmflib by generating a map (consisting of a large
empty room) and writing it to "woodbox_block.vmf". You can open the resulting
file using the Valve Hammer Editor and compile it for use in-game.

This example shows off the tools.Block class, which allows for the easy
creation of 3D block brushes. It's pretty awesome.

"""
from vmflib2 import *
from vmflib2.games import base
from vmflib2.types import Vertex
from vmflib2.tools import Block
import math
import colorsys

m = vmf.ValveMap()

walls = []

# Floor
walls.append(Block(Vertex(0, 0, -512), (1024, 1024, 64)))

# Ceiling
walls.append(Block(Vertex(0, 0, 512), (1024, 1024, 64)))

# Left wall
walls.append(Block(Vertex(-512, 0, 0), (64, 1024, 1024)))

# Right wall
walls.append(Block(Vertex(512, 0, 0), (64, 1024, 1024)))

# Forward wall
walls.append(Block(Vertex(0, 512, 0), (1024, 64, 1024)))

# Rear wall
walls.append(Block(Vertex(0, -512, 0), (1024, 64, 1024)))

# Set each wall's material
for wall in walls:
    wall.set_material('wood/woodwall009a')

# Add walls to world geometry
m.add_solids(walls)

spawn = base.InfoPlayerStart(m, origin=types.Origin(0, 0, -512 + 32))

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
m.write_vmf('woodbox_block.vmf')

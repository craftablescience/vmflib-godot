#! /usr/bin/env python3
"""Example map generator: heightmap

This script demonstrates vmflib2 by generating a map with a 2D skybox and
some terrain (a displacement map).

"""
from vmflib2 import *
from vmflib2.types import Vertex
from vmflib2.tools import Block, DisplacementMap
from vmflib2.brush import DispInfo
import vmflib2.games.base as base
from PIL import Image
import random

m = vmf.ValveMap()

heightmap_range = 512

displacement_height_scale = heightmap_range / 255

map_size = (120 * 256, 120 * 256)
map_height = heightmap_range + 1024
water_height = 128

# Environment and lighting
# Sun angle	S Pitch	Brightness		Ambience
# 0 225 0	 -25	 254 242 160 400	172 196 204 80

displacements_per_side = 20

d_x_size = map_size[0] / displacements_per_side
d_y_size = map_size[1] / displacements_per_side

map_center = (0, 0)

image_size = 16 * displacements_per_side + 1

heightmap_file = "examples/height.png"

# Open up the source image and resize it to be the number of displacement points
image = Image.open(heightmap_file).resize((image_size, image_size), Image.BICUBIC).convert('L')
pixels = image.load()

new_source = dict()

# Flip the source image so that increasing y = going up in image, not down
for y in range(image_size - 1, -1, -1):
    for x in range(image_size):
        new_source[x, y] = pixels[x, image_size - y - 1]

# Determine the alphas for our ground. We want low and steep areas to be low alpha (sand) and high, level areas to be
#   high alpha (grass)
alphas = dict()

for x in range(image_size):
    for y in range(image_size):
        h = new_source[x, y] - water_height / displacement_height_scale
        if x > 0 and y > 0:
            rough_slope = ((new_source[x - 1, y] - new_source[x, y]) ** 2 + (
                new_source[x, y - 1] - new_source[x, y]) ** 2) ** (2 / 4)
        else:
            rough_slope = 0
        if h < 0:
            a = 0
        if h > 0:
            a = (h * 8)
        if a > 255:
            a = 255
        if h > 0:
            a -= rough_slope * 8
        if a < 0:
            a = 0
        alphas[x, y] = a

m.world.skyname = 'sky_day02_01'
light = base.LightEnvironment(m, angles="0 225 0", pitch=-25, _light="254 242 160 400", _ambient="172 196 204 80")

# Displacement map for the floor
# do cool stuff

disp_org = types.Vertex(map_center[0], map_center[1], -16)  # types.Vertex(map_size[0] / 2, -map_size[1] / 2, -16),

dm = DisplacementMap(source=new_source, source_alphas=alphas, origin=disp_org,
                     size=types.Vertex(map_size[0], map_size[1], 32), x_subdisplacements=displacements_per_side,
                     y_subdisplacements=displacements_per_side, vertical_scale=displacement_height_scale)

dm.set_material("nature/blendsandgrass008a")
m.add_solid(dm)

# This section places something on the surface every few units -- good for ensuring that the get_height method works
scatter_offset = 128
for x in range((map_center[0] - map_size[0] // 2) + scatter_offset, (map_center[0] + map_size[0] // 2), scatter_offset):
    for y in range((map_center[1] - map_size[1] // 2) + scatter_offset, (map_center[1] + map_size[1] // 2),
                   scatter_offset):
        h = dm.get_height((x, y))

        if water_height - 40 < h < water_height - 32 and random.randrange(10) == 1:
            base.PropPhysics(m, origin=types.Origin(x, y, water_height),
                             angles=types.Origin(0, random.randrange(360), 0),
                             model="models/props_canal/boat001{0}.mdl".format(("a", "b")[random.randrange(2)]))
        elif water_height + 128 < h and random.randrange(20) == 1:
            base.PropStatic(m, origin=types.Origin(x, y, h),
                            model="models/props_foliage/tree_deciduous_0{0}a.mdl".format(random.randrange(3) + 1),
                            angles=types.Origin(0, random.randrange(360), 0), skin=1)

# Real Floor (This is what seals the map to prevent leaks)
real_floor = Block(Vertex(map_center[0], map_center[1], -16), (map_size[0], map_size[1], 32), 'tools/toolsnodraw')

water = Block(Vertex(map_center[0], map_center[1], water_height / 2), (map_size[0], map_size[1], water_height),
              'tools/toolsnodraw')
water.top().material = 'nature/water_canals_city_murky'

# Ceiling
ceiling = Block(Vertex(map_center[0], map_center[1], map_height + 16), (map_size[0], map_size[1], 32))
ceiling.set_material('tools/toolsskybox2d')

# Prepare some upper walls for the skybox
skywalls = []
wall_thickness = 64

# Left wall
skywalls.append(
    Block(
        Vertex(-wall_thickness / 2 + map_center[0] - map_size[0] / 2, map_center[1], map_height / 2),
        (wall_thickness, map_size[1], map_height)))
# Right wall
skywalls.append(
    Block(Vertex(+wall_thickness / 2 + map_center[0] + map_size[0] / 2, map_center[1], map_height / 2),
          (64, map_size[1], map_height)))
# Forward wall
skywalls.append(
    Block(Vertex(map_center[0], wall_thickness / 2 + map_center[1] + map_size[1] / 2, map_height / 2),
          (map_size[0] + 2 * wall_thickness, wall_thickness, map_height)))
# Rear wall
skywalls.append(
    Block(Vertex(map_center[0], -wall_thickness / 2 + map_center[1] - map_size[1] / 2, map_height / 2),
          (map_size[0] + 2 * wall_thickness, wall_thickness, map_height)))
for wall in skywalls:
    wall.set_material('tools/toolsskybox2d')

# Add everything we prepared to the world geometry
m.add_solids(skywalls)
m.add_solids([ceiling, water, real_floor])

# Add the spawnpoint, at ground level, at the center of the map
spawn = base.InfoPlayerStart(m, origin=types.Origin(map_center[0], map_center[1], dm.get_height(map_center) + 38))

# Add a soundscape entity, up where we can see it, to the center of the map
base.EnvSoundscape(m, radius=-1, soundscape="coast.general_shoreline",
                   origin=types.Origin(map_center[0], map_center[1], map_height - 128))

# Write the map to a file
m.write_vmf('heightmap.vmf')

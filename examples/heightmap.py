#! /usr/bin/env python3
"""Example map generator: heightmap

This script demonstrates vmflib2 by generating a map with a 2D skybox and
some terrain (a displacement map).

"""
from vmflib2 import *
from vmflib2.types import Vertex, Output
from vmflib2.tools import Block, DisplacementMap
import vmflib2.games.base as base
import vmflib2.games.halflife2 as hl2
from PIL import Image
import random
import math


def slope_alphas(dm):
    """Set a DisplacementMap's alpha value based on it's slope and the water level"""

    # Calculate the alphas for the displacement map. We could have just as easily read this in from the image.
    for x in range(image_size - 1):
        for y in range(image_size - 1):
            h = dm[x, y]
            # Start with the assumption that this is straight sand
            a = 0
            # If we're above the water, then the alpha value will equal the height above the water, meaning that areas
            # 255 units above water-level will be pure grass
            if h > water_height:
                a = h - water_height
            if a > 255:
                a = 255
            # Subtract 3 times the angle (as 180 degrees = 255 alpha units) from the alpha value
            # This way, steeper areas appear sandier.
            a -= dm.get_slope((x, y)) * (255 / math.pi) * 3
            if a < 0:
                a = 0
            # Finally, we set the actual value to what we've determined
            dm.source_alphas[x, y] = a

def generate_scatter(dm):
    """Generate trees above the waterline, and boats near the shore."""
    # This section places something on the surface every few units -- good for ensuring that the get_height method works
    scatter_offset = 128
    for x in range((map_center[0] - map_size[0] // 2) + scatter_offset, (map_center[0] + map_size[0] // 2), scatter_offset):
        for y in range((map_center[1] - map_size[1] // 2) + scatter_offset, (map_center[1] + map_size[1] // 2),
                       scatter_offset):
            h = ground.get_height((x, y))

            if water_height - 64 < h < water_height - 32 and random.randrange(20) == 0:
                # This spot is in shallow water, so spawn a boat. (spawn it slightly higher than water level, so that it can float)
                base.PropPhysics(m, origin=types.Origin(x, y, water_height + 8),
                                 angles=types.Origin(0, random.randrange(360), 0),
                                 model="models/props_canal/boat001{0}.mdl".format(("a", "b")[random.randrange(2)]))
            elif water_height + 128 < h and random.randrange(20) == 0:
                # We have an area somewhat away from the shore, so we can put a tree here.
                base.PropStatic(m, origin=types.Origin(x, y, h - 3),
                                model="models/props_foliage/tree_deciduous_0{0}a.mdl".format(random.randrange(3) + 1),
                                angles=types.Origin(0, random.randrange(360), 0), skin=1)


def create_helicopter(m):
    """Creates a helicopter near the edge of the map, a path for it to patrol circling the map, and covers the map
    in air path nodes.
    """
    # How high off the ground the helicopter will be
    helicopter_height = 1024
    helicopter_path_node_count = 32
    helicopter_path_node_name = "heli_loop_path_{0}"
    # Create the helicopter path
    for i in range(helicopter_path_node_count):
        rad_ang = i * (2 * math.pi / helicopter_path_node_count)

        pos = (math.cos(rad_ang) * (map_size[0] / 2 - 1024), math.sin(rad_ang) * (map_size[1] / 2 - 1024))
        h = ground.get_height(pos) + helicopter_height
        org = types.Origin(pos[0], pos[1], h)

        if i == 0:
            hl2.NpcHelicopter(m, targetname="heli", target=helicopter_path_node_name.format(i), origin=org)
            # Make the helicopter start the patrol the moment the map spawns.
            base.LogicAuto(m).add_outputs([
                Output("OnMapSpawn", "heli", "StartPatrol"),
            ])

        base.PathTrack(m, origin=org, targetname=helicopter_path_node_name.format(i),
                       target=helicopter_path_node_name.format((i + 1) % helicopter_path_node_count))

    # Make air nodes so that the helicopter can navigate around the map if it decides to follow the player.
    # If we wanted to make this a real map, we'd program in some more advanced behavior, and design an interesting arena
    air_node_offset = 512
    node = 1
    for x in range((map_center[0] - map_size[0] // 2) + air_node_offset, (map_center[0] + map_size[0] // 2),
                   air_node_offset):
        for y in range((map_center[1] - map_size[1] // 2) + air_node_offset, (map_center[1] + map_size[1] // 2),
                       air_node_offset):
            h = ground.get_height((x, y)) + helicopter_height
            node += 1
            base.InfoNodeAir(m, origin=types.Origin(x, y, h), nodeid=node, nodeheight=h)

m = vmf.ValveMap()

heightmap_range = 1024

displacement_height_scale = heightmap_range / 255

map_size = ((64 + 32) * 256, (64 + 32) * 256)
map_height = heightmap_range + (1024 * 2)
water_height = 256

# Environment and lighting
# Sun angle	S Pitch	Brightness		Ambience
# 0 225 0	 -25	 254 242 160 400	172 196 204 80

displacements_per_side = 32

d_x_size = map_size[0] / displacements_per_side
d_y_size = map_size[1] / displacements_per_side

map_center = (0, 0)

# TODO pass power to DisplacementMap
power = 3

image_size = 2 ** power * displacements_per_side + 1

heightmap_file = "examples/height.png"

# Open up the source image and resize it to be the number of displacement points
image = Image.open(heightmap_file).resize((image_size, image_size), Image.BICUBIC).convert('L')
pixels = image.load()

# This is where we will be putting the information from the image
#   (This could have just as easily come from somewhere else, like perlin noise)
new_source = dict()

# Flip the source image so that increasing y = going up in image, not down
# Also, scale the source to the height we want
for y in range(image_size - 1, -1, -1):
    for x in range(image_size):
        new_source[x, y] = pixels[x, image_size - y - 1] * displacement_height_scale

# Determine the alphas for our ground. We want low and steep areas to be low alpha (sand) and high, level areas to be
#   high alpha (grass)
alphas = dict()

# For now, we set all the alphas to 0. We will determine their actual values after we've set up the DisplacementMap.
for x in range(image_size):
    for y in range(image_size):
        alphas[x, y] = 0

m.world.skyname = 'sky_day02_01'
light = base.LightEnvironment(m, angles="0 225 0", pitch=-25, _light="254 242 160 400", _ambient="172 196 204 80")

# Displacement map for the floor
# do cool stuff

disp_org = types.Vertex(map_center[0], map_center[1], -16)  # types.Vertex(map_size[0] / 2, -map_size[1] / 2, -16),

# Create a DisplacementMap to act as the ground.
ground = DisplacementMap(source=new_source, source_alphas=alphas, origin=disp_org,
                         size=types.Vertex(map_size[0], map_size[1], 32), x_subdisplacements=displacements_per_side,
                         y_subdisplacements=displacements_per_side, power=power)
m.add_solid(ground)

# We choose a texture that supports alpha blending, to show off that feature.
ground.set_material("nature/blendsandgrass008a")

# Set the alpha values based off of the slope and water level. We need to do this before dm.realize() has been called,
#  as that's when the values we calculate get used.
slope_alphas(ground)

# Create the displacement brushes from the displacement map.
ground.realize()

# Create the trees and boats.
generate_scatter(ground)

# Real Floor (This is what seals the map to prevent leaks)
real_floor = Block(Vertex(map_center[0], map_center[1], -16), (map_size[0], map_size[1], 32), 'tools/toolsnodraw')

# This is the water brush. As is good practice, only the surface of the water has a water texture; the rest is nodraw
water = Block(Vertex(map_center[0], map_center[1], water_height / 2), (map_size[0], map_size[1], water_height),
              'tools/toolsnodraw')
water.top().material = 'nature/water_canals_city_murky'

# Ceiling
ceiling = Block(Vertex(map_center[0], map_center[1], map_height + 16), (map_size[0], map_size[1], 32))
ceiling.set_material('tools/toolsskybox2d')

# add a func_viscluster, because all of the vis leaves in this open map can see each other; this tells vvis.exe the
# result it will ultimately come to. This speeds up map compilation considerably.
for h in (map_height - 16, 16):
    # (we create two, one at the top of the map, and one at the bottom. this is because the water brush splits the vis-leafs)
    viscluster = base.FuncViscluster(m)
    viscluster_brush = Block(Vertex(map_center[0], map_center[1], h), (map_size[0], map_size[1], 32))
    viscluster_brush.set_material('tools/toolstrigger')
    viscluster.children.append(viscluster_brush)

# We surround the map with a giant box, to be a skybox. Note that being this open is incredibly inefficient, which is
# why we made the visclusters earlier.
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
player_origin = types.Origin(map_center[0], map_center[1], ground.get_height(map_center) + 38)
spawn = base.InfoPlayerStart(m, origin=player_origin)
suit = hl2.ItemSuit(m, origin=player_origin)

airboat_spawn = (map_center[0] + 512, map_center[1])
airboat = hl2.PropVehicleAirboat(m, origin=types.Origin(airboat_spawn[0], airboat_spawn[1],
                                                        ground.get_height(airboat_spawn) + 32), EnableGun=1)

# Add a soundscape entity, up where we can see it, to the center of the map
base.EnvSoundscape(m, radius=-1, soundscape="coast.general_shoreline",
                   origin=types.Origin(map_center[0], map_center[1], map_height - 128))

create_helicopter(m)

# Write the map to a file
m.write_vmf('heightmap.vmf')

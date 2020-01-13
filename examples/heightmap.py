#! /usr/bin/env python3
"""Example map generator: heightmap

This script demonstrates vmflib2 by generating a map with a 2D skybox and
some terrain (a displacement map).

"""
from vmflib2 import *
from vmflib2.types import Vertex, Output
from vmflib2.tools import Block, DisplacementMap, HollowBox
import vmflib2.games.base as base
import vmflib2.games.halflife2 as hl2
from PIL import Image
import random
import math


def slope_alphas(dm):
    """Set a DisplacementMap's alpha value based on its slope and the water level"""

    # Calculate the alphas for the displacement map. We could have just as easily read this in from the image.
    for x in range(image_size - 1):
        for y in range(image_size - 1):
            h = dm[x, y]
            # Start with the assumption that this is straight sand
            a = 0
            # If we're above the water, then the alpha value will equal the height above the water (* 2), meaning that
            # areas 128 units above water-level will be pure grass
            if h > water_height:
                a = (h - water_height) * 2
            if a > 255:
                a = 255

            # Get the angle of the slope here
            slope_angle = math.degrees(dm.get_slope((x, y)))

            # Add a sharp decrease in alpha around 45 degrees, so that unclimbable areas are visible
            if slope_angle > 30 and slope_angle < 60:
                a -= (slope_angle - 30) * 7
            elif slope_angle >= 60:
                a -= (slope_angle - 60) * 2 + 210

            if a < 0:
                a = 0
            # Finally, we set the actual value to what we've determined
            dm.source_alphas[x, y] = a

def generate_scatter(dm):
    """Generate trees above the waterline, and boats near the shore."""
    # This section places something on the surface every few units -- good for testing out the get_height method
    scatter_offset = 128
    for x in range((map_center[0] - map_size[0] // 2) + scatter_offset, (map_center[0] + map_size[0] // 2), scatter_offset):
        for y in range((map_center[1] - map_size[1] // 2) + scatter_offset, (map_center[1] + map_size[1] // 2),
                       scatter_offset):

            slope_angle = math.degrees(dm.get_slope(dm.get_relative_position((x,y))))
            h = ground.get_height((x, y))

            if water_height - 64 < h < water_height - 32 and random.randrange(20) == 0:
                # This spot is in shallow water, so spawn a boat. (spawn it slightly higher than water level, so that it can float)
                base.PropPhysics(m, origin=types.Origin(x, y, water_height + 8),
                                 angles=types.Origin(0, random.randrange(360), 0),
                                 model="models/props_canal/boat001{0}.mdl".format(("a", "b")[random.randrange(2)]))
            elif water_height + 128 < h and random.randrange(15) == 0 and slope_angle < 30:
                # We have a flat area somewhat away from the shore, so we can put a tree here.
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

heightmap_range = 1024 * 4

displacement_height_scale = heightmap_range / 255

displacements_per_side = 20

# We want the size of displacements to be multiples of 1024 because that gives VVIS an easier time of it
map_size = (1024*displacements_per_side, 1024*displacements_per_side)
map_height = heightmap_range + (1024 * 2)
water_height = 512

# Environment and lighting
# Sun angle	S Pitch	Brightness		Ambience
# 0 225 0	 -25	 254 242 160 400	172 196 204 80


d_x_size = map_size[0] / displacements_per_side
d_y_size = map_size[1] / displacements_per_side

map_center = (0, 0)

# TODO pass power to DisplacementMap
power = 3

image_size = 2 ** power * displacements_per_side + 1

heightmap_file = "height4.png"

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
                         y_subdisplacements=displacements_per_side, power=power, add_nodraw_brush=True)
m.add_solid(ground)

# We choose a texture that supports alpha blending, to show off that feature.
ground.set_material("nature/blendsandgrass008a")

# Set the alpha values based off of the slope and water level. We need to do this before dm.realize() has been called,
#  as that's when the values we calculate get used.
slope_alphas(ground)

# Create the displacement brushes from the displacement map.
ground.realize()

# Change all the high displacements to a material that has rocks instead of sand. (This value is carefully selected)
for block in ground.get_brushes_above_level(1096):
    block.set_material("nature/blendrocksgrass006a")

# Create the trees and boats.
generate_scatter(ground)


# We surround the map with a giant box, to be a skybox
skybox = HollowBox((map_center[0], map_center[1], map_height / 2), (map_size[0], map_size[1], map_height))
for brush in skybox.brushes:
    brush.set_material('tools/toolsskybox2d')
skybox.floor.set_material("tools/toolsnodraw")

# This is the water brush. As is good practice, only the surface of the water has a water texture; the rest is nodraw
water = skybox.get_level_brush(water_height / 2, water_height)
water.set_material("tools/toolsnodraw")
water.top().material = 'nature/water_canals_city_murky'

# Add everything we prepared to the world geometry
m.add_solids(skybox.brushes)
m.add_solid(water)

# Enclosing maps with big, open skyboxes like the one we just made is inefficient because we have a bunch of visleaves
#   touching each other. Instead of letting vvis.exe check all of them, we just tell it they're all connected via
#   a func_viscluster
viscluster = base.FuncViscluster(m)
viscluster_brush = skybox.get_level_brush(map_height - 16, 32)
viscluster_brush.set_material('tools/toolstrigger')
viscluster.children.append(viscluster_brush)

# We want to chop the visleaves in half, so that the mountains in the middle can actually block visibility.
hint_brush = skybox.get_level_brush(1450,4)
hint_brush.set_material("tools/toolsskip")
hint_brush.bottom().material = "tools/toolshint"
m.add_solid(hint_brush)


# Add the spawnpoint, at ground level, at the center of the map
player_origin = types.Origin(map_center[0], map_center[1], ground.get_height(map_center) + 38)
spawn = base.InfoPlayerStart(m, origin=player_origin)
suit = hl2.ItemSuit(m, origin=player_origin)



airboat_spawn = (map_center[0] + 650, map_center[1])
airboat = hl2.PropVehicleAirboat(m, origin=types.Origin(airboat_spawn[0], airboat_spawn[1],
                                                        ground.get_height(airboat_spawn) + 32), EnableGun=1)

# Add a soundscape entity, up where we can see it, to the center of the map
base.EnvSoundscape(m, radius=-1, soundscape="coast.general_shoreline",
                   origin=types.Origin(map_center[0], map_center[1], map_height - 128))

create_helicopter(m)

# Write the map to a file
m.write_vmf('heightmap.vmf')

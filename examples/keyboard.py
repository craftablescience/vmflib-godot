#! /usr/bin/env python3
"""Example map generator: keyboard

This script demonstrates vmflib by generating a map (consisting of a room containing a musical keyboard)
and writing it to "keyboard.vmf".  You can open the resulting file
using the Valve Hammer Editor and compile it for use in-game.


"""

from vmflib2 import *
from vmflib2.games import base
from vmflib2.games import halflife2
from vmflib2.types import Vertex, Output
from vmflib2.tools import Block
import math

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

# Create the player spawn and some weapons to trigger the keys
player_spawn_origin = types.Origin(128, 0, -512 + 32)
spawn = base.InfoPlayerStart(m, angles="0 180 0", origin=player_spawn_origin)
halflife2.ItemSuit(m, origin=player_spawn_origin)
halflife2.WeaponCrowbar(m, origin=player_spawn_origin)
for i in range(5):
    halflife2.WeaponFrag(m, origin=player_spawn_origin)

# Make manhacks okay with players
halflife2.AiRelationship(m, targetname="hack_r", disposition=3, rank=10, StartActive=1, subject="npc_manhack", target="!player")

# Make a stack of 5 crates full of manhacks
crate_height = 25
for z in range(-512 + crate_height + 32, -512 + (5 * crate_height) + 32, crate_height):
    org = types.Origin(0, 128, z)
    crate = halflife2.ItemItemCrate(m, origin=org, ItemClass="npc_manhack", ItemCount=3)
    crate.add_output(Output("OnBreak", "hack_r", "ApplyRelationship"))

key_count = 39
key_width = 32 + 8
lowest_pitch = 20
last_y_value = - (key_count / 3.6) * key_width

# Create the keyboard
for key_number in range(key_count):

    white_key = (key_number % 12 in (0, 2, 4, 5, 7, 9, 11))
    model = "models/humans/group01/male_02.mdl" if white_key else "models/humans/group01/male_01.mdl"

    if white_key:
        org = types.Origin(-128, last_y_value, -512 + 32)
        last_y_value += key_width
    else:
        org = types.Origin(-128 - 32, last_y_value - key_width / 2, -512 + 32)

    key = halflife2.NpcCitizen(m, origin=org, targetname="wk_key_{0}".format(key_number), model=model, citizentype=0,
                               spawnflags=1064960)

    # This equation gives us 12 pitches per octave
    pitch = ((2 ** (key_number / 12))) * lowest_pitch

    sound = base.AmbientGeneric(m, origin=org, targetname="wk_sound_{0}".format(key_number),
                                message="hl1/fvox/beep.wav", pitch=pitch, pitchstart=pitch, spawnflags=49,
                                SourceEntityName=key.targetname)

    key.add_outputs([
        Output("OnPlayerUse", key.targetname, "FireUser1"),
        Output("OnDamaged", key.targetname, "FireUser1"),
        Output("OnUser1", sound.targetname, "PlaySound", "", 0.1),
        # Output("OnUser1", sound.targetname, "StopSound", "", 1),
        Output("OnUser1", sound.targetname, "Pitch", pitch),
        Output("OnUser1", key.targetname, "Color", "0 255 0", 0.1),
        Output("OnUser1", key.targetname, "SetHealth", 1000),
        Output("OnUser1", key.targetname, "Color", "255 255 255", 1),
    ])

# Generate the circle of light_spots that illuminate this room

for y_ang in range(0, 360, 15):
    y_a = math.radians(y_ang)
    origin = types.Origin(
        64 * math.cos(y_a),
        64 * math.sin(y_a),
        -128
    )
    angles = types.Origin(-45, y_ang, 0)
    base.LightSpot(m, origin=origin, angles=angles, pitch=-45)

# Write the map to a file
m.write_vmf('keyboard.vmf')

#! /usr/bin/env python3
"""Example map generator: King of the Hill Example

This script demonstrates vmflib2 by generating a basic "king of the hill" style
map.  "King of the hill" is a game mode in Team Fortress 2 where each team
tries to maintain control of a central "control point" for some total defined
amount of time (before the other team does).

After this script executes, the map will be written to: koth_vmflib_example.vmf

This example highlights the use of TF2 game mechanics (in this case the use of
a control point and a goal timer). A simple implementation of team
spawn/resupply areas is also included.

https://developer.valvesoftware.com/wiki/Creating_a_Capture_Point
https://developer.valvesoftware.com/wiki/TF2/King_of_the_Hill
"""

from vmflib2 import *
from vmflib2.types import Vertex, Output, Origin
from vmflib2.tools import Block
import vmflib2.games.base as source
import vmflib2.games.tf as tf2

m = vmf.ValveMap()
la = source.LogicAuto(m)
gr = tf2.TfGamerules(m, targetname="game_rules")
tf2.TfLogicKoth(m, unlock_point=5)

la.add_outputs([
    Output("OnMapSpawn", gr.targetname, "SetBlueTeamGoalString", "#koth_setup_goal"),  # KOTH-specific
    Output("OnMapSpawn", gr.targetname, "SetRedTeamGoalString", "#koth_setup_goal"),  # KOTH-specific
    Output("OnMapSpawn", gr.targetname, "SetBlueTeamRespawnWaveTime", 6),  # KOTH-specific
    Output("OnMapSpawn", gr.targetname, "SetRedTeamRespawnWaveTime", 6),  # KOTH-specific
])

# Environment and lighting (these values come from Sky List on Valve dev wiki)
# Sun angle  S Pitch  Brightness         Ambience
# 0 300 0    -20      238 218 181 250    224 188 122 250
m.world.skyname = 'sky_harvest_01'
light = source.LightEnvironment(m, angles="0 300 0", pitch=-20, _light="238 218 181 250", _ambient="224 188 122 250")

# Ground
ground = Block(Vertex(0, 0, -32), (2048, 2048, 64), 'nature/dirtground004')
m.add_solid(ground)

# Skybox
skybox = [
    Block(Vertex(0, 0, 2048), (2048, 2048, 64)),     # Ceiling
    Block(Vertex(-1024, 0, 1024), (64, 2048, 2048)),    # Left wall
    Block(Vertex(1024, 0, 1024), (64, 2048, 2048)),     # Right wall
    Block(Vertex(0, 1024, 1024), (2048, 64, 2048)),     # Forward wall
    Block(Vertex(0, -1024, 1024), (2048, 64, 2048))     # Rear wall
]
for wall in skybox:
    wall.set_material('tools/toolsskybox2d')

m.add_solids(skybox)

# Control point master entity
cp_master = tf2.TeamControlPointMaster(m, targetname="master_control_point", caplayout="0")

# Control point entity
cp = tf2.TeamControlPoint(m, targetname="control_point_1", point_printname="Central Point")

# Control point prop
cp_prop = source.PropDynamic(m, targetname="prop_cap_1", model="models/props_gameplay/cap_point_base.mdl")

# Capture area
cp_area = tf2.TriggerCaptureArea(m, area_cap_point=cp.targetname)
cp_area.children.append(Block(Vertex(0, 0, 128), (256, 256, 256), 
    "TOOLS/TOOLSTRIGGER"))
cp_area.add_outputs([
    Output("OnCapTeam1", cp_prop.targetname, "Skin", 1),  # Not KOTH-specific
    Output("OnCapTeam2", cp_prop.targetname, "Skin", 2),  # Not KOTH-specific
    Output("OnCapTeam1", gr.targetname, "SetRedKothClockActive"),  # KOTH-only
    Output("OnCapTeam2", gr.targetname, "SetBlueKothClockActive")  # KOTH-only
])

# Player spawn areas

# Define RED spawn
spawn_red = tf2.InfoPlayerTeamspawn(m, origin=Origin(900, 900, 5), angles="0 -135 0", TeamNum=2)
health_red = tf2.ItemHealthkitFull(m, origin=Origin(950, 910, 0), TeamNum=2)
ammo_red = tf2.ItemAmmopackFull(m, origin=Origin(910, 950, 0), TeamNum=2)

# Define BLU spawn
spawn_blu = tf2.InfoPlayerTeamspawn(m, origin=Origin(-900, -900, 5), angles="0 -135 0", TeamNum=3)
health_blu = tf2.ItemHealthkitFull(m, origin=Origin(-950, -910, 0), TeamNum=3)
ammo_blu = tf2.ItemAmmopackFull(m, origin=Origin(-910, -950, 0), TeamNum=3)


# Write the map to a file
m.write_vmf('koth_vmflib_example.vmf')

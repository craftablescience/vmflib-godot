"""
Helper classes for creating maps in any Source Engine game that uses portal.fgd.
This file was auto-generated by import_fgd.py on 2018-06-20 02:19:30.503849.
"""

from vmflib2.vmf import *


class EnvLightrailEndpoint(Entity):
    """
    Auto-generated from portal.fgd, line 338.
    Special effects for the endpoints of the lightrail.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "env_lightrail_endpoint", vmf_map)

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Scale Small FX : Scale of the small effect.  1 is the default size, 2 is twice that, etc.
        self.small_fx_scale = 1 
        # Scale Large FX : Scale of the large effect.  1 is the default size, 2 is twice that, etc.
        self.large_fx_scale = 1 

        self.auto_properties.extend(["angles", "targetname", "parentname", "spawnflags", "small_fx_scale", "large_fx_scale"])


class EnvPortalCredits(Entity):
    """
    Auto-generated from portal.fgd, line 364.
    An entity to control the rolling credits for portal.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "env_portal_credits", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""


        self.auto_properties.extend(["targetname"])


class EnvPortalPathTrack(Entity):
    """
    Auto-generated from portal.fgd, line 45.
    An entity used to build paths for other entities to follow. Each path_track is a node on the path, each holding the name of the next path_track in the path.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "env_portal_path_track", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Scale Track FX : The amount to scale the track FX size
        self.Track_beam_scale = 0 
        # Scale Endpoint FX : The amount to scale the endpoint FX size.
        self.End_point_scale = 0 
        # Fade Out Endpoint : Amount of time to fade out the endpoint FX
        self.End_point_fadeout = 0 
        # Fade In Endpoint : Amount of time to fade in the endpoint FX
        self.End_point_fadein = 0 
        # Next Stop Target : The next path_track in the path.
        self.target = ""
        # Branch Path : An alternative path_track to be the next node in the path. Useful for making branching paths. Use the ToggleAlternatePath / EnableAlternatePath inputs to make the alternative path active.
        self.altpath = ""
        # New Train Speed : When the train reaches this path_track, it will set its speed to this speed. 
        self.speed = 0 
        # Path radius : Used by NPCs who follow track paths (attack chopper/gunship). This tells them the maximum distance they're allowed to be from the path at this node.
        self.radius = 0 
        # Orientation Type : The way that the path follower faces as it moves through this path track.
        self.orientationtype = 1 

        self.auto_properties.extend(["targetname", "parentname", "angles", "spawnflags", "Track_beam_scale", "End_point_scale", "End_point_fadeout", "End_point_fadein", "target", "altpath", "speed", "radius", "orientationtype"])


class FuncLiquidportal(Entity):
    """
    Auto-generated from portal.fgd, line 174.
    A space that fills with portal liquid and teleports entities when done filling
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "func_liquidportal", vmf_map)

        # Origin (X Y Z) : The position of this entity's center in the world. Rotating entities typically rotate around their origin.
        self.origin = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.InitialLinkedPortal = ""
        # TODO: Replace this filler. : TODO: Replace this filler.
        self.FillTime = ""

        self.auto_properties.extend(["origin", "angles", "InitialLinkedPortal", "FillTime"])


class FuncNoportalVolume(Entity):
    """
    Auto-generated from portal.fgd, line 127.
    A region in which no portal can be placed
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "func_noportal_volume", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""

        self.auto_properties.extend(["targetname", "parentname", "spawnflags"])


class FuncPortalBumper(Entity):
    """
    Auto-generated from portal.fgd, line 140.
    A region that portals trace to fit outside of but can be place on
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "func_portal_bumper", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""

        self.auto_properties.extend(["targetname", "parentname", "spawnflags"])


class FuncPortalDetector(Entity):
    """
    Auto-generated from portal.fgd, line 154.
    A region that fires an output if a portal is placed in it
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "func_portal_detector", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Portal pair ID that it detects : TODO: Replace this filler.
        self.LinkageGroupID = 0

        self.auto_properties.extend(["targetname", "parentname", "spawnflags", "LinkageGroupID"])


class FuncPortalOrientation(Entity):
    """
    Auto-generated from portal.fgd, line 107.
    Adjusts a portal's rotation to match a specified angle. The 'Bottom' of the portal points in the specified diretion.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "func_portal_orientation", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Start Disabled : TODO: Replace this filler.
        self.StartDisabled = 0 

        # Angles to face : The 'floor' of the portal pair linkage will be in this direction.
        self.AnglesToFace = "0 0 0" 
        # Match linked angles. : If set, portals placed in this volume will have their angles match their linked portals. This only works for floor or ceiling portals with a currently linked partner.
        self.MatchLinkedAngles = 0 

        self.auto_properties.extend(["targetname", "parentname", "StartDisabled", "AnglesToFace", "MatchLinkedAngles"])


class FuncWeightButton(Entity):
    """
    Auto-generated from portal.fgd, line 118.
    A button which activates after a specified amount of weight is applied
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "func_weight_button", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.WeightToActivate = ""

        self.auto_properties.extend(["targetname", "WeightToActivate"])


class InfoLightingRelative(Entity):
    """
    Auto-generated from portal.fgd, line 385.
    
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "info_lighting_relative", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Lighting Landmark : Entity at which the reference origin is contained. 
        self.LightingLandmark = ""

        self.auto_properties.extend(["targetname", "parentname", "LightingLandmark"])


class NpcPortalTurretFloor(Entity):
    """
    Auto-generated from portal.fgd, line 267.
    Combine (Portal) Floor Turret
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "npc_portal_turret_floor", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Skin Number : Which skin to use for this turret. Set to 0 to select randomly.
        self.SkinNumber = 0 

        # Damage pushes player : Being hit by this turret will push the player back.
        self.DamageForce = 1 

        self.auto_properties.extend(["targetname", "angles", "spawnflags", "SkinNumber", "DamageForce"])


class NpcPortalTurretGround(Entity):
    """
    Auto-generated from portal.fgd, line 243.
    Combine (Portal) ground turret
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "npc_portal_turret_ground", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # Render FX : TODO: Replace this filler.
        self.renderfx = 0 

        # Render Mode : Used to set a non-standard rendering mode on this entity. See also 'FX Amount' and 'FX Color'.
        self.rendermode = 0 
        # FX Amount (0 - 255) : The FX amount is used by the selected Render Mode.
        self.renderamt = 255 
        # FX Color (R G B) : The FX color is used by the selected Render Mode.
        self.rendercolor = "255 255 255" 
        # Disable Receiving Shadows : TODO: Replace this filler.
        self.disablereceiveshadows = 0 

        # Damage Filter : Name of the filter entity that controls which entities can damage us.
        self.damagefilter = "" 

        # Response Contexts : Response system context(s) for this entity. Format should be: 'key:value,key2:value2,etc'. When this entity speaks, the list of keys & values will be passed to the response rules system.
        self.ResponseContext = "" 

        # Disable shadows : TODO: Replace this filler.
        self.disableshadows = 0 

        # Target Path Corner : If set, the name of a path corner entity that this NPC will walk to, after spawning.
        self.target = ""
        # Squad Name : NPCs that are in the same squad (i.e. have matching squad names) will share information about enemies, and will take turns attacking and covering each other.
        self.squadname = ""
        # Hint Group : Hint groups are used by NPCs to restrict their hint-node searching to a subset of the map's hint nodes. Only hint nodes with matching hint group names will be considered by this NPC.
        self.hintgroup = "" 
        # Hint Limit Nav : Limits NPC to using specified hint group for navigation requests, but does not limit local navigation.
        self.hintlimiting = 0 
        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Sleep State : Holds the NPC in stasis until specified condition. See also 'Wake Radius' and 'Wake Squad'.
        self.sleepstate = 0 
        # Wake Radius : Auto-wake if player within this distance
        self.wakeradius = 0 
        # Wake Squad : Wake all of the NPCs squadmates if the NPC is woken
        self.wakesquad = 0 
        # Enemy Filter : Filter by which to filter potential enemies
        self.enemyfilter = "" 
        # Ignore unseen enemies : Prefer visible enemies, regardless of distance or relationship priority
        self.ignoreunseenenemies = 0 
        # Physics Impact Damage Scale : Scales damage energy when this character is hit by a physics object. With a value of 0 the NPC will take no damage from physics.
        self.physdamagescale = "1.0" 

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""



        # TODO: Replace this filler. : TODO: Replace this filler.
        self.ConeOfFire = ""

        self.auto_properties.extend(["targetname", "angles", "renderfx", "rendermode", "renderamt", "rendercolor", "disablereceiveshadows", "damagefilter", "ResponseContext", "disableshadows", "target", "squadname", "hintgroup", "hintlimiting", "spawnflags", "sleepstate", "wakeradius", "wakesquad", "enemyfilter", "ignoreunseenenemies", "physdamagescale", "parentname", "ConeOfFire"])


class NpcRocketTurret(Entity):
    """
    Auto-generated from portal.fgd, line 27.
    Aims a rocket at a target.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "npc_rocket_turret", vmf_map)

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""

        self.auto_properties.extend(["parentname", "targetname", "angles", "spawnflags"])


class NpcSecurityCamera(Entity):
    """
    Auto-generated from portal.fgd, line 278.
    Security Camera
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "npc_security_camera", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # World Model : TODO: Replace this filler.
        self.model = ""
        # Skin : Some models have multiple versions of their textures, called skins. Set this to a number other than 0 to use that skin instead of the default.
        self.skin = 0 
        # Disable Shadows : Used to disable dynamic shadows on this entity.
        self.disableshadows = 0 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""

        self.auto_properties.extend(["targetname", "angles", "model", "skin", "disableshadows", "spawnflags"])


class PointEnergyBallLauncher(Entity):
    """
    Auto-generated from portal.fgd, line 15.
    Launches energy balls.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "point_energy_ball_launcher", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Origin (X Y Z) : The position of this entity's center in the world. Rotating entities typically rotate around their origin.
        self.origin = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # Global Entity Name : Name by which this entity is linked to another entity in a different map. When the player transitions to a new map, entities in the new map with globalnames matching entities in the previous map will have the previous map's state copied over their state.
        self.globalname = "" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Ball count : This is how many balls will be bouncing around inside the spawner
        self.ballcount = 3 
        # Min ball speed : The minimum speed of balls that fly in the spawner
        self.minspeed = "300.0" 
        # Max ball speed : The maximum speed of balls that fly in the spawner
        self.maxspeed = "600.0" 
        # Ball radius : The radius of the energy balls
        self.ballradius = "20.0" 
        # Ball Type : TODO: Replace this filler.
        self.balltype = "Combine Energy Ball 1" 
        # Ball Respawn Time : The energy balls respawn time
        self.ballrespawntime = "4.0f" 

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.BallLifetime = ""
        # Min life after portal transition : When energy balls created by this launcher pass through a portal and their life is refreshed to be this number at minimum.
        self.MinLifeAfterPortal = 6 

        self.auto_properties.extend(["targetname", "origin", "angles", "globalname", "spawnflags", "ballcount", "minspeed", "maxspeed", "ballradius", "balltype", "ballrespawntime", "parentname", "targetname", "BallLifetime", "MinLifeAfterPortal"])


class PropGladosCore(Entity):
    """
    Auto-generated from portal.fgd, line 249.
    Core of GlaDOS computer.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "prop_glados_core", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Global Entity Name : Name by which this entity is linked to another entity in a different map. When the player transitions to a new map, entities in the new map with globalnames matching entities in the previous map will have the previous map's state copied over their state.
        self.globalname = "" 

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # World Model : TODO: Replace this filler.
        self.model = ""
        # Skin : Some models have multiple versions of their textures, called skins. Set this to a number other than 0 to use that skin instead of the default.
        self.skin = 0 
        # Disable Shadows : Used to disable dynamic shadows on this entity.
        self.disableshadows = 0 

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Damage Filter : Name of the filter entity that controls which entities can damage us.
        self.damagefilter = "" 

        # Disable shadows : TODO: Replace this filler.
        self.disableshadows = 0 

        # Explosion Damage : If non-zero, when this entity breaks it will create an explosion that causes the specified amount of damage. See also 'Explosion Radius'.
        self.ExplodeDamage = 0 
        # Explosion Radius : If non-zero, when this entity breaks it will create an explosion with a radius of the specified amount. See also 'Explosion Damage'.
        self.ExplodeRadius = 0 
        # Performance Mode : Used to limit the amount of gibs produced when this entity breaks, for performance reasons.
        self.PerformanceMode = 0 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Pressure Delay : Delay, in seconds, after 'broken' by pressure before breaking apart (allows for sound to play before breaking apart).
        self.pressuredelay = 0 

        # Minimum DX Level : TODO: Replace this filler.
        self.mindxlevel = 0 
        # Maximum DX Level : TODO: Replace this filler.
        self.maxdxlevel = 0 

        # Start Fade Dist : Distance at which the prop starts to fade (<0 = use fademaxdist).
        self.fademindist = -1 
        # End Fade Dist : Max fade distance at which the prop is visible (0 = don't fade out)
        self.fademaxdist = 0 
        # Fade Scale : If you specify a fade in the worldspawn, or if the engine is running under dx7, then the engine will forcibly fade out props even if fademindist/fademaxdist isn't specified.
        self.fadescale = 1 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Min Damage to Hurt : The prop will ignore any damage events if the damage is less than this amount.
        self.minhealthdmg = 0 
        # Shadow Cast Distance : Use this to override how far this object casts shadows. 0 = default distance.
        self.shadowcastdist = 0 
        # Physics Impact Damage Scale : Scales damage energy when this object is hit by a physics object. NOTE: 0 means this feature is disabled for backwards compatibility.\nSet to 1.0 for materials as strong as flesh, smaller numbers indicate stronger materials.
        self.physdamagescale = "0.1" 
        # Impact damage type : TODO: Replace this filler.
        self.Damagetype = 0 
        # Damaging it Doesn't Push It : Used to determine whether or not damage should cause the brush to move.
        self.nodamageforces = 0 
        # Scale Factor For Inertia : Scales the angular mass of an object. Used to hack angular damage and collision response.
        self.inertiaScale = "1.0" 
        # Mass Scale : A scale multiplier for the object's mass.
        self.massScale = "0" 
        # Override Parameters : A list of physics key/value pairs that are usually in a physics prop .qc file. Format is 'key,value,key,value,etc'.
        self.overridescript = "" 
        # Health Level to Override Motion : If specified, this object will start motion disabled. Once its health has dropped below this specified amount, it will enable motion.
        self.damagetoenablemotion = 0 
        # Physics Impact Force to Override Motion : If specified, this object will start motion disabled. Any impact that imparts a force greater than this value on the physbox will enable motion.
        self.forcetoenablemotion = 0 
        # Sound to make when punted : TODO: Replace this filler.
        self.puntsound = ""

        # Core Personality : Which personality VO set the core is set to.
        self.CoreType = 1 
        # Pause (in secs) between VO Lines. : When the core is talking, this is the number of seconds delay between it's spoken lines.
        self.DelayBetweenLines = "0.4" 

        self.auto_properties.extend(["targetname", "globalname", "angles", "model", "skin", "disableshadows", "targetname", "damagefilter", "disableshadows", "ExplodeDamage", "ExplodeRadius", "PerformanceMode", "spawnflags", "pressuredelay", "mindxlevel", "maxdxlevel", "fademindist", "fademaxdist", "fadescale", "spawnflags", "minhealthdmg", "shadowcastdist", "physdamagescale", "Damagetype", "nodamageforces", "inertiaScale", "massScale", "overridescript", "damagetoenablemotion", "forcetoenablemotion", "puntsound", "CoreType", "DelayBetweenLines"])


class PropPortal(Entity):
    """
    Auto-generated from portal.fgd, line 195.
    A portal
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "prop_portal", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.Activated = ""
        # TODO: Replace this filler. : TODO: Replace this filler.
        self.PortalTwo = ""
        # Portal pair ID that it belongs to : TODO: Replace this filler.
        self.LinkageGroupID = 0

        self.auto_properties.extend(["targetname", "angles", "Activated", "PortalTwo", "LinkageGroupID"])


class PropPortalStatsDisplay(Entity):
    """
    Auto-generated from portal.fgd, line 308.
    Portal Stats Display
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "prop_portal_stats_display", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Global Entity Name : Name by which this entity is linked to another entity in a different map. When the player transitions to a new map, entities in the new map with globalnames matching entities in the previous map will have the previous map's state copied over their state.
        self.globalname = "" 


        self.auto_properties.extend(["targetname", "angles", "parentname", "globalname"])


class PropTelescopicArm(Entity):
    """
    Auto-generated from portal.fgd, line 296.
    Telescopic Arm
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "prop_telescopic_arm", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # World Model : TODO: Replace this filler.
        self.model = ""
        # Skin : Some models have multiple versions of their textures, called skins. Set this to a number other than 0 to use that skin instead of the default.
        self.skin = 0 
        # Disable Shadows : Used to disable dynamic shadows on this entity.
        self.disableshadows = 0 


        self.auto_properties.extend(["targetname", "angles", "model", "skin", "disableshadows"])


class TriggerPortalCleanser(Entity):
    """
    Auto-generated from portal.fgd, line 98.
    A trigger volume that disolves any entities that touch it and fizzles active portals when the player touches it.
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "trigger_portal_cleanser", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Origin (X Y Z) : The position of this entity's center in the world. Rotating entities typically rotate around their origin.
        self.origin = ""

        # Start Disabled : TODO: Replace this filler.
        self.StartDisabled = 0 

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Origin (X Y Z) : The position of this entity's center in the world. Rotating entities typically rotate around their origin.
        self.origin = ""

        # Start Disabled : TODO: Replace this filler.
        self.StartDisabled = 0 

        # Global Entity Name : Name by which this entity is linked to another entity in a different map. When the player transitions to a new map, entities in the new map with globalnames matching entities in the previous map will have the previous map's state copied over their state.
        self.globalname = "" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Filter Name : Filter to use to see if activator triggers me. See filter_activator_name for more explanation.
        self.filtername = ""


        # Name : The name that other entities refer to this entity by.
        self.targetname = ""


        self.auto_properties.extend(["targetname", "parentname", "origin", "StartDisabled", "targetname", "parentname", "origin", "StartDisabled", "globalname", "spawnflags", "filtername", "targetname"])


class VguiNeurotoxinCountdown(Entity):
    """
    Auto-generated from portal.fgd, line 322.
    Neurotoxin Countdown
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "vgui_neurotoxin_countdown", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # Panel width : Width of the panel in units.
        self.width = 256 
        # Panel height : Height of the panel in units.
        self.height = 128 

        self.auto_properties.extend(["targetname", "angles", "parentname", "width", "height"])


class WeaponPortalgun(Entity):
    """
    Auto-generated from portal.fgd, line 217.
    Portalgun
    """
    def __init__(self, vmf_map):
        Entity.__init__(self, "weapon_portalgun", vmf_map)

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Pitch Yaw Roll (Y Z X) : This entity's orientation in the world. Pitch is rotation around the Y axis, 
        self.angles = "0 0 0" 

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.spawnflags = ""
        # Start Fade Dist/Pixels : Distance at which the prop starts to fade (<0 = use fademaxdist). If 'Screen Space Fade' is selected, this represents the number of pixels wide covered by the prop when it starts to fade.
        self.fademindist = -1 
        # End Fade Dist/Pixels : Maximum distance at which the prop is visible (0 = don't fade out). If 'Screen Space Fade' is selected, this represents the *minimum* number of pixels wide covered by the prop when it fades.
        self.fademaxdist = 0 
        # Fade Scale : If you specify a fade in the worldspawn, or if the engine is running under dx7, then the engine will forcibly fade out props even if fademindist/fademaxdist isn't specified.
        self.fadescale = 1 

        # Name : The name that other entities refer to this entity by.
        self.targetname = ""

        # Parent : The name of this entity's parent in the movement hierarchy. Entities with parents move with their parent.
        self.parentname = ""

        # TODO: Replace this filler. : TODO: Replace this filler.
        self.CanFirePortal1 = ""
        # TODO: Replace this filler. : TODO: Replace this filler.
        self.CanFirePortal2 = ""

        self.auto_properties.extend(["targetname", "angles", "spawnflags", "fademindist", "fademaxdist", "fadescale", "targetname", "parentname", "CanFirePortal1", "CanFirePortal2"])


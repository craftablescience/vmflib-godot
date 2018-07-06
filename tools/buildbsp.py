#! /usr/bin/env python3
"""

Utility for building a map using installed Source SDK tools.
Call with -h or --help to see usage information.

Examples:

  # Creates/installs/runs .bsp in same dir
  python buildbsp.py --game tf2 mymap.vmf
  
  # Creates/installs .bsp but does not run
  python buildbsp.py --game css --no-run mymap.vmf
  
  # Only create .bsp, and use fast config
  python buildbsp.py --game tf2 --no-run --no-install --fast mymap.vmf

"""
import argparse
import sys
import os
import subprocess
import webbrowser
import urllib.parse
import shutil


class Game:
    def __init__(self, id, dir, uses_sdk=False, rel_tools_path=os.path.join("..", "bin")):
        self.id = id              # Numeric Steam catalog ID number
        self.dir = dir            # Path to inner game directory (containing gameinfo.txt)
        self.uses_sdk = uses_sdk  # False if game ships with its own map compilers
        self.rel_tools_path = rel_tools_path

    def get_game_dir(self):
        """Returns joined game directory path relative to Steamapps"""
        subdir = "common"
        subsubdir = self.dir
        if WIN32 or CYGWIN:
            subsubdir = subsubdir.lower()
        return os.path.join(subdir, subsubdir)


WIN32 = sys.platform.startswith('win32')
CYGWIN = sys.platform.startswith('cygwin')
LINUX = sys.platform.startswith('linux')
DARWIN = False  # Not supported yet

# Information for commented out entries came from a (non-comprehensive) list of source engine games
# TODO: Extract to external file; add more information
GAMES = {
    'hl2': Game(220, os.path.join("Half-Life 2", "hl2")),
    'css': Game(240, os.path.join("Counter-Strike Source", "cstrike")),
    'hls': Game(280, os.path.join("Half-Life 2", 'hl1')),  # Half-Life: Source
    'dod': Game(300, os.path.join("Day of Defeat Source", "dod")),
    'hl2mp': Game(320, os.path.join("Half-Life 2 Deathmatch", "hl2mp")),
    'hl2ep1': Game(380, os.path.join("Half-Life 2", 'episodic')),  # Half-Life 2: Episode One
    'portal': Game(400, os.path.join('Portal', 'portal')),
    'hl2ep2': Game(420, os.path.join("Half-Life 2", 'ep2')),  # Half-Life 2: Episode Two
    'tf2': Game(440, os.path.join("Team Fortress 2", "tf")),
    'l4d': Game(500, os.path.join('left 4 dead', 'left4dead'), uses_sdk=True), # Left 4 Dead # TODO TEST GAME
    'l4d2': Game(550, os.path.join('Left 4 Dead 2', 'left4dead2'), uses_sdk=True), # Left 4 Dead 2 # TODO TEST GAME
    # '': Game(570, os.path.join('', ''), uses_sdk=?), # Dota 2
    'portal2': Game(620, os.path.join('Portal 2', 'portal2')),
    'as': Game(630, os.path.join('Alien Swarm', 'swarm'), uses_sdk=True), # Alien Swarm # has its own sdk
    'csgo': Game(730, os.path.join('Counter-Strike Global Offensive', 'csgo'), uses_sdk=True), # Counter-Strike: Global Offensive
    # '': Game(1300, os.path.join('', ''), uses_sdk=?), # SiN Episodes: Emergence
    # '': Game(2100, os.path.join('', ''), uses_sdk=?), # Dark Messiah of Might & Magic Single Player
    'ship': Game(2400, os.path.join('The Ship', 'ship'), uses_sdk=True), # The Ship # TODO TEST GAME seems to require external SDK
    # '': Game(2450, os.path.join('', ''), uses_sdk=?), # Bloody Good Time
    # '': Game(2600, os.path.join('', ''), uses_sdk=?), # Vampire: The Masquerade - Bloodlines
    'gm': Game(4000, os.path.join("GarrysMod", "garrysmod")),
    # '': Game(4920, os.path.join('', ''), uses_sdk=?), # Natural Selection 2
    # '': Game(10220, os.path.join('', ''), uses_sdk=?), # Postal 3
    'pvk2': Game(17570, os.path.join('pirates, vikings and knights ii', 'pvkii'), rel_tools_path=os.path.join("..", "sdkbase_pvkii", "bin")), # Pirates
    'dys': Game(17580, os.path.join('Dystopia', 'dystopia'), uses_sdk=True), # Dystopia
    # '': Game(17710, os.path.join('', ''), uses_sdk=?), # Nuclear Dawn
    'emp': Game(17740, os.path.join('Empires', 'empires')),
    # '': Game(22200, os.path.join('', ''), uses_sdk=?), # Zeno Clash
    # '': Game(1309, os.path.join('', ''), uses_sdk=?), # SiN Multiplayer
    # '': Game(1313, os.path.join('', ''), uses_sdk=?), # SiN
    # '': Game(2130, os.path.join('', ''), uses_sdk=?), # Dark Messiah of Might & Magic Multi-Player
    # '': Game(4932, os.path.join('', ''), uses_sdk=?), # Natural Selection 2 - Deluxe DLC
    # '': Game(51100, os.path.join('', ''), uses_sdk=?), # Tactical Intervention (No longer available)
    # '': Game(52003, os.path.join('', ''), uses_sdk=?), # Mac Portal
    # '': Game(70000, os.path.join('', ''), uses_sdk=?), # Dino D-Day
    # '': Game(91700, os.path.join('', ''), uses_sdk=?), # E.Y.E: Divine Cybermancy
    # '': Game(201070, os.path.join('', ''), uses_sdk=?), # Revelations 2012
    # '': Game(203810, os.path.join('', ''), uses_sdk=?), # Dear Esther
    # '': Game(212160, os.path.join('', ''), uses_sdk=?), # Vindictus
    # The stanley parable works, kind of. I'm not sure why you would want to make a map for it, though.
    'sp': Game(221910, os.path.join('The Stanley Parable', 'thestanleyparable'), uses_sdk=True),  # The Stanley Parable
    # '': Game(222880, os.path.join('', ''), uses_sdk=?), # Insurgency
    'nmrih': Game(224260, os.path.join('nmrih', 'nmrih'), rel_tools_path=os.path.join("..", "sdk", "bin")), # No More Room in Hell
    # '': Game(225600, os.path.join('', ''), uses_sdk=?), # Blade Symphony
    # '': Game(238430, os.path.join('', ''), uses_sdk=?), # Contagion
    'nt': Game(244630, os.path.join('NEOTOKYO', 'NeotokyoSource'), uses_sdk=True), # NEOTOKYO° # TODO TEST GAME
    # '': Game(247120, os.path.join('', ''), uses_sdk=?), # Portal 2 Sixense Perceptual Pack
    # '': Game(251110, os.path.join('', ''), uses_sdk=?), # INFRA
    # '': Game(264240, os.path.join('', ''), uses_sdk=?), # CONSORTIUM
    'fof': Game(265630, os.path.join('Fistful of Frags', 'fof'), rel_tools_path=os.path.join("..", "sdk", "bin")), # Fistful of Frags
    # '': Game(266430, os.path.join('', ''), uses_sdk=?), # Anarchy Arcade
    # '': Game(302810, os.path.join('', ''), uses_sdk=?), # Divinia Chronicles: Relics of Gan-Ti
    # '': Game(310110, os.path.join('', ''), uses_sdk=?), # NS2: Combat
    'dab': Game(317360, os.path.join('Double Action', 'dab')), # Double Action: Boogaloo
    'cure': Game(355180, os.path.join('Codename CURE', 'cure')), # Codename CURE
    'bms': Game(362890, os.path.join('Black Mesa', 'bms')), # Black Mesa
    'te120': Game(365300, os.path.join('Transmissions Element 120', 'te120')), # Transmissions: Element 120
    # '': Game(399120, os.path.join('', ''), uses_sdk=?), # Prospekt
    # '': Game(447820, os.path.join('', ''), uses_sdk=?), # Day of Infamy


}

def _make_arg_parser():
    parser = argparse.ArgumentParser(description='Build, install, and test a VMF map.')
    parser.add_argument('map')
    parser.add_argument('-g', '--game', default='hl2', choices=GAMES.keys(),
        help="selects which game to use")
    parser.add_argument('--no-run', action="store_true",
        help="don't run the game after building/installing")
    parser.add_argument('--no-install', action="store_true",
        help="don't install (or run) the map after building")
    parser.add_argument('-f', '--fast', action="store_true",
        help="enable fast compile options")
    parser.add_argument('--hdr', action="store_true",
        help="enable full HDR compile")
    parser.add_argument('--final', action="store_true",
        help="use with --hdr for slow high-quality HDR compile")
    parser.add_argument('-p', '--steam-windows-path',
        help="path to your (Windows) Steam folder")
    parser.add_argument('--source-sdk-path',
                        help="path to your sourceSDK folder")
    # parser.add_argument('--username',
    #    help="your Steam username (needed for some games)") # Not recently

    return parser


def main():
    parser = _make_arg_parser()
    args = parser.parse_args()
    game = GAMES[args.game]
    #username = args.username  # May be None
    vmf_file = os.path.abspath(args.map)
    path, filename = os.path.split(vmf_file)
    mapname = filename[:-4]
    mappath = os.path.join(path, mapname)
    bsp_file = os.path.join(path, mapname + ".bsp")
    sourcesdk = args.source_sdk_path
    winsteam = args.steam_windows_path
    if not winsteam:
        winsteam = os.getenv('winsteam')

    # We need to find out where the SteamApps directory is.
    if winsteam:
        steamapps = os.path.join(winsteam, "Steamapps")
        if not os.path.isdir(steamapps):  # Try lowercase
            steamapps = os.path.join(winsteam, "steamapps")
        if not os.path.isdir(steamapps):
            raise Exception(
                "The provided Steam directory does not contain a Steamapps directory: %s" %
                os.path.abspath(winsteam)
            )
    elif WIN32 or CYGWIN:
        if not sourcesdk:
            sourcesdk = os.getenv('sourcesdk')
        if CYGWIN:
            def cygwin2dos(path):
                return subprocess.check_output(["cygpath", '-w', '%s' % path], universal_newlines=True).strip()
            sourcesdk = subprocess.check_output(["cygpath", sourcesdk], universal_newlines=True).strip()
        sourcesdk = os.path.abspath(sourcesdk)
        steamapps = os.path.dirname(os.path.dirname(sourcesdk))
        if not os.path.isdir(steamapps):
            raise Exception("Steamapps directory could not be found. Please specify using -p or see --help.")
        # if not username:
        #    username = os.path.basename(os.path.dirname(sourcesdk))
    else:
        raise Exception("Unable to determine where your (Windows) Steam installation is located. See --help.")
    steamapps = os.path.abspath(steamapps)

    # Prepare some useful paths
    gamedir = os.path.join(steamapps, game.get_game_dir())
    mapsdir = os.path.join(gamedir, "maps")

    # If the gamedir doesn't exist, then we have a problem.
    if not os.path.exists(gamedir):
        raise Exception("Game directory does not exist: %s. Please ensure that the game is installed and that"
                        " the -p argument is correct." % gamedir)

    # If the mapsdir doesn't exist, but the gamedir does, then the /maps/ folder is missing, which is easily fixed.
    if not os.path.exists(mapsdir):
        os.makedirs(mapsdir)

    # Get path to correct bin tools directory (game or SDK)
    if game.uses_sdk:
        if not sourcesdk:
            # Try finding SDK within Steamapps
            # TODO
            raise Exception("Could not locate sourcesdk folder. Please specify using --source-sdk-path")
        toolsdir = os.path.join(sourcesdk, "bin", "orangebox", "bin")
    else:
        toolsdir = os.path.abspath(os.path.join(gamedir, game.rel_tools_path))

    # Make sure gamedir path seems legit
    if not os.path.isfile(os.path.join(gamedir, "gameinfo.txt")):
        raise Exception("Game directory does not contain a gameinfo.txt: %s" % gamedir)

    if WIN32 or CYGWIN:
        # Convert some paths if using Cygwin
        if CYGWIN:
            gamedir = cygwin2dos(gamedir)
            mappath = cygwin2dos(mappath)

        # Change working directory first because VBSP is dumb
        # os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))

        # Run the SDK tools
        vbsp_exe = os.path.join(toolsdir, "vbsp.exe")
        print(vbsp_exe)
        code = subprocess.call([vbsp_exe, '-game', gamedir, mappath])
        print("VBSP finished with status %s." % code)

        if code != 0:
            if code == 1:
                print("Looks like SteamService isn't working. Try reopening Steam.")
            elif code == -11:
                print("Looks like you might have gotten the 'material not found' " +
                    "error messages. Try signing into Steam, or restarting it " +
                    "and signing in.")
            else:
                print("Looks like VBSP crashed, but I'm not sure why.")
            exit(code)

        vvis_exe = os.path.join(toolsdir, "vvis.exe")
        opts = [vvis_exe]
        if args.fast:
            opts.append('-fast')
        opts.extend(['-game', gamedir, mappath])
        subprocess.call(opts)

        vrad_exe = os.path.join(toolsdir, "vrad.exe")
        opts = [vrad_exe]
        if args.fast:
            opts.extend(['-bounce', '2', '-noextra'])
        if args.hdr:
            opts.append('-both')
        if args.hdr and args.final:
            opts.append('-final')
        opts.extend(['-game', gamedir, mappath])
        subprocess.call(opts)

        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            print("Copying map %s to %s" % (mapname, mapsdir))
            shutil.copy(bsp_file, mapsdir)
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % mapname)
            run_url = "steam://run/%d//%s" % (game.id, params)
            print(run_url)
            webbrowser.open(run_url)
            if CYGWIN:
                print("\nYou're running cygwin, so I can't launch the game for you.")
                print("Double-click the URL above, right-click, and click 'Open'.")
                print("Or paste the URL above into the Windows 'Run...' dialog.")
                print("Or, just run 'map %s' in the in-game console." % mapname)
        else:
            print("Not launching game")
    elif LINUX:
        # Environment to use with wine calls
        env = os.environ.copy()
        env['WINEPREFIX'] = os.path.expanduser("~/.winesteam")
        
        # Define path-converting helper function
        def unix2wine(path):
            return subprocess.check_output(["winepath", '-w', '%s' % path], env=env).strip()
        
        # Wine-ify some of our paths
        gamedir = unix2wine(gamedir)
        mappath = unix2wine(mappath)

        # Tell wine to look for DLLs here
        #env['WINEDLLPATH'] = os.path.join(sourcesdk, "bin")
        
        #print("WINEDLLPATH is as follows: ", env['WINEDLLPATH'])

        # Use native maps directory instead of the Wine installation's
        mapsdir = os.path.join('~', '.steam', 'steam', 'SteamApps', game.get_game_dir(), "maps")
        mapsdir = os.path.expanduser(mapsdir)

        # Change working directory first because VBSP is dumb
        #os.chdir(os.path.join(sourcesdk, 'bin', 'orangebox'))
        
        print("Using -game dir: %s" % gamedir)
        
        # We now need to set the VPROJECT env variable
        env['VPROJECT'] = gamedir

        # Run the SDK tools
        vbsp_exe = os.path.join(toolsdir, "vbsp.exe")
        code = subprocess.call(['wine', vbsp_exe, '-game', gamedir, mappath], env=env)
        print("VBSP finished with status %s." % code)

        # Handle various exit status codes VBPS may have returned
        if code != 0:
            if code == 1:
                print("\nLooks like VBSP crashed, possibly due to invalid geometry in the map. Check the output above.")
                print("\It could also be related to SteamService isn't working. Try re(launching) wine's Steam:")
                steambin = os.path.join(os.path.dirname(steamapps), 'steam.exe')
                print('\nWINEPREFIX="%s" wine "%s" -no-dwrite' % (env['WINEPREFIX'], steambin))
            elif code == -11:
                print("\nLooks like you might have gotten the 'material not found' " +
                    "error messages. Try signing into Steam, or restarting it " +
                    "and signing in.")
            else:
                print("\nLooks like VBSP crashed, but I'm not sure why.")
            exit(code)

        vvis_exe = os.path.join(toolsdir, "vvis.exe")
        opts = ['wine', vvis_exe]
        if args.fast:
            opts.append('-fast')
        opts.extend(['-game', gamedir, mappath])
        code = subprocess.call(opts, env=env)

        if code != 0:
            print("\nLooks like VVIS crashed, but I'm not sure why.")
            exit(code)

        vrad_exe = os.path.join(toolsdir, "vrad.exe")
        opts = ['wine', vrad_exe]
        if args.fast:
            opts.extend(['-bounce', '2', '-noextra'])
        if args.hdr:
            opts.append('-both')
        if args.hdr and args.final:
            opts.append('-final')
        opts.extend(['-game', gamedir, mappath])
        code = subprocess.call(opts, env=env)
        
        if code != 0:
            print("\nLooks like VRAD crashed, but I'm not sure why.")
            exit(code)

        # Install the map to the game's map directory (unless --no-install)
        if not args.no_install:
            shutil.copy(bsp_file, mapsdir)
        else:
            print("Not installing map")

        # Launch the game (unless --no-run or --no-install)
        if not args.no_run and not args.no_install:
            params = urllib.parse.quote("-dev -console -allowdebug +map %s" % mapname)
            run_url = "steam://run/%d//%s" % (game.id, params)
            print(run_url)
            webbrowser.open(run_url)
        else:
            print("Not launching game")
    else:
        raise OSError('Your OS is not supported yet!')

if __name__ == '__main__':
    main()

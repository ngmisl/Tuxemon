Tuxemon 0.4.34
==============

Tuxemon is a free, open source monster-fighting RPG.  It's in constant
development and improving all the time!  Contributors of all skill and level
are welcome to join.

[![Build Status](https://travis-ci.org/Tuxemon/Tuxemon.svg?branch=development)](https://travis-ci.org/Tuxemon/Tuxemon)
[![Documentation Status](https://readthedocs.org/projects/tuxemon/badge/?version=latest)](https://tuxemon.readthedocs.io/en/latest/?badge=latest)

![screenshot](https://www.tuxemon.org/images/featurette-01.png)


Features
--------

- Game data is all json, easy to modify and extend
- Game maps are created using the Tiled Map Editor
- Simple game script to write the story
- Dialogs, interactions on map, npc scripting
- Localized in several languages
- Seamless keyboard, mouse, and gamepad input
- Animated maps
- Lots of documentation
- Python code can be modified without a compiler
- CLI interface for live game debugging
- Runs on Windows, Linux, OS X, and some support on Android
- 183 monsters with sprites
- 98 techniques to use in battle
- 221 NPC sprites
- 18 items


Installation
------------

If you want to try the game, it's recommended to download and try the
development branch first. The master branch be stable, but is often out
of date.


**Windows Source**

Install the latest version of python 3 from
[here](https://www.python.org/downloads/)

Run:

```cmd
git clone https://github.com/Tuxemon/Tuxemon.git
cd Tuxemon
python -m pip install -U -r requirements.txt
python run_tuxemon.py
```

**Windows Binary**

Check the [release page](https://github.com/Tuxemon/Tuxemon/releases) 
for binaries.

**Ubuntu**

```sh
sudo apt install python python-pygame python-pip python-imaging git
git clone https://github.com/Tuxemon/Tuxemon.git
cd Tuxemon
sudo pip install -U -r requirements.txt
python run_tuxemon.py
```

**Ubuntu 18.04 w/venv**

Use this if you don't want to modify your system packages
```sh
sudo apt install git python3-venv
git clone https://github.com/Tuxemon/Tuxemon.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run_tuxemon.py
```

**Debian**

```sh
sudo apt-get install python python-pygame python-pip python-imaging git
git clone https://github.com/Tuxemon/Tuxemon.git
cd Tuxemon
sudo pip install -U -r requirements.txt
python run_tuxemon.py
```

*Optional rumble support*

```sh
sudo apt install build-essential
git clone https://github.com/zear/libShake.git
cd libShake/
make BACKEND=LINUX; sudo make install BACKEND=LINUX
```

**Mac OS X (Yosemite)**

```sh
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew tap Homebrew/python
brew update
brew install python
brew install sdl sdl_image sdl_ttf portmidi git
brew install sdl_mixer --with-libvorbis
sudo pip install git+https://github.com/pygame/pygame.git
sudo pip install -U -r requirements.txt 
git clone https://github.com/Tuxemon/Tuxemon.git
ulimit -n 10000; python run_tuxemon.py
```

**Arch Linux**

Tuxemon is available in the
[AUR](https://aur.archlinux.org/packages/tuxemon-git/).

**Smartphones**

Android builds are highly experimental.  Download and install the apk
from the [releases page](https://github.com/Tuxemon/Tuxemon/releases)
and install to your device.  You will need to manually install the mods
folder.  Connect your device to your computer and make a folder called
"Tuxemon" in "Internal Storage", then copy the mods folder.  Tuxemon
will also need file system permissions, which you can set in your phones
settings.

**Fedora Linux**

```
sudo dnf install SDL*-devel freetype-devel libjpeg-devel portmidi-devel
python3-devel virtualenv venv
pip install -r requirements.txt
```


Controls
--------

##### Game Controls
###### You can also set your own inputs in the options menu or cfg file
* *Arrow Keys* - Movement
* *Enter* - Select/activate
* *ESC* - Menu/Cancel
* *Shift* - Sprint

##### Debugging
These are enabled when "dev_tools = True" in the config 
* *r* - Reload the map tiles
* *n* - No clip

##### Map Editor

Use *Tiled* map editor: http://www.mapeditor.org/


CLI Interface
--------------

The CLI interface is a very convenient way to debug and develop your
maps. After you enable the CLI interface, you can use the terminal to
enter commands.  You could, for example, give your self potions to
battle, or add a monster directly to your party.  It's also possible to
change game variables directly.  In fact, any action or condition that
is usable in the map can be used with the CLI interface,

**Setting up**

You can enable cli by changing `cli_enabled` to `True` in the
`tuxemon.cfg` file:

```
[game]
cli_enabled = True
```

**Commands**

- `help [command_name]` — Lists all commands, or specific information on a command.
- `action <action_name> [params]` — Execute EventAction.  Uses same syntax as the map script.
- `test <condition_name> [params]` — Test EventCondition.  Uses same systax as the map script.
- `random_encounter` — Sets you in a wild tuxemon battle, similar to walking in tall grass.
- `trainer_battle <npc_slug>` — Sets you in a trainer battle with specified npc.
- `quit` — Quits the game.
- `whereami` — Prints out the map filename
- `shell` — Starts the python shell, that you can use to modify the game directly. For advanced users.

**CLI Examples**

Get Commands

```
> help
Available Options
=================
action  help  quit  random_encounter  shell  test  trainer_battle  whereami

Enter 'help [command]' for more info.
```

Get help on an action

```
> help action teleport

    Teleport the player to a particular map and tile coordinates.

    Script usage:
        .. code-block::

            teleport <map_name>,<x>,<y>

    Script parameters:
        map_name: Name of the map to teleport to.
        x: X coordinate of the map to teleport to.
        y: Y coordinate of the map to teleport to.
```

Test and give an item
```
> test has_item player,potion
False
> action add_item potion,1
> test has_item player,potion
True
```

**NOTE!**  The CLI interface is new and the error messages are not very
helpful. In general, you should be using the commands when the game is playing,
and you are on the world map.


Check out the 
[scripting reference](https://tuxemon.readthedocs.io/en/latest/handcrafted/scripting.html) 
for all the available actions and conditions for use with `action` and `test`!


Building
--------

There are many scripts for various builds in the buildconfig folder. 
These are meant to be run from the project root directory, for example,
to build the portable pypy build:

```
[user@localhost Tuxemon]$ buildconfig/build_pypy_portable_linux.sh
```

There will be a new directory called build, which will have the package
if everything was successful.

WARNING!  The build scripts are designed to be run in a dedicated VM.  They
will add and remove packages and could leave you OS in a bad state.  You
should not use them on your personal computer.  Use in a vm or container.


License
-------

With the exception of the lib folder which may have its own license, all
code in this project is licenced under the GPLv3.

GPL v3+

Copyright (C) 2017 William Edwards <shadowapex@gmail.com>,     
Benjamin Bean <superman2k5@gmail.com>

This software is distributed under the GNU General Public Licence as published
by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.  See the file [LICENSE](LICENSE) for the conditions
under which this software is made available.  Tuxemon also contains code from
other sources.


External links
--------------

* Official website: [tuxemon.org](https://www.tuxemon.org)
* Official forum: [forum.tuxemon.org](https://forum.tuxemon.org/)
* Matrix: [Tuxemon](https://matrix.to/#/!ktrcrHpgkDOGCQOlxX:matrix.org)
* Discord: [Tuxemon](https://discord.gg/3ZffZwz)
* Reddit: [/r/Tuxemon](https://www.reddit.com/r/tuxemon)
* YouTube: [Tuxemon](https://www.youtube.com/channel/UC6BJ6H7dB2Dpb8wzcYhDU3w)
* Readthedocs: https://tuxemon.readthedocs.io/en/latest/

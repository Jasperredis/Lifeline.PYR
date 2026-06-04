# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR -- A retro-style arcade game made by jasperredis.
# Copyright (C) 2025  jasperredis

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

# Lifeline.PYR v1.0

# Import libraries
from cerbose import cprint
import pygame as pg

# Core modules
import mod.core.assets as ast
from mod.core.save import S

# Other modules
import mod.etc.BTXT as B

# Initialise
pg.mixer.init()

MUSIC = ast.ASSETS['music/main']
CURRENT = ""

MUSIC_DATA = {
    1: {
        "title": "main",
        "options": "options",
        "game": "game_a",
        "about": "main",
        "howtoplay": "main",
        "updates": "main",
        "begin": None,
        "tips": "bonus",
    },
    2: {
        "title": "main",
        "options": "options",
        "game": "game_b",
        "about": "main",
        "howtoplay": "main",
        "updates": "main",
        "begin": None,
        "tips": "bonus",
    },
    3: {
        "title": "main",
        "options": "options",
        "game": "bonus",
        "about": "main",
        "howtoplay": "main",
        "updates": "main",
        "begin": None,
        "tips": "bonus",
    },
    4: {
        "title": "main_alt",
        "options": "main_alt",
        "game": "game_alt",
        "about": "main_alt",
        "howtoplay": "main_alt",
        "updates": "main_alt",
        "begin": None,
        "tips": "main_alt",
    },
    5: {
        "title": "main_Lifeline.py",
        "options": "main_Lifeline.py",
        "game": "gameplay_Lifeline.py",
        "about": "main_Lifeline.py",
        "howtoplay": "main_Lifeline.py",
        "updates": "main_Lifeline.py",
        "begin": None,
        "tips": "main_Lifeline.py",
    }
}

def switch_music(stage):
    """
    The name is self-explanatory. Arguments:
    - stage (str): The stage it currently is; determines the track.
    """
    global CURRENT, MUSIC, MUSIC_DATA

    stage_val = MUSIC_DATA[S['ost']][stage]
    track_name = stage_val() if callable(stage_val) else stage_val

    if track_name != CURRENT:
        music_temp = f"music/{track_name}"
        if music_temp in ast.ASSETS:
            MUSIC.stop()
            MUSIC = ast.ASSETS[music_temp]
            CURRENT = track_name
            if CURRENT != None:
                MUSIC.play(loops=-1)
        else:
            cprint("error", f"Track for {stage} does not exist.")
            B.BTX = f"Track for \"{stage}\" does not exist!"

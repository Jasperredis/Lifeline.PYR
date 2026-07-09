# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.0.1

from cerbose import cprint
import pygame as pg
import mod.core.assets as ast
from mod.core.save import S
import mod.etc.BTXT as B

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

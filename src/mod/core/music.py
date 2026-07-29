# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

from cerbose import cprint
import pygame as pg
import mod.core.assets as ast
from mod.core.save import save_data
import mod.etc.BTXT as B

pg.mixer.init()

music = ast.assets_data['music/main']
current = ""

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
    global current, music

    stage_val = MUSIC_DATA[save_data['ost']][stage]
    track_name = stage_val() if callable(stage_val) else stage_val

    if track_name != current:
        music_temp = f"music/{track_name}"
        if music_temp in ast.assets_data:
            music.stop()
            music = ast.assets_data[music_temp]
            current = track_name
            if current is not None:
                music.play(loops=-1)
        else:
            cprint("error", f"Track for {stage} does not exist.")
            B.bottom_text = f"Track for \"{stage}\" does not exist!"

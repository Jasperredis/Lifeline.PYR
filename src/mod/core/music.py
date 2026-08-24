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
        "keybindings": "options",
        "game_1d": "game_a",
        "game_2d": "game_a",
        "game_sel": "main",
        "license": "main",
        "begin": None,
    },
    2: {
        "title": "main",
        "options": "options",
        "keybindings": "options",
        "game_1d": "game_b",
        "game_2d": "game_b",
        "game_sel": "main",
        "license": "main",
        "begin": None,
    },
    3: {
        "title": "main",
        "options": "options",
        "keybindings": "options",
        "game_1d": "bonus",
        "game_2d": "bonus",
        "game_sel": "main",
        "license": "main",
        "begin": None,
    },
    4: {
        "title": "main_Lifeline.py",
        "options": "main_Lifeline.py",
        "keybindings": "main_Lifeline.py",
        "game_1d": "gameplay_Lifeline.py",
        "game_2d": "gameplay_Lifeline.py",
        "game_sel": "main_Lifeline.py",
        "license": "main_Lifeline.py",
        "begin": None,
    },
    5: {
        "title": None,
        "options": None,
        "keybindings": None,
        "game_sel": None,
        "game_1d": None,
        "game_2d": None,
        "license": None,
        "begin": None
    }
}


def switch_music(stage):
    global current, music

    stage_val = MUSIC_DATA[save_data['ost']][stage]
    track_name = stage_val() if callable(stage_val) else stage_val

    if track_name is None:
        music.stop()
        return
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

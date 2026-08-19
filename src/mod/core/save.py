# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

from cerbose import cprint
from datetime import datetime
import pygame as pg
import json
import os
import mod.etc.BTXT as B

DEFAULT_SAVE = {
    "bg": 1,
    "dif": 1,
    "fullscreen": False,
    "high": 0,
    "htp-theme": 1,
    "indicators": True,
    "inertia": True,
    "keybindings": {
        "game-1d-jump": "w",
        "game-1d-slow": "s",
        "game-2d-jump": "UP",
        "game-2d-move-down": "s",
        "game-2d-move-up": "w",
        "game-2d-slow": "DOWN",
        "game-dash": "e",
        "game-move-left": "a",
        "game-move-right": "d",
        "game-pause": "ESCAPE",
        "menu-decrease": "LEFT",
        "menu-down": "DOWN",
        "menu-exit": "x",
        "menu-increase": "RIGHT",
        "menu-left": "LEFT",
        "menu-right": "RIGHT",
        "menu-up": "UP",
        "screenshot": "F2"
    },
    "life-tick-sound": False,
    "mouse-move": False,
    "mouse-nav": True,
    "mouse-theme": 1,
    "notifs": True,
    "ost": 1,
    "palette": 1,
    "played": 0,
    "seen_begin": False,
    "seenup": False,
    "total": 0,
    "velocity-icon": False,
    "winscale": 4,
}

cprint("proc", "Loading save...")
try:
    with open('save.json', 'r') as f:  # Read and parse save.json
        save_data = json.load(f)  # Save data variable!!!
    cprint("ok", "Loaded save!")
except FileNotFoundError:  # Write new save if save is not found
    with open('save.json', 'w') as f:
        json.dump(DEFAULT_SAVE, f)
    save_data = DEFAULT_SAVE
    cprint("info", "Save not found; Wrote new save.")


def write_save(save_data):  # Write the save to save.json
    cprint("proc", "Writing save...")
    time = datetime.now()
    try:
        with open('save.json', 'w') as f:
            json.dump(save_data, f)
        cprint("ok", "Wrote save!")
        B.bottom_text = \
            f"Updated save at {time.hour}:{time.minute}:{time.second}."

    except Exception as e:
        ERROR_MSG = f"""
=== SAVE ERROR AT {time.hour}:{time.minute}:{time.second} ===
Could not write save because of an unknown error:\n{e}\n
Below is the save that would have been writen:\n{save_data}\n
        """
        B.bottom_text = "Save failure; see logs/errors.txt."
        with open(os.path.join("logs", "errors.txt"), 'a') as f:
            f.write(ERROR_MSG)


def keyb(keys, key):
    return keys[pg.key.key_code(save_data["keybindings"][key])]

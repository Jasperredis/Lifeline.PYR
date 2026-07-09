# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.0.1

from mod.core.save import S
from mod.stage.game.game import constants

GAMEDATA = {}

def init(tick):
    global GAMEDATA
    constants.do_depend()
    GAMEDATA = {
        "plrx": 126, # player x pos
        "plry": 64,
        "life": 5,
        "last_loss": 0,
        "enemies": [],
        "heals": [],
        "paused": False,
        "sel": 1, # selected pause option
        "lkpt": 0, # last key press time
        "iframe": 0, # invincibility frame
        "last_iframe_time": 0,
        "score": 0,
        "gameover": False,
        "jumping": False,
        "last_jump": -300,
        "initial_high": S["high"],
        "velocity": 3,
        "velocity_y": 3,
        "falls": [],
        "dash": 106,
        "start_tick": tick,
        "lasers": []
    }
    S["played"] += 1

    # my cat typed the garbled part of the line below
    # print("log init gdata78u9-06=4wsa6.789-0078-9564444444444444444444444444444444444444444444444x21q   ")

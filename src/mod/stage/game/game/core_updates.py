# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import mod.core.assets as ast
from mod.core.save import S, wr
import mod.etc.etcils as etc
from mod.stage.game.game import constants as con

def do_updates(rsurface, tick, GAMEDATA):
    if not GAMEDATA["paused"]:
        # Deplete life and add score
        if tick - GAMEDATA["last_loss"] >= con.life_depletion_time:
            GAMEDATA["last_loss"] = tick
            GAMEDATA["life"] -= 1
            if not GAMEDATA["gameover"]: # Score
                GAMEDATA["score"] += con.score_increment
                S["total"] += con.score_increment
                # Handle highscore
                if GAMEDATA["score"] > S["high"]:
                    S["high"] = GAMEDATA["score"]

        # Handle game over
        if GAMEDATA["life"] <= 0 and not GAMEDATA["gameover"]:
            wr(S)  # Update save
            GAMEDATA["gameover"] = True  # Enable flag
            ast.ASSETS["gameaud/gameover"].play()

        # Handle iframes
        if GAMEDATA["iframe"]:
            if tick - GAMEDATA["last_iframe_time"] >= con.iframe_end_time:
                GAMEDATA["iframe"] = False
            else:
                rsurface.blit(
                    ast.ASSETS["game/iframe"],
                    (etc.centrexy(ast.ASSETS["game/iframe"], onecoord="x"), 1),
                )

    # Ensure correct life ticking
    else:
            GAMEDATA["last_loss"] += 1

    return GAMEDATA

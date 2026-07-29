# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import mod.core.assets as ast
from mod.core.save import save_data, write_save
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
                save_data["total"] += con.score_increment
                # Handle highscore
                if GAMEDATA["score"] > save_data["high"]:
                    save_data["high"] = GAMEDATA["score"]

        # Handle game over
        if GAMEDATA["life"] <= 0 and not GAMEDATA["gameover"]:
            write_save(save_data)  # Update save
            GAMEDATA["gameover"] = True  # Enable flag
            ast.assets_data["gameaud/gameover"].play()

        # Handle iframes
        if GAMEDATA["iframe"]:
            if tick - GAMEDATA["last_iframe_time"] >= con.iframe_end_time:
                GAMEDATA["iframe"] = False
            else:
                rsurface.blit(
                    ast.assets_data["game/iframe"],
                    (etc.centrexy(ast.assets_data["game/iframe"], onecoord="x"), 1),
                )

    # Ensure correct life ticking
    else:
            GAMEDATA["last_loss"] += 1

    return GAMEDATA

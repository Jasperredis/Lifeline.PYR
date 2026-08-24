# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev
# This is FREE SOFTWARE. See the LICENSE-GPL file for more information.

import mod.core.assets as ast
from mod.core.save import save_data, write_save
import mod.etc.etcils as etc
from mod.stage.game import constants as con
from mod.stage.game.ui import draw_notif


def do_updates(rsurface, tick, game):
    if not game.paused:
        # Deplete life and add score
        depletion_time = con.life_depletion_time if save_data["dif"] != 4 \
            else con.life_depletion_time_intense
        if tick - game.last_loss >= depletion_time:
            game.last_loss = tick
            game.life -= 1
            if not game.gameover:  # Score
                game.score += con.score_increment
                save_data["total"] += con.score_increment
                draw_notif(rsurface, "50_pts", tick, game)
                if save_data["life-tick-sound"]:
                    ast.assets_data["gameaud/tick"].play()
        # Handle game over
        if game.life <= 0 and not game.gameover:
            game.score *= con.score_multipliers[save_data["dif"]]
            game.score = int(game.score)
            game.gameover = True  # Enable flag
            ast.assets_data["gameaud/gameover"].play()
            # Handle highscore
            if game.score > save_data["high"]:
                save_data["high"] = game.score
            write_save(save_data)  # Update save
        # Handle iframes
        if game.iframe:
            if tick - game.last_iframe_time >= con.iframe_end_time:
                game.iframe = False
            else:
                rsurface.blit(
                    ast.assets_data["game/iframe"],
                    (etc.centrexy(ast.assets_data["game/iframe"],
                                  onecoord="x"), 1),
                )
    else:  # Correct life ticking for time paused
        game.last_loss += 1
    return game

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

# Lifeline.PYR v1.0.1.1

# Core modules
import mod.core.assets as ast
from mod.core.save import S, wr

# Other module
import mod.etc.etcils as etc

# Game module
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

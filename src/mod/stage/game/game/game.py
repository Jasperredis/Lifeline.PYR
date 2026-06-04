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

# Import libraries
import pygame as pg

# Game modules
from mod.stage.game.game.ui import draw_ui, draw_ui_before_entities
from mod.stage.game.game.spawns import do_spawns
from mod.stage.game.game.core_updates import do_updates
from mod.stage.game.game.inputx import take_input
from mod.stage.game.game.pause import do_pause
from mod.stage.game.game import gamedata
from mod.stage.game.game import player

started = False

def ACT(rsurface, keys, tick, mx, my, mb):
    global started

    # Initialise gamedata
    if not started:
        gamedata.init(tick)
        started = True

    # Act
    draw_ui_before_entities(rsurface)
    player.make_player(rsurface, gamedata.GAMEDATA, tick, keys)
    draw_ui(rsurface, gamedata.GAMEDATA, tick, keys)
    gamedata.GAMEDATA = do_spawns(rsurface, player.plr, gamedata.GAMEDATA, tick)

    # inputx
    inputx_result = take_input(gamedata.GAMEDATA, keys, tick, mx, my, mb)
    gamedata.GAMEDATA = inputx_result[0]
    if inputx_result[1] == "restart":
        gamedata.init(tick)

    gamedata.GAMEDATA = do_updates(rsurface, tick, gamedata.GAMEDATA)

    # Pause and determine return
    if not gamedata.GAMEDATA["paused"]:
        return "game"

    final_return = do_pause(rsurface, keys, tick, gamedata.GAMEDATA)

    if isinstance(final_return, dict):
        gamedata.GAMEDATA = final_return
        return "game"
    elif final_return == "restart":
        gamedata.init(tick)
        return "game"
    elif final_return == "game":
        return "game"
    else:
        started = False
        return final_return

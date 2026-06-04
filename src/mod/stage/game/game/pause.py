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

# Lifeline.PYR v1.0

# Import libraries
import pygame as pg

# Core modules
import mod.core.assets as ast
from mod.core.save import S, wr

# Other module
import mod.etc.etcils as etc

lkpt, sel = 0, 1

def do_pause(rsurface, keys, tick, GAMEDATA):
    global lkpt, sel

    if lkpt > tick:
        lkpt = 0

    # Render
    rsurface.blit(ast.ASSETS["game/pause"], etc.centrexy(ast.ASSETS["game/pause"]))
    etc.MKTX(rsurface, sel, 1, "RESUME", "game")
    etc.MKTX(rsurface, sel, 2, "RESTART", "game")
    etc.MKTX(rsurface, sel, 3, "OPTIONS", "game")
    etc.MKTX(rsurface, sel, 4, "TITLE", "game")

    # Take input
    if keys[pg.K_UP] and etc.srp(tick, lkpt):
        sel -= 1
        lkpt = tick
        ast.ASSETS["mainaud/blip"].play()
    elif keys[pg.K_DOWN] and etc.srp(tick, lkpt):
        sel += 1
        lkpt = tick
        ast.ASSETS["mainaud/blip"].play()
    elif keys[pg.K_RETURN] and etc.srp(tick, lkpt):
        ast.ASSETS["mainaud/blip"].play()
        if sel == 1:
            GAMEDATA["paused"] = False
            return GAMEDATA
        elif sel == 2:
            sel = 1
            return "restart"
        elif sel == 3:
            wr(S)
            lkpt = 0
            return "options"
        else:
            wr(S)
            lkpt = 0
            return "back"
        lkpt = tick
    sel = max(1, min(sel, 4))

    return "game"
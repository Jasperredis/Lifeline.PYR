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
from mod.core.save import S, wr 
import mod.core.assets as ast

# Game module
from mod.stage.game import select

# Game.game modules
from mod.stage.game.game import game

# Other modules
import mod.etc.magicvars as mgv

# Main variables
main_stage = "select"
lkpt = 0

def ACT(rsurface, keys, tick, mx, my, mb):
    global main_stage

    # Render bg
    rsurface.blit(mgv.BGS[str(S["bg"])], (0, 0))

    if main_stage == "select":
        main_stage = select.ACT(rsurface, keys, tick)
    elif main_stage == "back":
        main_stage = "select"
        return "title"
    elif main_stage == "options":
        main_stage = "game"
        return "options"
    elif main_stage == "game":
        main_stage = game.ACT(rsurface, keys, tick, mx, my, mb)

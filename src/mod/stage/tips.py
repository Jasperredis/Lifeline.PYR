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

# Import core module
import mod.core.assets as ast

# Import other modules
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc

TIPS = [
    " Dash doesn't work if its charge is <10.",
    " Dashing in two axis at once in 2D| \
mode doubles your dash usage, making the| \
dash effectively useless. Only use dash| \
in one axis!",
    " This tip looks weird.",
    " Clear all enemies is incredibly useful if| \
you can stack up on heals with a little| \
amount of enemies.",
    " You can't collect heals while jumping.",
    "This tip is 6px further to the left than| \
all of the other tips."
]
tip = 0
lkpt = 0

def ACT(rsurface, keys, tick):
    global TIPS, tip, lkpt

    if lkpt > tick:
        lkpt = 0
    
    # Render static display
    rsurface.blit(
        ast.ASSETS["tips/header"], (
            etc.centrexy(ast.ASSETS["tips/header"], onecoord='x'), 1
        )
    )

    # Render tip
    tip_y = 15
    print(tip, TIPS)
    tip_added = f"Press [RETURN] for a new tip.|Pres [X] to return to the title.||Tip `{tip + 1}/{len(TIPS)}:|" + TIPS[tip]
    tip_proc = tip_added.split('|')
    for line in tip_proc:
        anti_alias = True if tip == 2 else False
        colour = (0, 255, 0) if tip == 2 else mgv.COLOURS[18] 
        text_surface = ast.ASSETS["font1"].render(
            line, anti_alias, colour
        )
        rsurface.blit(text_surface, (2, tip_y))
        tip_y += 6

    # Change tip
    if keys[pg.K_RETURN] and etc.srp(tick, lkpt):
        tip += 1
        tip = 0 if tip >= len(TIPS) else tip
        lkpt = tick

    # Leave
    if keys[pg.K_x]:
        return "title"

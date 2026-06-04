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

# Lifeline.PYR v1.0.1

# Import libraries
import pygame as pg

# Core modules
import mod.core.assets as ast
from mod.core.save import S

# Other modules
import mod.etc.etcils as etc
import mod.etc.magicvars as mgv

TEXT = ["Welcome to Lifeline.PYR."]
text_phase = 0
lkpt = 0
TEXT_ADDONS = [
    "",
    "It seems you haven't played this game]]before.",
    "Use the UP and DOWN arrow keys to navigate]]the title screen.",
    "Use the [RETURN] key to select an option.",
    "It is recommended to explore the]]\"HOW TO PLAY\" menu on the title screen.",
    "You will now see the title screen, and]]this never again.",
    ""
]

def ACT(rsurface, keys, tick):
    global TEXT, text_phase, lkpt, TEXT_ADDONS
    
    text_y = 1
    text_temp = TEXT + ["", "Press [RETURN] to continue."]
    for line in text_temp:
        text_surf = ast.ASSETS["font1"].render(
            line, False, mgv.COLOURS[18]
        )
        rsurface.blit(text_surf, (1, text_y))
        text_y += 6

    if keys[pg.K_RETURN] and etc.srp(tick, lkpt):
        text_phase += 1
        TEXT.extend(TEXT_ADDONS[text_phase].split(']]'))
        lkpt = tick

    if text_phase >= len(TEXT_ADDONS) - 1:
        S["seen_begin"] = True
        return "title"

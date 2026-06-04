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
from cerbose import cprint
import pygame as pg
import sys

# Core modules
import mod.core.assets as ast
from mod.core.save import S

# Other modules
import mod.etc.etcils as etc

lkpt = 0

def ACT(rsurface, tick, mx, my, mb):
    global lkpt
    # Close
    xrect = ast.ASSETS['win/close0'].get_rect()
    xrect.x, xrect.y = 251, 0
    render = ast.ASSETS['win/close1'] if xrect.collidepoint(mx, my) else ast.ASSETS['win/close0']
    rsurface.blit(render, xrect)
    if xrect.collidepoint(mx, my) and mb[0]:
        etc.CLOSE()
    # Fullscreen ToggleW
    xrect.x, xrect.y = 246, 0
    if S['fullscreen']:
        render = ast.ASSETS['win/small1'] if xrect.collidepoint(mx, my) else ast.ASSETS['win/small0']
    else:
        render = ast.ASSETS['win/full1'] if xrect.collidepoint(mx, my) else ast.ASSETS['win/full0']
    rsurface.blit(render, xrect)
    if xrect.collidepoint(mx, my) and mb[0] and etc.srp(tick, lkpt):
        S['fullscreen'] = not S['fullscreen']
        return True # Force makeDisp() (rebuild display)
    # Minimise
    xrect.x, xrect.y = 241, 0
    render = ast.ASSETS['win/min1'] if xrect.collidepoint(mx, my) else ast.ASSETS['win/min0']
    rsurface.blit(render, xrect)
    if xrect.collidepoint(mx, my) and mb[0] and etc.srp(tick, lkpt):
        pg.display.iconify()

    return False

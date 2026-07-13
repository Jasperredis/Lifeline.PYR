# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

from cerbose import cprint
import pygame as pg
import sys
import mod.core.assets as ast
from mod.core.save import S
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

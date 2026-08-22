# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import save_data
import mod.etc.etcils as etc
import mod.etc.BTXT as B
import mod.etc.magicvars as mgv

lkpt = 0


def act(rsurface, fps, tick, mx, my, mb):
    # Metrics
    TOP_TEXT = f"FPS: {fps} - Tick: {tick} - Mouse: {mx}, {my}"
    text = ast.assets_data["font1"].render(TOP_TEXT, False, mgv.colours[19])
    rsurface.blit(text, (2, 2))
    # B.bottom_text
    text = ast.assets_data["font1"].render(B.bottom_text, False, mgv.colours[19])
    rsurface.blit(text, (1, 138))
    # Close
    xrect = ast.assets_data['win/close0'].get_rect()
    xrect.x, xrect.y = 251, 0
    render = ast.assets_data['win/close1'] if xrect.collidepoint(mx, my) \
        else ast.assets_data['win/close0']
    rsurface.blit(render, xrect)
    if xrect.collidepoint(mx, my) and mb[0]:
        etc.close()
    # Fullscreen Toggle
    xrect.x, xrect.y = 246, 0
    if save_data['fullscreen']:
        render = ast.assets_data['win/small1'] if xrect.collidepoint(mx, my) \
            else ast.assets_data['win/small0']
    else:
        render = ast.assets_data['win/full1'] if xrect.collidepoint(mx, my) \
            else ast.assets_data['win/full0']
    rsurface.blit(render, xrect)
    if xrect.collidepoint(mx, my) and mb[0] and etc.srp(tick, lkpt):
        save_data['fullscreen'] = not save_data['fullscreen']
        return True  # Run make_display() (rebuild display)
    # Minimise
    xrect.x, xrect.y = 241, 0
    render = ast.assets_data['win/min1'] if xrect.collidepoint(mx, my) \
        else ast.assets_data['win/min0']
    rsurface.blit(render, xrect)
    if xrect.collidepoint(mx, my) and mb[0] and etc.srp(tick, lkpt):
        pg.display.iconify()
    return False  # Do not run make_display

# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev
# This is FREE SOFTWARE. See the LICENSE-GPL file for more information.

import pygame as pg
import mod.core.assets as ast
from mod.core.save import save_data, write_save, keyb
import mod.etc.etcils as etc
import mod.etc.magicvars as mgv

lkpt, sel = 0, 1


def do_pause(rsurface, keys, tick, game, mx, my, mb):
    global lkpt, sel

    if lkpt > tick:
        lkpt = 0

    # Render
    rsurface.blit(ast.assets_data["game/pause"],
                  etc.centrexy(ast.assets_data["game/pause"]))
    OPTIONS = ["RESUME", "RESTART", "OPTIONS", "TITLE"]
    for i, text in enumerate(OPTIONS):
        rect = etc.mk_text_option(rsurface, sel, i + 1, text, mgv.colours[19],
                                  True, (rsurface.get_height() / 2) - 19,
                                  return_rect=True)
        if save_data["mouse-nav"] and rect.collidepoint(mx, my - 8):
            sel = i + 1
    # Take input
    if keyb(keys, "menu-up") and etc.srp(tick, lkpt):
        sel -= 1
        lkpt = tick
        ast.assets_data["mainaud/blip"].play()
    elif keyb(keys, "menu-down") and etc.srp(tick, lkpt):
        sel += 1
        lkpt = tick
        ast.assets_data["mainaud/blip"].play()
    elif ((keys[pg.K_RETURN] or (save_data["mouse-nav"] and mb[0]))
          and etc.srp(tick, lkpt)):
        ast.assets_data["mainaud/blip"].play()
        if sel == 1:
            game.paused = False
            return game
        elif sel == 2:
            sel = 1
            return "restart"
        elif sel == 3:
            write_save(save_data)
            lkpt = 0
            return "options"
        else:
            write_save(save_data)
            lkpt = 0
            return "back"
        lkpt = tick
    sel = max(1, min(sel, len(OPTIONS)))

    return "game"

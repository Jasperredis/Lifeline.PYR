# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import S, wr
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

# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import pygame as pg
from mod.core.save import S, wr 
import mod.core.assets as ast
from mod.stage.game import select
from mod.stage.game.game import game
import mod.etc.magicvars as mgv

main_stage = "select"
lkpt = 0

def ACT(rsurface, keys, tick, mx, my, mb):
    global main_stage

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

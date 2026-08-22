# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

from mod.core.save import save_data
from mod.stage.game import select
from mod.stage.game.game import game
import mod.etc.magicvars as mgv

main_stage = "select"
lkpt = 0


def act(rsurface, keys, tick, mx, my, mb):
    global main_stage

    rsurface.blit(mgv.bgs[str(save_data["bg"])], (0, 0))

    if main_stage == "select":
        main_stage = select.act(rsurface, keys, tick, mx, my, mb)
    elif main_stage == "back":
        main_stage = "select"
        return "title"
    elif main_stage == "options":
        main_stage = "game"
        return "options"
    elif main_stage == "game":
        main_stage = game.act(rsurface, keys, tick, mx, my, mb)

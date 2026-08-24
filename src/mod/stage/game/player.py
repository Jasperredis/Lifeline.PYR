# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev

import pygame as pg
import mod.core.assets as ast
import mod.etc.magicvars as mgv
from mod.stage.game import constants as con
from mod.stage.game import inputx
from mod.core.save import keyb


def make_player(rsurface, game, tick, keys):
    global plr

    if game.jumping:
        y_deduction = 999
        pointer_sprite = (
            ast.assets_data["game/pointer_jumpend"]
            if (tick - game.last_jump) >= con.jumpend_marker
            else ast.assets_data["game/pointer_jump"])
        # Player ghost
        if game.mode != "2d":
            plrcol = mgv.colours[20] if (
                tick - game.last_jump >= con.jumpend_marker) else \
                mgv.colours[16]
            plrghost = pg.Rect((game.plrx, game.plry - 1), (3, 1))
            pg.draw.rect(rsurface, plrcol, plrghost)  # Draw player ghost
        else:
            plrcol = "jumpend" if (
                tick - game.last_jump >= con.jumpend_marker) else "jumping"
            rsurface.blit(ast.assets_data[f"game/plr_{plrcol}_2d"],
                          (game.plrx, game.plry - 1))
    else:  # Not jumping
        y_deduction = 1
        if game.mode != "2d":
            if keyb(keys, "game-1d-slow"):
                plrcol = mgv.colours[10]
            elif (keyb(keys, "game-dash") and inputx.moving and
                  game.dash > con.dash_functioning_min):
                plrcol = mgv.colours[5]
            else:
                plrcol = mgv.colours[19]
        else:
            if keyb(keys, "game-2d-slow"):
                plrcol = "slow_"
            elif (keyb(keys, "game-dash") and inputx.moving and
                  game.dash > con.dash_functioning_min):
                plrcol = "dash_"
            else:
                plrcol = ""
        pointer_sprite = ast.assets_data["game/pointer"]

    # Create rect
    plr_height = 1 if game.mode != "2d" else 3
    plr = pg.Rect((game.plrx, game.plry - y_deduction), (3, plr_height))

    # Draw
    if game.mode != "2d":
        pg.draw.rect(rsurface, plrcol, plr)
    elif not game.jumping:
        rsurface.blit(ast.assets_data[f"game/plr_{plrcol}2d"],
                      (game.plrx, game.plry - 1))
    pointer_offset = 2 if game.mode != "2d" else 7
    pointer_y = con.pointer_y if (
        game.mode != "2d") else game.plry - pointer_offset
    rsurface.blit(pointer_sprite, (game.plrx - 1, pointer_y))

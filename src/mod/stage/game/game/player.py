# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
import mod.etc.magicvars as mgv
from mod.stage.game.game import constants as con
from mod.stage.game import select
from mod.stage.game.game import inputx
from mod.core.save import keyb

def make_player(rsurface, GAMEDATA, tick, keys):
    global plr

    # Make data
    if GAMEDATA["jumping"]:
        # Base data
        y_deduction = 999
        pointer_sprite = (
            ast.assets_data["game/pointer_jumpend"]
            if (tick - GAMEDATA["last_jump"]) >= con.jumpend_marker
            else ast.assets_data["game/pointer_jump"]
        )
        # Player ghost
        if select.game_type != "2d":
            plrcol = mgv.colours[20] if tick - GAMEDATA["last_jump"] >= con.jumpend_marker else mgv.colours[16]
            plrghost = pg.Rect(
                (GAMEDATA["plrx"], GAMEDATA["plry"] - 1), 
                (3, 1)
            )
            pg.draw.rect(rsurface, plrcol, plrghost)  # Draw player ghost
        else:
            plrcol = "jumpend" if tick - GAMEDATA["last_jump"] >= con.jumpend_marker else "jumping"
            rsurface.blit(ast.assets_data[f"game/plr_{plrcol}_2d"], (GAMEDATA["plrx"], GAMEDATA["plry"] - 1))

    else: # Not jumping
        y_deduction = 1
        if select.game_type != "2d":
            if keyb(keys, "game-1d-slow"):
                plrcol = mgv.colours[10]
            elif keyb(keys, "game-dash") and inputx.moving and GAMEDATA["dash"] > con.dash_functioning_min:
                plrcol = mgv.colours[5]
            else:
                plrcol = mgv.colours[19]
        else:
            if keyb(keys, "game-2d-slow"):
                plrcol = "slow_"
            elif keyb(keys, "game-dash") and inputx.moving and GAMEDATA["dash"] > con.dash_functioning_min:
                plrcol = "dash_"
            else:
                plrcol = ""
        pointer_sprite = ast.assets_data["game/pointer"]

    # Create rect
    plr_height = 1 if select.game_type != "2d" else 3
    plr = pg.Rect(
        (GAMEDATA["plrx"], GAMEDATA["plry"] - y_deduction),
        (3, plr_height)
    )

    # Draw
    if select.game_type != "2d":
        pg.draw.rect(rsurface, plrcol, plr)
    elif not GAMEDATA["jumping"]:
        rsurface.blit(ast.assets_data[f"game/plr_{plrcol}2d"], (GAMEDATA["plrx"], GAMEDATA["plry"] - 1))
    pointer_offset = 2 if select.game_type != "2d" else 7
    pointer_y = con.pointer_y if select.game_type != "2d" else GAMEDATA["plry"] - pointer_offset
    rsurface.blit(pointer_sprite, (GAMEDATA["plrx"] - 1, pointer_y))

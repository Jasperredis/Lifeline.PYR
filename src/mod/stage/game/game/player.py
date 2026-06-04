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

# Lifeline.PYR v1.0

# Import libraries
import pygame as pg

# Core module
import mod.core.assets as ast

# Other module
import mod.etc.magicvars as mgv

# Game modules
from mod.stage.game.game import constants as con
from mod.stage.game import select

def make_player(rsurface, GAMEDATA, tick, keys):
    global plr

    # Make data
    if GAMEDATA["jumping"]:
        # Base data
        y_deduction = 999
        pointer_sprite = (
            ast.ASSETS["game/pointer_jumpend"]
            if (tick - GAMEDATA["last_jump"]) >= con.jumpend_marker
            else ast.ASSETS["game/pointer_jump"]
        )
        # Player ghost
        if select.game_type != "2d":
            plrcol = mgv.COLOURS[19] if tick - GAMEDATA["last_jump"] >= con.jumpend_marker else mgv.COLOURS[15]
            plrghost = pg.Rect(
                (GAMEDATA["plrx"], GAMEDATA["plry"] - 1), 
                (3, 1)
            )
            pg.draw.rect(rsurface, plrcol, plrghost)  # Draw player ghost
        else:
            plrcol = "jumpend" if tick - GAMEDATA["last_jump"] >= con.jumpend_marker else "jumping"
            rsurface.blit(ast.ASSETS[f"game/plr_{plrcol}_2d"], (GAMEDATA["plrx"], GAMEDATA["plry"] - 1))
            
    else: # Not jumping (wow no dip)
        y_deduction = 1
        if select.game_type != "2d":
            if keys[pg.K_s]:
                plrcol = mgv.COLOURS[9]
            elif keys[pg.K_e] and (keys[pg.K_a] or keys[pg.K_d]) and GAMEDATA["dash"] > con.dash_functioning_min:
                plrcol = mgv.COLOURS[4]
            else:
                plrcol = mgv.COLOURS[18]
        else:
            if keys[pg.K_DOWN]:
                plrcol = "slow_"
            elif keys[pg.K_e] and (keys[pg.K_a] or keys[pg.K_d] or keys[pg.K_s] or keys[pg.K_w]) and GAMEDATA["dash"] > con.dash_functioning_min:
                plrcol = "dash_"
            else:
                plrcol = ""
        pointer_sprite = ast.ASSETS["game/pointer"]

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
        rsurface.blit(ast.ASSETS[f"game/plr_{plrcol}2d"], (GAMEDATA["plrx"], GAMEDATA["plry"] - 1))
    pointer_offset = 2 if select.game_type != "2d" else 7
    pointer_y = con.pointer_y if select.game_type != "2d" else GAMEDATA["plry"] - pointer_offset
    rsurface.blit(pointer_sprite, (GAMEDATA["plrx"] - 1, pointer_y))

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
import random as rd

# Core module
import mod.core.assets as ast
from mod.core.save import S

# Other module
import mod.etc.etcils as etc

# Game module
from mod.stage.game.game import constants as con
from mod.stage.game import select

def take_input(GAMEDATA, keys, tick, mx, my, mb):
    if not GAMEDATA["paused"] and not GAMEDATA["gameover"]:
        # Get game type dependent keys
        slow_key = keys[pg.K_s] if select.game_type != "2d" else keys[pg.K_DOWN]
        jump_key = keys[pg.K_w] if select.game_type != "2d" else keys[pg.K_UP]
        
        # Calculate plrx changes
        plrx_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
        # Dash
        if keys[pg.K_e] and (keys[pg.K_a] or keys[pg.K_d]):
            GAMEDATA["dash"] -= con.dash_decrement
            if GAMEDATA["dash"] > con.dash_functioning_min:
                plrx_mod *= con.dash_multiplier
                ast.ASSETS['gameaud/dash'].play()
        else:
            GAMEDATA["dash"] += con.dash_constant_increment
        GAMEDATA["dash"] = max(0, min(GAMEDATA["dash"], con.dash_max))

        # Calculate plry changes (if in 2D mode)
        if select.game_type == "2d":
            plry_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
            # Dash
            if keys[pg.K_e] and (keys[pg.K_w] or keys[pg.K_s]):
                GAMEDATA["dash"] -= con.dash_decrement
                if GAMEDATA["dash"] > con.dash_functioning_min:
                    plry_mod *= con.dash_multiplier
                    ast.ASSETS['gameaud/dash'].play()
            else:
                GAMEDATA["dash"] += con.dash_constant_increment
            GAMEDATA["dash"] = max(0, min(GAMEDATA["dash"], con.dash_max))
        
        # Inertia 
        if S["inertia"]:
            plrx_mod /= con.inertia_base_plrx_divisor
            if keys[pg.K_a]:
                GAMEDATA["velocity"] -= plrx_mod
            if keys[pg.K_d]:
                GAMEDATA["velocity"] += plrx_mod
            if select.game_type == "2d":
                plry_mod /= con.inertia_base_plrx_divisor
                if keys[pg.K_w]:
                    GAMEDATA["velocity_y"] -= plry_mod
                if keys[pg.K_s]:
                    GAMEDATA["velocity_y"] += plry_mod
            GAMEDATA["plrx"] += GAMEDATA["velocity"]
            GAMEDATA["velocity"] -= GAMEDATA["velocity"] / con.inertia_divisor_slow if slow_key else GAMEDATA["velocity"] / con.inertia_divisor_norm
            GAMEDATA["plry"] += GAMEDATA["velocity_y"]
            GAMEDATA["velocity_y"] -= GAMEDATA["velocity_y"] / con.inertia_divisor_slow if slow_key else GAMEDATA["velocity_y"] / con.inertia_divisor_norm
        else: # No inertia
            if keys[pg.K_a]:
                GAMEDATA["plrx"] -= plrx_mod
            elif keys[pg.K_d]:
                GAMEDATA["plrx"] += plrx_mod
            if select.game_type == "2d":
                if keys[pg.K_w]:
                    GAMEDATA["plry"] -= plry_mod
                elif keys[pg.K_s]:
                    GAMEDATA["plry"] += plry_mod
                    
        GAMEDATA["plrx"] = max(con.x_min, min(GAMEDATA["plrx"], con.x_max))
        GAMEDATA["plry"] = max(con.y_min, min(GAMEDATA["plry"], con.y_max))

        # Jumping
        if GAMEDATA["jumping"] and (tick - GAMEDATA["last_jump"]) >= con.jump_tick_end or GAMEDATA["jumping"] and slow_key:
            GAMEDATA["jumping"] = False
            ast.ASSETS["gameaud/land"].play()
        elif jump_key and (tick - GAMEDATA["last_jump"]) >= con.jump_cooldown_time:
            GAMEDATA["jumping"] = True
            GAMEDATA["last_jump"] = tick
            ast.ASSETS["gameaud/jump"].play()

    # Pause
    if keys[pg.K_ESCAPE] and not GAMEDATA["paused"]:
        ast.ASSETS["gameaud/pause"].play()
        GAMEDATA["paused"] = True

    #! This must stay at the end!
    # Game over
    if GAMEDATA["gameover"] and keys[pg.K_r]:
        return [GAMEDATA, "restart"]

    return [GAMEDATA, None]

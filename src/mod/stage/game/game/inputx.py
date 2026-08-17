# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import save_data
from mod.stage.game.game import constants as con
from mod.stage.game import select

moving = False


def take_input(GAMEDATA, keys, tick, mx, my, mb):
    global moving

    if not GAMEDATA["paused"] and not GAMEDATA["gameover"]:
        # Get game type dependent keys
        slow_key = keys[pg.K_s] if select.game_type != "2d" \
            else keys[pg.K_DOWN]
        jump_key = keys[pg.K_w] if select.game_type != "2d" \
            else keys[pg.K_UP]

        # Take input
        moving_left = (keys[pg.K_a] and not save_data["mouse-move"]) or (
            mx < (GAMEDATA["plrx"] + 10) and mb[0] and save_data["mouse-move"])
        moving_right = (keys[pg.K_d] and not save_data["mouse-move"]) or (
            mx > (GAMEDATA["plrx"] - 10) and mb[0] and save_data["mouse-move"])
        moving_up = (select.game_type == "2d" and
                     keys[pg.K_w] and not save_data["mouse-move"]) or (
            my < (GAMEDATA["plry"] + 10) and mb[0] and save_data["mouse-move"])
        moving_down = (select.game_type == "2d" and
                       keys[pg.K_s] and not save_data["mouse-move"]) or (
            my > (GAMEDATA["plry"] - 10) and mb[0] and save_data["mouse-move"])
        moving = (moving_left or moving_right or moving_up or moving_down)

        # Calculate plrx changes
        plrx_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
        plry_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
        # Dash
        if keys[pg.K_e] and moving:
            GAMEDATA["dash"] -= con.dash_decrement
            if GAMEDATA["dash"] > con.dash_functioning_min:
                if moving_left or moving_right:
                    plrx_mod *= con.dash_multiplier
                if moving_up or moving_down:
                    plry_mod *= con.dash_multiplier
                ast.assets_data['gameaud/dash'].play()
        else:
            GAMEDATA["dash"] += con.dash_constant_increment
        GAMEDATA["dash"] = max(0, min(GAMEDATA["dash"], con.dash_max))

        # Inertia
        if save_data["inertia"]:
            plrx_mod /= con.inertia_base_plrx_divisor
            if moving_left:
                GAMEDATA["velocity"] -= plrx_mod
            if moving_right:
                GAMEDATA["velocity"] += plrx_mod
            if select.game_type == "2d":
                plry_mod /= con.inertia_base_plrx_divisor
                if moving_up:
                    GAMEDATA["velocity_y"] -= plry_mod
                if moving_down:
                    GAMEDATA["velocity_y"] += plry_mod
            GAMEDATA["plrx"] += GAMEDATA["velocity"]
            GAMEDATA["velocity"] -= (
                GAMEDATA["velocity"] / con.inertia_divisor_slow if slow_key
                else GAMEDATA["velocity"] / con.inertia_divisor_norm
            )
            GAMEDATA["plry"] += GAMEDATA["velocity_y"]
            GAMEDATA["velocity_y"] -= (
                GAMEDATA["velocity_y"] / con.inertia_divisor_slow if slow_key
                else GAMEDATA["velocity_y"] / con.inertia_divisor_norm
            )
        else:  # No inertia
            if moving_left:
                GAMEDATA["plrx"] -= plrx_mod
            if moving_right:
                GAMEDATA["plrx"] += plrx_mod
            if select.game_type == "2d":
                if moving_up:
                    GAMEDATA["plry"] -= plry_mod
                elif moving_down:
                    GAMEDATA["plry"] += plry_mod

        GAMEDATA["plrx"] = max(con.x_min, min(GAMEDATA["plrx"], con.x_max))
        GAMEDATA["plry"] = max(con.y_min, min(GAMEDATA["plry"], con.y_max))

        # Jumping
        if GAMEDATA["jumping"] and (tick - GAMEDATA["last_jump"]) >= \
           con.jump_tick_end or GAMEDATA["jumping"] and slow_key:
            GAMEDATA["jumping"] = False
            ast.assets_data["gameaud/land"].play()
        elif jump_key and (
            (tick - GAMEDATA["last_jump"]) >= con.jump_cooldown_time
        ):
            GAMEDATA["jumping"] = True
            GAMEDATA["last_jump"] = tick
            ast.assets_data["gameaud/jump"].play()

    # Pause
    if keys[pg.K_ESCAPE] and not GAMEDATA["paused"]:
        ast.assets_data["gameaud/pause"].play()
        GAMEDATA["paused"] = True

    # This must stay at the end!
    # Game over
    if GAMEDATA["gameover"] and keys[pg.K_r]:
        return [GAMEDATA, "restart"]

    return [GAMEDATA, None]

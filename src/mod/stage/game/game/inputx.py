# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import save_data, keyb
from mod.stage.game.game import constants as con
from mod.stage.game import select

moving = False


def take_input(GAMEDATA, keys, tick, mx, my, mb):
    global moving

    if not GAMEDATA["paused"] and not GAMEDATA["gameover"]:
        # Get game type dependent keys
        slow_key = keyb(keys, "game-1d-slow") if select.game_type != "2d" \
            else keyb(keys, "game-2d-slow")
        jump_key = keyb(keys, "game-1d-jump") if select.game_type != "2d" \
            else keyb(keys, "game-2d-jump")

        # Take input
        moving_left = (keyb(keys, "game-move-left")
                       and not save_data["mouse-move"]) or (
            mx < (GAMEDATA["plrx"] + 10) and mb[0] and save_data["mouse-move"])
        moving_right = (keyb(keys, "game-move-right")
                        and not save_data["mouse-move"]) or (
            mx > (GAMEDATA["plrx"] - 10) and mb[0] and save_data["mouse-move"])
        moving_up = (select.game_type == "2d" and
                     keyb(keys, "game-2d-move-up")
                     and not save_data["mouse-move"]) or (
            my < (GAMEDATA["plry"] + 10) and mb[0] and save_data["mouse-move"])
        moving_down = (select.game_type == "2d" and
                       keyb(keys, "game-2d-move-down")
                       and not save_data["mouse-move"]) or (
            my > (GAMEDATA["plry"] - 10) and mb[0] and save_data["mouse-move"])
        moving = (moving_left or moving_right or moving_up or moving_down)

        # Calculate plrx changes
        plrx_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
        plry_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
        # Dash
        if keyb(keys, "game-dash") and moving:
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
    if keyb(keys, "game-pause") and not GAMEDATA["paused"]:
        ast.assets_data["gameaud/pause"].play()
        GAMEDATA["paused"] = True

    # This must stay at the end!
    # Game over
    if GAMEDATA["gameover"] and keys[pg.K_r]:
        return [GAMEDATA, "restart"]

    return [GAMEDATA, None]

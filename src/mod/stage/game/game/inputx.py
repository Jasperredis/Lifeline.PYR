# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import S
from mod.stage.game.game import constants as con
from mod.stage.game import select


def take_input(GAMEDATA, keys, tick, mx, my, mb):
    if not GAMEDATA["paused"] and not GAMEDATA["gameover"]:
        # Get game type dependent keys
        slow_key = keys[pg.K_s] if select.game_type != "2d" \
            else keys[pg.K_DOWN]
        jump_key = keys[pg.K_w] if select.game_type != "2d" \
            else keys[pg.K_UP]

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
            if (keys[pg.K_a] and not S["mouse-move"]) or (
                mx < (GAMEDATA["plrx"] + 10) and mb[0] and S["mouse-move"]
            ):
                GAMEDATA["velocity"] -= plrx_mod
            if (keys[pg.K_d] and not S["mouse-move"]) or (
                mx > (GAMEDATA["plrx"] - 10) and mb[0] and S["mouse-move"]
            ):
                GAMEDATA["velocity"] += plrx_mod
            if select.game_type == "2d":
                plry_mod /= con.inertia_base_plrx_divisor
                if (keys[pg.K_w] and not S["mouse-move"]) or (
                    my < (GAMEDATA["plry"] + 10) and mb[0] and S["mouse-move"]
                ):
                    GAMEDATA["velocity_y"] -= plry_mod
                if (keys[pg.K_s] and not S["mouse-move"]) or (
                    my > (GAMEDATA["plry"] - 10) and mb[0] and S["mouse-move"]
                ):
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
            if (keys[pg.K_a] and not S["mouse-move"]) or (
                mx < GAMEDATA["plrx"] and mb[0] and S["mouse-move"]
            ):
                GAMEDATA["plrx"] -= plrx_mod
            if (keys[pg.K_d] and not S["mouse-move"]) or (
                mx > GAMEDATA["plrx"] and mb[0] and S["mouse-move"]
            ):
                GAMEDATA["plrx"] += plrx_mod
            if select.game_type == "2d":
                if keys[pg.K_w]:
                    GAMEDATA["plry"] -= plry_mod
                elif keys[pg.K_s]:
                    GAMEDATA["plry"] += plry_mod

        GAMEDATA["plrx"] = max(con.x_min, min(GAMEDATA["plrx"], con.x_max))
        GAMEDATA["plry"] = max(con.y_min, min(GAMEDATA["plry"], con.y_max))

        # Jumping
        if GAMEDATA["jumping"] and (tick - GAMEDATA["last_jump"]) >= \
           con.jump_tick_end or GAMEDATA["jumping"] and slow_key:
            GAMEDATA["jumping"] = False
            ast.ASSETS["gameaud/land"].play()
        elif jump_key and (
            (tick - GAMEDATA["last_jump"]) >= con.jump_cooldown_time
        ):
            GAMEDATA["jumping"] = True
            GAMEDATA["last_jump"] = tick
            ast.ASSETS["gameaud/jump"].play()

    # Pause
    if keys[pg.K_ESCAPE] and not GAMEDATA["paused"]:
        ast.ASSETS["gameaud/pause"].play()
        GAMEDATA["paused"] = True

    # This must stay at the end!
    # Game over
    if GAMEDATA["gameover"] and keys[pg.K_r]:
        return [GAMEDATA, "restart"]

    return [GAMEDATA, None]

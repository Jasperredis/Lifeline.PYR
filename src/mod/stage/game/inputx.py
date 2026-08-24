# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import save_data, keyb
from mod.stage.game import constants as con

moving = False


def get_moving(keys, mode, game, mx, my, mb):
    global moving_left, moving_right, moving_up, moving_down, moving
    global slow_key, jump_key
    slow_key = keyb(keys, "game-1d-slow") if mode != "2d" \
        else keyb(keys, "game-2d-slow")
    jump_key = keyb(keys, "game-1d-jump") if mode != "2d" \
        else keyb(keys, "game-2d-jump")
    moving_left = (keyb(keys, "game-move-left")
                   and not save_data["mouse-move"]) or (
        mx < (game.plrx + 10) and mb[0] and save_data["mouse-move"])
    moving_right = (keyb(keys, "game-move-right")
                    and not save_data["mouse-move"]) or (
        mx > (game.plrx - 10) and mb[0] and save_data["mouse-move"])
    moving_up = (mode == "2d" and
                 keyb(keys, "game-2d-move-up")
                 and not save_data["mouse-move"]) or (
        my < (game.plry + 10) and mb[0] and save_data["mouse-move"])
    moving_down = (mode == "2d" and
                   keyb(keys, "game-2d-move-down")
                   and not save_data["mouse-move"]) or (
        my > (game.plry - 10) and mb[0] and save_data["mouse-move"])
    moving = (moving_left or moving_right or moving_up or moving_down)


def do_plrx_mod(keys, game):
    global plrx_mod, plry_mod
    plrx_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
    plry_mod = con.plrx_slow_mod if slow_key else con.plrx_norm_mod
    # Dash
    if keyb(keys, "game-dash") and moving:
        game.dash -= con.dash_decrement
        if game.dash > con.dash_functioning_min:
            if moving_left or moving_right:
                plrx_mod *= con.dash_multiplier
            if moving_up or moving_down:
                plry_mod *= con.dash_multiplier
            if moving:
                ast.assets_data['gameaud/dash'].play()
    else:
        game.dash += con.dash_constant_increment
        game.dash = max(0, min(game.dash, con.dash_max))
    return game


def inertia_move(game, mode):
    global plrx_mod, plry_mod
    plrx_mod /= con.inertia_base_plrx_divisor
    if moving_left:
        game.velocity -= plrx_mod
    if moving_right:
        game.velocity += plrx_mod
    if mode == "2d":
        plry_mod /= con.inertia_base_plrx_divisor
        if moving_up:
            game.velocity_y -= plry_mod
        if moving_down:
            game.velocity_y += plry_mod
    game.plrx += game.velocity
    game.velocity -= (
        game.velocity / con.inertia_divisor_slow if slow_key
        else game.velocity / con.inertia_divisor_norm
    )
    game.plry += game.velocity_y
    game.velocity_y -= (
        game.velocity_y / con.inertia_divisor_slow if slow_key
        else game.velocity_y / con.inertia_divisor_norm
    )
    return game


def no_inertia_move(game, mode):
    if moving_left:
        game.plrx -= plrx_mod
    if moving_right:
        game.plrx += plrx_mod
    if mode == "2d":
        if moving_up:
            game.plry -= plry_mod
        if moving_down:
            game.plry += plry_mod
    return game


def do_jump(game, tick):
    if game.jumping and ((tick - game.last_jump)
                         >= con.jump_tick_end or slow_key):
        game.jumping = False
        ast.assets_data["gameaud/land"].play()
    elif jump_key and (tick - game.last_jump) >= con.jump_cooldown_time:
        game.jumping = True
        game.last_jump = tick
        ast.assets_data["gameaud/jump"].play()
    return game


def take_input(mode, game, keys, tick, mx, my, mb):
    if not game.paused and not game.gameover:
        get_moving(keys, mode, game, mx, my, mb)
        game = do_plrx_mod(keys, game)
        game = inertia_move(game, mode) if save_data["inertia"] else \
            no_inertia_move(game, mode)
        game.plrx = max(con.x_min, min(game.plrx, con.x_max))
        game.plry = max(con.y_min, min(game.plry, con.y_max))
        game = do_jump(game, tick)
    if keyb(keys, "game-pause") and not game.paused:
        ast.assets_data["gameaud/pause"].play()
        game.paused = True

    if game.gameover and keys[pg.K_r]:
        return [game, "restart"]
    return [game, None]

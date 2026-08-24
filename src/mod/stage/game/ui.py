# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev
# This is FREE SOFTWARE. See the LICENSE-GPL file for more information.

# from collections import Counter (see line 183)
import pygame as pg
import random as rd
import mod.core.assets as ast
from mod.core.save import save_data, keyb
import mod.etc.etcils as etc
import mod.etc.magicvars as mgv
from mod.stage.game import constants as con
from mod.stage.game import inputx


def make_text(mode, rsurface, content, order, *, lessen_base=False):
    if mode != "2d":
        col, highlight = mgv.colours[1], None
    else:
        col, highlight = mgv.colours[19], mgv.colours[1]
    text = ast.assets_data["font1"].render(
        content, False, col, highlight)
    if mode != "2d":
        y_base = 9 if lessen_base else 13
        x_pos = etc.centrexy(text, onecoord="x")
    else:
        y_base = 1
        x_pos = 217
    y_pos_base = (rsurface.get_height() / 2) if mode != "2d" else 0
    y_pos = y_pos_base + y_base + (order * 6)
    rsurface.blit(text, (x_pos, y_pos))


def draw_tl_icon(mode, rsurface, image, y, *, text=None):
    rsurface.blit(image, (2, y))
    if text is not None:
        text_surf = ast.assets_data["font1"].render(
            text, False, mgv.colours[19], mgv.colours[1]
        )  # Make text
        rsurface.blit(text_surf, (15, y+3))  # Blit text


def draw_life(rsurface, game, tick):
    life_width = ast.assets_data["game/life0"].get_width()
    padding = 3
    if game.mode != "2d":
        life_x = (rsurface.get_width() // 2) - (life_width * 3) - padding
        life_y = (rsurface.get_height() // 2) + 3
    else:
        life_x = 1
        life_y = (rsurface.get_height() // 2) - (life_width * 3) - padding
        life_y += 25

    # Render existing life
    for i in range(game.life):
        rsurface.blit(ast.assets_data["game/life1"], (life_x, life_y))
        if game.mode != "2d":
            life_x += life_width + 1
        else:
            life_y += life_width + 1

    # Render missing life
    for i in range(5 - game.life):
        rsurface.blit(ast.assets_data["game/life0"], (life_x, life_y))
        if game.mode != "2d":
            life_x += life_width + 1
        else:
            life_y += life_width + 1

    # Render life tick timer
    ltime = min(
        [0, 1, 2, 3, 4, 5, 6],
        key=lambda x: abs(x - ((tick - game.last_loss) // 10)))
    rsurface.blit(
        ast.assets_data[f"game/life_time{ltime}"],
        (life_x, life_y))


def get_text(game):
    if game.mode != "2d":
        if not game.gameover:
            return [
                f"SCORE: {game.score}", f"HIGH: {save_data['high']}",
                f"TOTAL: {save_data['total']}",
                f"GAME: {save_data['played']}"]
        else:
            if game.score > game.initial_high:
                return [
                    "GAMEOVER!", f"SCORE: {game.score}",
                    f"NEW HIGHSCORE! {game.initial_high} TO {game.score}",
                    "PRESS [R] TO RESTART."]
            else:
                return [
                    "GAMEOVER!", f"SCORE: {game.score}",
                    f"HIGH: {game.initial_high}", "PRESS [R] TO RESTART."]
    else:
        if not game.gameover:
            return [
                "SCORE:", str(game.score), "",
                "HIGH:", str(save_data["high"]), "",
                "TOTAL:", str(save_data["total"]), "",
                "GAME:", str(save_data["played"])]
        else:
            return [
                "GAME", "OVER!", "",
                "SCORE:", str(game.score), "",
                "HIGH:", str(save_data["high"]), "",
                "AGAIN:", "[R]"]


def draw_text(rsurface, game, tick):
    if not game.shown_death_notif:
        draw_notif(rsurface, "dead", tick, game)
        game.shown_death_notif = True
    text = get_text(game)
    for i, line in enumerate(text, start=1):
        make_text(game.mode, rsurface, line, i, lessen_base=game.gameover)


def draw_jump_charge(rsurface, game, tick):
    rtime = min(
        [1, 60, 120, 180, 240, 300],
        key=lambda x: abs(x - (tick - game.last_jump)))
    rtime = int(rtime / 60) - 1
    rtime = max(0, min(rtime, 4))
    text_cont = f"{rtime}/4" if game.mode == "2d" else f"JUMP PWR: {rtime}/4"
    draw_tl_icon(
        game.mode, rsurface, ast.assets_data[f"game/jump{rtime}"], 2,
        text=text_cont)


def draw_velocity_icon(rsurface, game, tick):
    if save_data["inertia"] and save_data["velocity-icon"]:
        if game.mode != "2d":
            draw_tl_icon(game.mode, rsurface,
                         ast.assets_data["game/velocity"], 17,
                         text=f"VELOCITY: {round(game.velocity, 2)}")
        else:
            draw_tl_icon(game.mode, rsurface,
                         ast.assets_data["game/velocity_x"], 17,
                         text=str(round(game.velocity, 2)))
            draw_tl_icon(game.mode, rsurface,
                         ast.assets_data["game/velocity_y"], 32,
                         text=str(round(game.velocity_y, 2)))


def draw_dash_bar(rsurface, game, tick, keys):
    dash_bar_x = etc.centrexy(ast.assets_data["game/dash"], onecoord="x")
    if keyb(keys, "game-dash") and inputx.moving and game.dash > 10:
        dash_bar_x += rd.randint(-1, 1)
    rsurface.blit(
        ast.assets_data["game/dash"],
        (dash_bar_x,
         rsurface.get_height() - (
             1 + ast.assets_data["game/dash"].get_height())))
    dash_fill = pg.Rect(
        dash_bar_x + 11, rsurface.get_height() - 7, game.dash, 2)
    pg.draw.rect(rsurface, mgv.colours[6], dash_fill)


def draw_notifs(rsurface, tick):
    global pts_y, showing_pts
    if showing_pts:
        if tick - last_show_pts_time <= 3 or tick - last_show_pts_time == 5:
            pts_y -= 1
        elif tick - last_show_pts_time >= con.show_pts_time:
            showing_pts = False
    if showing_pts:
        rsurface.blit(ast.assets_data[f"notif/{showing_pts_num}"],
                      (pts_x, pts_y))


def draw_ui(rsurface, game, tick, keys):
    if not game.gameover:
        draw_life(rsurface, game, tick)
    draw_text(rsurface, game, tick)
    draw_jump_charge(rsurface, game, tick)
    draw_velocity_icon(rsurface, game, tick)
    draw_dash_bar(rsurface, game, tick, keys)
    draw_notifs(rsurface, tick)


def draw_ui_before_entities(mode, rsurface):
    if mode == "normal_game":
        rsurface.blit(ast.assets_data["game/bar"],
                      (etc.centrexy(ast.assets_data["game/bar"])))
    elif mode == "2d":
        rsurface.blit(ast.assets_data["game/field"],
                      (etc.centrexy(ast.assets_data["game/field"])))


showing_pts = False
pts_x, pts_y, last_show_pts_time, showing_pts_num = 0, 0, 0, 0


def draw_notif(rsurface, num, tick, game):
    global showing_pts, pts_x, pts_y, last_show_pts_time, showing_pts_num
    if save_data["notifs"]:
        showing_pts = True
        pts_x, pts_y = game.plrx, game.plry - \
            con.show_pts_y_offset
        last_show_pts_time = tick
        showing_pts_num = num

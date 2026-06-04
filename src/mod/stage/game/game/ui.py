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
# from collections import Counter (see line 183)
import pygame as pg
import random as rd

# Core modules
import mod.core.assets as ast
from mod.core.save import S

# Other modules
import mod.etc.etcils as etc
import mod.etc.magicvars as mgv

# Game module (for getting game type)
from mod.stage.game import select

def make_text(rsurface, content, order, *, lessen_base=False):
    if select.game_type != "2d":
        col, highlight = mgv.COLOURS[0], None
    else:
        col, highlight = mgv.COLOURS[18], mgv.COLOURS[0]
    text = ast.ASSETS["font1"].render(
        content, False, col, highlight
    )
    if select.game_type != "2d":
        y_base = 9 if lessen_base else 13
        x_pos = etc.centrexy(text, onecoord="x")
    else:
        y_base = 1
        x_pos = 217
    y_pos_base = (rsurface.get_height() / 2) if select.game_type != "2d" else 0
    y_pos = y_pos_base + y_base + (order * 6)
    rsurface.blit(text, (x_pos, y_pos))

def draw_tl_icon(rsurface, image, y, *, text=None):
    rsurface.blit(image, (2, y))
    if text is not None:
        text_surf = ast.ASSETS["font1"].render(
            text, False, mgv.COLOURS[18], mgv.COLOURS[0]
        )  # Make text
        rsurface.blit(text_surf, (15, y+3))  # Blit text     

def draw_ui(rsurface, GAMEDATA, tick, keys):
    # * Life
    if not GAMEDATA["gameover"]:
        life_width = ast.ASSETS["game/life0"].get_width()
        padding = 3
        if select.game_type != "2d":
            life_x = (rsurface.get_width() // 2) - (life_width * 3) - padding
            life_y = (rsurface.get_height() // 2) + 3
        else:
            life_x = 1
            life_y = (rsurface.get_height() // 2) - (life_width * 3) - padding
            life_y += 25

        # Render existing life
        for i in range(GAMEDATA["life"]):
            rsurface.blit(
                ast.ASSETS["game/life1"], (life_x, life_y)
            )
            if select.game_type != "2d":
                life_x += life_width + 1
            else:
                life_y += life_width + 1

        # Render missing life             
        for i in range(5 - GAMEDATA["life"]):
            rsurface.blit(
                ast.ASSETS["game/life0"], (life_x, life_y)
            )
            if select.game_type != "2d":
                life_x += life_width + 1
            else:
                life_y += life_width + 1

        # Render life tick timer
        ltime = min(
            [0, 1, 2, 3, 4, 5, 6],
            key=lambda x: abs(x - ((tick - GAMEDATA["last_loss"]) // 10)),
        )
        rsurface.blit(
            ast.ASSETS[f"game/life_time{ltime}"],
            (life_x, life_y)
        )

    # * Text
    if not GAMEDATA["gameover"]:
        if select.game_type != "2d":
            make_text(rsurface, f"SCORE: {GAMEDATA["score"]}", 1)
            make_text(rsurface, f"HIGH: {S['high']}", 2)
            make_text(rsurface, f"TOTAL: {S['total']}", 3)
            make_text(rsurface, f"GAME: {S['played']}", 4)
        else:
            make_text(rsurface, "SCORE:", 0)
            make_text(rsurface, str(GAMEDATA["score"]), 1)
            make_text(rsurface, "HIGH:", 3)
            make_text(rsurface, str(S["high"]), 4)
            make_text(rsurface, "TOTAL:", 6)
            make_text(rsurface, str(S["total"]), 7)
            make_text(rsurface, "GAME:", 9)
            make_text(rsurface, str(S["played"]), 10)
    elif GAMEDATA["gameover"]:  # Game over
        if select.game_type != "2d":
            make_text(rsurface, f"SCORE: {GAMEDATA['score']}", 1, lessen_base=True)
            make_text(rsurface, "GAMEOVER!", 0, lessen_base=True)
            if GAMEDATA["initial_high"] < GAMEDATA["score"]:
                textcont = f"NEW HIGHSCORE! {GAMEDATA["initial_high"]} TO {GAMEDATA["score"]}"
            else:
                textcont = f"HIGH: {GAMEDATA["initial_high"]}"
            make_text(rsurface, textcont, 2, lessen_base=True)
            make_text(rsurface, "PRESS [R] TO RESTART.", 3, lessen_base=True)
        else:
            make_text(rsurface, "GAME", 0)
            make_text(rsurface, "OVER!", 1)
            make_text(rsurface, "SCORE:", 3)
            make_text(rsurface, str(GAMEDATA['score']), 4)
            make_text(rsurface, "HIGH:", 6)
            make_text(rsurface, str(S['high']), 7)
            make_text(rsurface, "AGAIN:", 9)
            make_text(rsurface, "[R]", 10)

    # * Others
    # Show jump charge
    rtime = min(
        [1, 60, 120, 180, 240, 300],
        key=lambda x: abs(x - (tick - GAMEDATA["last_jump"])),
    )
    rtime = int(rtime / 60) - 1
    rtime = max(0, min(rtime, 4))
    text_cont = f"{rtime}/4" if select.game_type == "2d" else f"JUMP PWR: {rtime}/4"
    draw_tl_icon(
        rsurface,
        ast.ASSETS[f"game/jump{rtime}"],
        2, text=text_cont
    )
    
    # Show velocity
    if S["inertia"] and S["velocity-icon"]:
        if select.game_type != "2d":
            draw_tl_icon(rsurface, ast.ASSETS["game/velocity"], 17, text=f"VELOCITY: {round(GAMEDATA['velocity'], 2)}")
        else:
            draw_tl_icon(rsurface, ast.ASSETS["game/velocity_x"], 17, text=str(round(GAMEDATA["velocity"], 2)))
            draw_tl_icon(rsurface, ast.ASSETS["game/velocity_y"], 32, text=str(round(GAMEDATA["velocity_y"], 2)))

    # Dash bar
    dash_bar_x = etc.centrexy(ast.ASSETS["game/dash"], onecoord="x")
    if keys[pg.K_e] and (keys[pg.K_a] or keys[pg.K_d]) and GAMEDATA["dash"] > 10:
        dash_bar_x += rd.randint(-1, 1)
    rsurface.blit(
        ast.ASSETS["game/dash"],
        (
            dash_bar_x,
            rsurface.get_height() - (1 + ast.ASSETS["game/dash"].get_height()),
        ),
    )
    dash_fill = pg.Rect(
        dash_bar_x + 11,
        rsurface.get_height() - 7,  # 7 for getting into bar
        GAMEDATA["dash"],
        2,
    )
    pg.draw.rect(rsurface, mgv.COLOURS[5], dash_fill)

    #! The code below was made when enemies were only one coordinate because 2D mode didn't exist yet.
    #! I still want the feature, but I don't really feel like working with the logic as of right now,
    #! so it's going to stay commented out.
    #
    # Show many enemies warnings
    # entity_counts = Counter(GAMEDATA["enemies"])
    # entity_counts.update(GAMEDATA["heals"])
    # for x, count in entity_counts.items():
    #     if count > 1:
    #         rsurface.blit(
    #             ast.ASSETS["game/many_enemies"],
    #             (x, (rsurface.get_height() // 2) - (4 + ast.ASSETS["game/many_enemies"].get_height()))
    #             # 4 is padding
    #        )

def draw_ui_before_entities(rsurface):
    if select.game_type == "normal_game":
        rsurface.blit(ast.ASSETS["game/bar"], (etc.centrexy(ast.ASSETS["game/bar"])))
    elif select.game_type == "2d":
        rsurface.blit(ast.ASSETS["game/field"], (etc.centrexy(ast.ASSETS["game/field"])))

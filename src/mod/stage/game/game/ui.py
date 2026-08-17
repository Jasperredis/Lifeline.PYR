# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

# from collections import Counter (see line 183)
import pygame as pg
import random as rd
import mod.core.assets as ast
from mod.core.save import save_data
import mod.etc.etcils as etc
import mod.etc.magicvars as mgv
from mod.stage.game import select
from mod.stage.game.game import constants as con


def make_text(rsurface, content, order, *, lessen_base=False):
    if select.game_type != "2d":
        col, highlight = mgv.colours[1], None
    else:
        col, highlight = mgv.colours[19], mgv.colours[1]
    text = ast.assets_data["font1"].render(
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
        text_surf = ast.assets_data["font1"].render(
            text, False, mgv.colours[19], mgv.colours[1]
        )  # Make text
        rsurface.blit(text_surf, (15, y+3))  # Blit text


def draw_ui(rsurface, GAMEDATA, tick, keys):
    global pts_y, showing_pts
    # * Life
    if not GAMEDATA["gameover"]:
        life_width = ast.assets_data["game/life0"].get_width()
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
                ast.assets_data["game/life1"], (life_x, life_y)
            )
            if select.game_type != "2d":
                life_x += life_width + 1
            else:
                life_y += life_width + 1

        # Render missing life
        for i in range(5 - GAMEDATA["life"]):
            rsurface.blit(
                ast.assets_data["game/life0"], (life_x, life_y)
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
            ast.assets_data[f"game/life_time{ltime}"],
            (life_x, life_y)
        )

    # * Text
    if not GAMEDATA["gameover"]:
        if select.game_type != "2d":
            make_text(rsurface, f"SCORE: {GAMEDATA["score"]}", 1)
            make_text(rsurface, f"HIGH: {save_data['high']}", 2)
            make_text(rsurface, f"TOTAL: {save_data['total']}", 3)
            make_text(rsurface, f"GAME: {save_data['played']}", 4)
        else:
            make_text(rsurface, "SCORE:", 0)
            make_text(rsurface, str(GAMEDATA["score"]), 1)
            make_text(rsurface, "HIGH:", 3)
            make_text(rsurface, str(save_data["high"]), 4)
            make_text(rsurface, "TOTAL:", 6)
            make_text(rsurface, str(save_data["total"]), 7)
            make_text(rsurface, "GAME:", 9)
            make_text(rsurface, str(save_data["played"]), 10)
    elif GAMEDATA["gameover"]:  # Game over
        if not GAMEDATA["shown_death_notif"]:
            draw_notif(rsurface, "dead", tick, GAMEDATA)
            GAMEDATA["shown_death_notif"] = True
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
            make_text(rsurface, str(save_data['high']), 7)
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
        ast.assets_data[f"game/jump{rtime}"],
        2, text=text_cont
    )
    
    # Show velocity
    if save_data["inertia"] and save_data["velocity-icon"]:
        if select.game_type != "2d":
            draw_tl_icon(rsurface, ast.assets_data["game/velocity"], 17, text=f"VELOCITY: {round(GAMEDATA['velocity'], 2)}")
        else:
            draw_tl_icon(rsurface, ast.assets_data["game/velocity_x"], 17, text=str(round(GAMEDATA["velocity"], 2)))
            draw_tl_icon(rsurface, ast.assets_data["game/velocity_y"], 32, text=str(round(GAMEDATA["velocity_y"], 2)))

    # Dash bar
    dash_bar_x = etc.centrexy(ast.assets_data["game/dash"], onecoord="x")
    if keys[pg.K_e] and (keys[pg.K_a] or keys[pg.K_d]) and GAMEDATA["dash"] > 10:
        dash_bar_x += rd.randint(-1, 1)
    rsurface.blit(
        ast.assets_data["game/dash"],
        (
            dash_bar_x,
            rsurface.get_height() - (1 + ast.assets_data["game/dash"].get_height()),
        ),
    )
    dash_fill = pg.Rect(
        dash_bar_x + 11,
        rsurface.get_height() - 7,  # 7 for getting into bar
        GAMEDATA["dash"],
        2,
    )
    pg.draw.rect(rsurface, mgv.colours[6], dash_fill)

    # Draw points popup
    if showing_pts:
        if tick - last_show_pts_time <= 3 or tick - last_show_pts_time == 5:
            pts_y -= 1
        elif tick - last_show_pts_time >= con.show_pts_time:
            showing_pts = False
    if showing_pts:
        rsurface.blit(ast.assets_data[f"game/notif_{showing_pts_num}"],
                      (pts_x, pts_y))

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
    #             ast.assets_data["game/many_enemies"],
    #             (x, (rsurface.get_height() // 2) - (4 + ast.assets_data["game/many_enemies"].get_height()))
    #             # 4 is padding
    #        )

def draw_ui_before_entities(rsurface):
    if select.game_type == "normal_game":
        rsurface.blit(ast.assets_data["game/bar"], (etc.centrexy(ast.assets_data["game/bar"])))
    elif select.game_type == "2d":
        rsurface.blit(ast.assets_data["game/field"], (etc.centrexy(ast.assets_data["game/field"])))


showing_pts = False
pts_x, pts_y, last_show_pts_time, showing_pts_num = 0, 0, 0, 0


def draw_notif(rsurface, num, tick, GAMEDATA):
    global showing_pts, pts_x, pts_y, last_show_pts_time, showing_pts_num
    if save_data["notifs"]:
        showing_pts = True
        pts_x, pts_y = GAMEDATA["plrx"], GAMEDATA["plry"] - \
            con.show_pts_y_offset
        last_show_pts_time = tick
        showing_pts_num = num

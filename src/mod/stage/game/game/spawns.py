# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import random as rd
import mod.core.assets as ast
from mod.core.save import save_data
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
from mod.stage.game.game import constants as con
from mod.stage.game import select
from mod.stage.game.game.ui import draw_notif

# falling_scorers = ["-50_pts", "25_pts", "50_pts", "100_pts"]
# for reference ↓↓↓
FALLING_SCORER_SCORE_RESULTS = {
    "-50_pts": -50,
    "25_pts": 25,
    "50_pts": 50,
    "100_pts": 100
}


def get_falling_type(GAMEDATA):
    # Assuming there is a powerup, choose one
    if (GAMEDATA["life"] <= 2 and not
            etc.chance(con.falling_ignore_pref_chance)):
        powerup = "max_life"
        dire = True
    elif (len(GAMEDATA["enemies"]) >= con.enemy_crowdedness and not
          etc.chance(con.falling_ignore_pref_chance)):
        powerup = "clear_enemies"
        dire = True
    else:
        powerup = rd.choice(con.falling_powerups)
        dire = False

    # Choose and return type
    powerup_chance = con.dire_falling_powerup_chance if dire else \
        con.falling_powerup_chance
    if etc.chance(powerup_chance):
        return powerup
    elif etc.chance(con.falling_scorer_chance):
        return rd.choice(con.falling_scorers)
    else:
        return rd.choice(con.falling_hazards)


def do_spawns(rsurface, plr, GAMEDATA, tick):
    # Spawn enemies and heals
    if not GAMEDATA["paused"] and etc.chance(con.spawn_chance):
        addition = {
                "x": rd.randint(con.x_min, con.x_max),
                "y": 63 if select.game_type != "2d" else
                rd.randint(con.y_min, con.y_max)
           }
        if etc.chance(50):
            GAMEDATA['enemies'].append(addition)
        else:
            GAMEDATA['heals'].append(addition)

    # Handle each enemy and heal
    new_enemies, new_heals = [], []

    # Enemies
    for enemy in GAMEDATA["enemies"]:
        # Rect
        i = pg.Rect(
            (enemy["x"], enemy["y"]),
            (3, 1 if select.game_type != "2d" else 3)
        )
        # Render
        if select.game_type != "2d":
            pg.draw.rect(rsurface, mgv.colours[12], i)
        else:
            rsurface.blit(ast.assets_data["game/enemy_2d"],
                          (enemy["x"], enemy["y"]))
        # Collisions
        if not GAMEDATA["paused"] and plr.colliderect(i):
            if not GAMEDATA["iframe"]:
                GAMEDATA["life"] -= 1
                GAMEDATA["iframe"] = True
                GAMEDATA["last_iframe_time"] = tick
                ast.assets_data["gameaud/hurt"].play()
                draw_notif(rsurface, "hurt", tick, GAMEDATA)
        else:
            new_enemies.append({"x": enemy["x"], "y": enemy["y"]})
        if save_data['indicators']:
            rsurface.blit(
                ast.assets_data['game/enemy_indicator'],
                (enemy["x"] - 1, enemy["y"] - con.enemy_indicator_offset +
                 (2 if select.game_type == "2d" else 0))
            )

    # Heals
    for heal in GAMEDATA["heals"]:
        # Rect
        i = pg.Rect(
            (heal["x"], heal["y"]),
            (3, 1 if select.game_type != "2d" else 3)
        )
        # Render
        if select.game_type != "2d":
            pg.draw.rect(rsurface, mgv.colours[11], i)
        else:
            rsurface.blit(ast.assets_data["game/heal_2d"],
                          (heal["x"], heal["y"]))
        # Collisions
        if not GAMEDATA["paused"] and plr.colliderect(i):
            GAMEDATA["life"] += 1
            ast.assets_data["gameaud/heal"].play()
            draw_notif(rsurface, "heal", tick, GAMEDATA)
        else:
            new_heals.append({"x": heal["x"], "y": heal["y"]})
        if save_data['indicators']:
            rsurface.blit(
                ast.assets_data['game/heal_indicator'],
                (heal["x"] - 1, heal["y"] - con.heal_indicator_offset +
                 (2 if select.game_type == "2d" else 0))
            )

    # Update data
    GAMEDATA["enemies"], GAMEDATA["heals"] = new_enemies, new_heals
    GAMEDATA["life"] = max(0, min(GAMEDATA["life"], 5))

    # Spawn falling things
    if not GAMEDATA["paused"] and etc.chance(con.falling_thing_chance):
        fall_type = get_falling_type(GAMEDATA)
        if fall_type in con.falling_hazards:
            x = rd.randint(int(GAMEDATA["plrx"] - con.falling_hazard_x_range),
                           int(GAMEDATA["plrx"] + con.falling_hazard_x_range))
        else:
            x = rd.randint(con.x_min, con.x_max)
        GAMEDATA["falls"].append(  # Actually add
            {
                "x": x,
                "y": con.falling_object_init_y,
                "type": fall_type
            }
        )

    # Handle each fall
    new_falls = []
    for fall in GAMEDATA["falls"]:
        # Create rect
        fall_rect = ast.assets_data[f"game/{fall['type']}"].get_rect()
        fall["y"] += 2 if not GAMEDATA["paused"] else 0
        fall_rect.x, fall_rect.y = fall["x"], fall["y"]
        rsurface.blit(ast.assets_data[f"game/{fall['type']}"],
                      fall_rect)  # Render
        # Collisions
        if not GAMEDATA["paused"] and plr.colliderect(fall_rect):
            if fall["type"] == "clear_enemies":
                ast.assets_data["gameaud/jump"].play()
                GAMEDATA["enemies"] = []
            elif fall["type"] == "max_life":
                ast.assets_data["gameaud/max_life"].play()
                GAMEDATA["life"] = 5
            elif fall["type"] == "max_jump":
                ast.assets_data["gameaud/jump"].play()
                GAMEDATA["last_jump"] = con.jump_init
            elif fall["type"] in con.falling_scorers:
                if fall["type"] == "-50_pts":
                    ast.assets_data["gameaud/point_loss"].play()
                else:
                    ast.assets_data["gameaud/scorer"].play()
                GAMEDATA["score"] += FALLING_SCORER_SCORE_RESULTS[fall["type"]]
            else:
                GAMEDATA["life"] = 0
                ast.assets_data["gameaud/falling_obj_kill"].play()
            if f"game/notif_{fall['type']}" in ast.assets_data:
                draw_notif(rsurface, fall["type"], tick, GAMEDATA)
        else:
            new_falls.append(fall)
    GAMEDATA["falls"] = new_falls

    # Spawn lasers
    if not GAMEDATA["paused"] and etc.chance(con.laser_chance):
        GAMEDATA["lasers"].append(
            {
                "x": GAMEDATA["plrx"],
                "fired": False,
                "start_time": tick,
                "last_frame_change": tick,
                "frame": 2
            }
        )
        ast.assets_data["gameaud/laser_warn"].play()

    # Handle lasers
    new_lasers = []
    for laser in GAMEDATA["lasers"]:
        if not GAMEDATA["paused"]:
            if not tick - laser["start_time"] >= con.laser_end_time:
                if not laser["fired"]:
                    if tick - laser["start_time"] >= con.laser_fire_time:
                        laser["fired"] = True
                        laser["fire_time"] = tick
                        ast.assets_data["gameaud/laser_strike"].play()
                    else:
                        rsurface.blit(
                            ast.assets_data["game/laser_warn"],
                            (laser["x"] - 2, con.laser_warn_y_pos -
                             ast.assets_data["game/laser_warn"].get_height())
                        )
                    new_lasers.append(laser)
                else:
                    laser_rect = ast.assets_data["game/laser_1_top"].get_rect()
                    laser_rect.x, laser_rect.y = laser["x"], 0
                    rsurface.blit(
                        ast.assets_data[f"game/laser_{laser['frame']}_top"],
                        laser_rect)
                    laser_rect.height = rsurface.get_height()
                    rsurface.blit(
                        ast.assets_data[f"game/laser_{laser['frame']}_bottom"],
                        (laser["x"] - 2,
                         ast.assets_data["game/laser_1_top"].get_height())
                    )
                    if tick - laser["last_frame_change"] >= \
                       con.laser_frame_interval:
                        laser["frame"] = 1 if laser["frame"] == 2 else 2
                        laser["last_frame_change"] = tick
                    if plr.colliderect(laser_rect):
                        GAMEDATA["life"] = 0
                    else:
                        new_lasers.append(laser)
                if (tick - laser["start_time"] >= con.laser_fire_time and
                        tick - laser["start_time"] <= con.laser_flash_time):
                    flash_rect = pg.Rect(0, 0,
                                         rsurface.get_width(),
                                         rsurface.get_height())
                    pg.draw.rect(rsurface, mgv.colours[19], flash_rect)
        else:
            laser["start_time"] += 1
            laser["last_frame_change"] += 1
            new_lasers.append(laser)
    GAMEDATA["lasers"] = new_lasers

    return GAMEDATA

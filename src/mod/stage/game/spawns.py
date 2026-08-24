# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import random as rd
import mod.core.assets as ast
from mod.core.save import save_data
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
from mod.stage.game import constants as con
from mod.stage.game.ui import draw_notif

FALLING_SCORER_SCORE_RESULTS = {
    "-50_pts": -50,
    "25_pts": 25,
    "50_pts": 50,
    "100_pts": 100
}


def get_falling_type(game):
    # Assuming there is a powerup, choose one
    if (game.life <= 2 and not
            etc.chance(con.falling_ignore_pref_chance)):
        powerup = "max_life"
        dire = True
    elif (len(game.enemies) >= con.enemy_crowdedness and not
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


def get_spawn_type():
    if save_data["dif"] == 1:
        enemy_chance = con.enemy_chance_easy
    elif save_data["dif"] == 2:
        enemy_chance = con.enemy_chance_normal
    else:
        enemy_chance = con.enemy_chance_hard
    if etc.chance(enemy_chance):
        return "enemy"
    return "heal"


def spawn_enemies_and_heals(game):
    spawn_chance = con.spawn_chance if save_data["dif"] != 4 \
        else con.spawn_chance_intense
    if not game.paused and etc.chance(spawn_chance):
        addition = {
                "x": rd.randint(con.x_min, con.x_max),
                "y": 63 if game.mode != "2d" else
                rd.randint(con.y_min, con.y_max)
           }
        if get_spawn_type() == "heal":
            game.heals.append(addition)
        else:
            game.enemies.append(addition)
    return game


def handle_spawn(rsurface, tick, plr, new_enemies, new_heals, spawn,
                 spawn_type, game):
    i = pg.Rect((spawn["x"], spawn["y"]), (3, 1 if game.mode != "2d" else 3))
    # Render
    if game.mode != "2d":
        colour = 12 if spawn_type == "enemy" else 11
        pg.draw.rect(rsurface, mgv.colours[colour], i)
    else:
        sprite = "game/enemy_2d" if spawn_type == "enemy" else "game/heal_2d"
        rsurface.blit(ast.assets_data[sprite], (spawn["x"], spawn["y"]))
    # Collisions
    if not game.paused and plr.colliderect(i):
        if spawn_type == "enemy":
            if not game.iframe:
                game.life -= 1
                game.iframe = True
                game.last_iframe_time = tick
                ast.assets_data["gameaud/hurt"].play()
                draw_notif(rsurface, "hurt", tick, game)
            else:
                new_enemies.append({"x": spawn["x"], "y": spawn["y"]})
        elif spawn_type == "heal":
            game.life += 1
            game.life = max(0, min(game.life, 5))
            ast.assets_data["gameaud/heal"].play()
            draw_notif(rsurface, "heal", tick, game)
    else:
        if spawn_type == "enemy":
            new_enemies.append({"x": spawn["x"], "y": spawn["y"]})
        elif spawn_type == "heal":
            new_heals.append({"x": spawn["x"], "y": spawn["y"]})
    if save_data['indicators']:
        sprite = "game/enemy_indicator" if spawn_type == "enemy" else \
            "game/heal_indicator"
        offset = con.enemy_indicator_offset if spawn_type == "enemy" else \
            con.heal_indicator_offset
        rsurface.blit(
            ast.assets_data[sprite],
            (spawn["x"] - 1, spawn["y"] - offset +
             (2 if game.mode == "2d" else 0)))
    return new_enemies, new_heals, game


def spawn_falling_objects(game):
    if not game.paused and etc.chance(con.falling_thing_chance):
        fall_type = get_falling_type(game)
        if fall_type in con.falling_hazards:
            x = rd.randint(int(game.plrx - con.falling_hazard_x_range),
                           int(game.plrx + con.falling_hazard_x_range))
        else:
            x = rd.randint(con.x_min, con.x_max)
        game.falls.append(  # Actually add
            {
                "x": x,
                "y": con.falling_object_init_y,
                "type": fall_type
            }
        )
    return game


def handle_falling_object(rsurface, tick, plr, new_falls, fall, game):
    # Create rect
    fall_rect = ast.assets_data[f"game/{fall['type']}"].get_rect()
    fall["y"] += 2 if not game.paused else 0
    fall_rect.x, fall_rect.y = fall["x"], fall["y"]
    rsurface.blit(ast.assets_data[f"game/{fall['type']}"],
                  fall_rect)  # Render
    # Collisions
    if not game.paused and plr.colliderect(fall_rect):
        if fall["type"] == "clear_enemies":
            ast.assets_data["gameaud/jump"].play()
            game.enemies = []
        elif fall["type"] == "max_life":
            ast.assets_data["gameaud/max_life"].play()
            game.life = 5
        elif fall["type"] == "max_jump":
            ast.assets_data["gameaud/jump"].play()
            game.last_jump = con.jump_init
        elif fall["type"] in con.falling_scorers:
            if fall["type"] == "-50_pts":
                ast.assets_data["gameaud/point_loss"].play()
            else:
                ast.assets_data["gameaud/scorer"].play()
                game.score += FALLING_SCORER_SCORE_RESULTS[fall["type"]]
        else:
            game.life = 0
            ast.assets_data["gameaud/falling_obj_kill"].play()
        if f"game/notif_{fall['type']}" in ast.assets_data:
            draw_notif(rsurface, fall["type"], tick, game)
    else:
        new_falls.append(fall)
    return game, new_falls


def spawn_lasers(game, tick):
    if not game.paused and etc.chance(con.laser_chance):
        game.lasers.append(
            {
                "x": game.plrx,
                "fired": False,
                "start_time": tick,
                "last_frame_change": tick,
                "frame": 2
            }
        )
        ast.assets_data["gameaud/laser_warn"].play()
    return game


def handle_laser(rsurface, tick, plr, new_lasers, laser, game):
    if not game.paused:
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
                    (laser["x"] - 3,
                     ast.assets_data["game/laser_1_top"].get_height())
                )
                if tick - laser["last_frame_change"] >= \
                   con.laser_frame_interval:
                    laser["frame"] = 1 if laser["frame"] == 2 else 2
                    laser["last_frame_change"] = tick
                if plr.colliderect(laser_rect):
                    game.life = 0
                else:
                    new_lasers.append(laser)
    else:
        laser["start_time"] += 1
        laser["last_frame_change"] += 1
        new_lasers.append(laser)
    return game, new_lasers


def do_spawns(rsurface, plr, game, tick):
    game = spawn_enemies_and_heals(game)

    # Heals & enemies
    new_enemies, new_heals = [], []
    for enemy in game.enemies:
        new_enemies, new_heals, game = handle_spawn(
            rsurface, tick, plr, new_enemies, new_heals, enemy, "enemy", game)
    for heal in game.heals:
        new_enemies, new_heals, game = handle_spawn(
            rsurface, tick, plr, new_enemies, new_heals, heal, "heal", game)
    game.enemies, game.heals = new_enemies, new_heals

    # Falling objects
    game = spawn_falling_objects(game)
    new_falls = []
    for fall in game.falls:
        game, new_falls = handle_falling_object(
            rsurface, tick, plr, new_falls, fall, game)
    game.falls = new_falls

    # Lasers
    game = spawn_lasers(game, tick)
    new_lasers = []
    for laser in game.lasers:
        game, new_lasers = handle_laser(
            rsurface, tick, plr, new_lasers, laser, game)
    game.lasers = new_lasers

    return game

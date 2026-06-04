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

# Lifeline.PYR v1.0.1.1

# Import libraries
import pygame as pg
import random as rd
import math

# Core modules
import mod.core.assets as ast
from mod.core.save import S

# Other modules
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc

# Game modules
from mod.stage.game.game import constants as con
from mod.stage.game import select

def get_falling_type(GAMEDATA):
    # Assuming there is a powerup, choose one
    if GAMEDATA["life"] <= 2 and not etc.chance(con.falling_ignore_pref_chance):
        powerup = "max_life"
        dire = True
    elif len(GAMEDATA["enemies"]) >= con.enemy_crowdedness and not etc.chance(con.falling_ignore_pref_chance):
        powerup = "clear_enemies"
        dire = True
    else:
        powerup = rd.choice(con.falling_powerups)
        dire = False

    # Determine if there should be a powerup
    powerup_chance = con.dire_falling_powerup_chance if dire else con.falling_powerup_chance

    # Return type
    if etc.chance(powerup_chance):
        return powerup
    else:
        return rd.choice(con.falling_hazards)


def do_spawns(rsurface, plr, GAMEDATA, tick):
    # Spawn enemies and heals
    if not GAMEDATA["paused"] and etc.chance(con.spawn_chance):
        addition = {
                "x": rd.randint(con.x_min, con.x_max),
                "y": 63 if select.game_type != "2d" else rd.randint(con.y_min, con.y_max)
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
            pg.draw.rect(rsurface, mgv.COLOURS[11], i)
        else:
            rsurface.blit(ast.ASSETS["game/enemy_2d"], (enemy["x"], enemy["y"]))
        # Collisions
        if not GAMEDATA["paused"] and plr.colliderect(i):
            if not GAMEDATA["iframe"]:
                GAMEDATA["life"] -= 1
                GAMEDATA["iframe"] = True
                GAMEDATA["last_iframe_time"] = tick
                ast.ASSETS["gameaud/hurt"].play()
        else:
            new_enemies.append({"x": enemy["x"], "y": enemy["y"]})
        if S['indicators']:
            rsurface.blit(
                ast.ASSETS['game/enemy_indicator'], 
                (enemy["x"] - 1, enemy["y"] - con.enemy_indicator_offset + (2 if select.game_type == "2d" else 0))
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
            pg.draw.rect(rsurface, mgv.COLOURS[10], i)
        else:
            rsurface.blit(ast.ASSETS["game/heal_2d"], (heal["x"], heal["y"]))
        # Collisions
        if not GAMEDATA["paused"] and plr.colliderect(i):
            GAMEDATA["life"] += 1
            ast.ASSETS["gameaud/heal"].play()
        else:
            new_heals.append({"x": heal["x"], "y": heal["y"]})
        if S['indicators']:
            rsurface.blit(
                ast.ASSETS['game/heal_indicator'], 
                (heal["x"] - 1, heal["y"] - con.heal_indicator_offset + (2 if select.game_type == "2d" else 0))
            )
            
    # Update data
    GAMEDATA["enemies"], GAMEDATA["heals"] = new_enemies, new_heals
    GAMEDATA["life"] = max(0, min(GAMEDATA["life"], 5))

    # Spawn falling things
    if not GAMEDATA["paused"] and etc.chance(con.falling_thing_chance):
        typr = get_falling_type(GAMEDATA)
        if typr in con.falling_hazards:
            x = rd.randint(int(GAMEDATA["plrx"] - con.falling_hazard_x_range), int(GAMEDATA["plrx"] + con.falling_hazard_x_range))
        else:
            x = rd.randint(con.x_min, con.x_max)
        GAMEDATA["falls"].append( # Actually add
            {
                "x": x,
                "y": con.falling_object_init_y,
                "type": typr
            }  
        )

    # Handle each fall
    new_falls = []
    for fall in GAMEDATA["falls"]:
        # Create rect
        fall_rect = ast.ASSETS[f"game/{fall['type']}"].get_rect()
        fall["y"] += 2 if not GAMEDATA["paused"] else 0
        fall_rect.x, fall_rect.y = fall["x"], fall["y"]
        rsurface.blit(ast.ASSETS[f"game/{fall['type']}"], fall_rect) # Render
        # Collisions
        if not GAMEDATA["paused"] and plr.colliderect(fall_rect):
            if fall["type"] == "clear_enemies":
                ast.ASSETS["gameaud/jump"].play()
                GAMEDATA["enemies"] = []
            elif fall["type"] == "max_life":
                ast.ASSETS["gameaud/heal"].play()
                GAMEDATA["life"] = 5
            elif fall["type"] == "max_jump":
                ast.ASSETS["gameaud/jump"].play()
                GAMEDATA["last_jump"] = con.jump_init
            else:
                GAMEDATA["life"] = 0
                ast.ASSETS["gameaud/falling_obj_kill"].play()
        else:
            new_falls.append(fall)
    GAMEDATA["falls"] = new_falls

    # Spawn lasers
    if not GAMEDATA["paused"] and etc.chance(con.laser_chance):
        GAMEDATA["lasers"].append (
            {
                "x": GAMEDATA["plrx"],
                "fired": False,
                "start_time": tick,
                "last_frame_change": tick,
                "frame": 2
            }
        )
        ast.ASSETS["gameaud/laser_warn"].play()

    # Handle lasers
    new_lasers = []
    for laser in GAMEDATA["lasers"]:
        if not GAMEDATA["paused"]:
            if not tick - laser["start_time"] >= con.laser_end_time:
                if not laser["fired"]:
                    if tick - laser["start_time"] >= con.laser_fire_time:
                        laser["fired"] =  True
                        laser["fire_time"] = tick
                        ast.ASSETS["gameaud/laser_strike"].play()
                    else:
                        rsurface.blit(
                            ast.ASSETS["game/laser_warn"],
                            (laser["x"] - 2, con.laser_warn_y_pos - ast.ASSETS["game/laser_warn"].get_height())
                        )
                    new_lasers.append(laser)
                else:
                    laser_rect = ast.ASSETS["game/laser_1_top"].get_rect()
                    laser_rect.x, laser_rect.y = laser["x"], 0
                    rsurface.blit(ast.ASSETS[f"game/laser_{laser['frame']}_top"], laser_rect)
                    laser_rect.height = rsurface.get_height()
                    rsurface.blit(
                        ast.ASSETS[f"game/laser_{laser['frame']}_bottom"],
                        (laser["x"] - 2, ast.ASSETS["game/laser_1_top"].get_height())
                    )
                    if tick - laser["last_frame_change"] >= con.laser_frame_interval:
                       laser["frame"] = 1 if laser["frame"] == 2 else 2
                       laser["last_frame_change"] = tick
                    if plr.colliderect(laser_rect):
                        GAMEDATA["life"] = 0
                    else:
                        new_lasers.append(laser)
                if tick - laser["start_time"] >= con.laser_fire_time and tick - laser["start_time"] <= con.laser_flash_time:
                    flash_rect = pg.Rect(0, 0, rsurface.get_width(), rsurface.get_height())
                    pg.draw.rect(rsurface, mgv.COLOURS[18], flash_rect)
        else:
            laser["start_time"] += 1
            laser["last_frame_change"] += 1
            new_lasers.append(laser)
    GAMEDATA["lasers"] = new_lasers
        
    return GAMEDATA

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

# Import game module
from mod.stage.game import select

# core_updates
life_depletion_time = 60
score_increment = 50
iframe_end_time = 10

# spawns
spawn_chance = 4.7
enemy_indicator_offset = 6
heal_indicator_offset = 8
falling_thing_chance = 1
dire_falling_thing_chance = 3.5
falling_powerup_chance = 10
dire_falling_powerup_chance = 80
falling_hazards = [
    "ow_a", "ow_b"
]
falling_powerups = [
    "max_life", "clear_enemies", "max_jump"
]
falling_ignore_pref_chance = 10
enemy_crowdedness = 12 # How many enemies needed until a clear_enemies powerup is considered
falling_hazard_x_range = 55
falling_object_init_y = -9 # Right above the screen
jump_init = -300
laser_chance = 0.2
laser_fire_time = 80
laser_frame_interval = 5
laser_end_time = 179
laser_warn_y_pos = 59
laser_flash_time = 10

# inputx
plrx_slow_mod = 1
plrx_norm_mod = 3
dash_decrement = 12
dash_multiplier = 3.5
dash_constant_increment = 0.7
dash_max = 106 # Pixel length of the dash bar
inertia_base_plrx_divisor = 3
inertia_divisor_slow = 2
inertia_divisor_norm = 5
jump_tick_end = 60
jump_cooldown_time = 300

# player
jumpend_marker = 45
pointer_y = 55

# Global
dash_functioning_min = 10

# Game type dependent
def do_depend():
    global x_min, x_max, y_min, y_max
    x_min = 4 if select.game_type == "normal_game" else 42
    x_max = 249 if select.game_type == "normal_game" else 211
    y_min = 64 if select.game_type == "normal_game" else 19
    y_max = 64 if select.game_type == "normal_game" else 107   

# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

from mod.core import args
import mod.etc.BTXT as B
from cerbose import cprint
import json

# core_updates
score_increment = 50
iframe_end_time = 10
life_depletion_time = 60
life_depletion_time_intense = 30
score_multipliers = [None, 0.8, 1, 1.2, 1.2]

# spawns
spawn_chance = 4.7
spawn_chance_intense = 6.8
enemy_chance_hard = 60
enemy_chance_easy = 40
enemy_chance_normal = 50
enemy_indicator_offset = 6
heal_indicator_offset = 8
falling_thing_chance = 1
dire_falling_thing_chance = 3.5
falling_powerup_chance = 10
falling_scorer_chance = 25
dire_falling_powerup_chance = 80
falling_hazards = ["ow_a", "ow_b"]
falling_powerups = ["max_life", "clear_enemies", "max_jump"]
falling_scorers = ["-50_pts", "25_pts", "50_pts", "100_pts"]
falling_ignore_pref_chance = 10
enemy_crowdedness = 12  # How many enemies needed until a clear_enemies powerup
                        # is considered
falling_hazard_x_range = 55
falling_object_init_y = -9  # Right above the screen
jump_init = -300
laser_chance = 0.2
laser_fire_time = 80
laser_frame_interval = 5
laser_end_time = 179
laser_warn_y_pos = 59

# inputx
plrx_slow_mod = 1
plrx_norm_mod = 3
dash_decrement = 12
dash_multiplier = 3.5
dash_constant_increment = 0.7
dash_max = 106  # Pixel length of the dash bar
inertia_base_plrx_divisor = 3
inertia_divisor_slow = 2
inertia_divisor_norm = 5
jump_tick_end = 60
jump_cooldown_time = 300

# player
jumpend_marker = 45
pointer_y = 55

# ui
show_pts_time = 10
show_pts_y_offset = 7

# Global
dash_functioning_min = 10


# Game type dependent
def do_depend(mode):
    global x_min, x_max, y_min, y_max
    x_min = 4 if mode == "normal_game" else 42
    x_max = 249 if mode == "normal_game" else 211
    y_min = 64 if mode == "normal_game" else 19
    y_max = 64 if mode == "normal_game" else 107

    # Additionally, check for constants to override
    if args.constants_override:
        try:
            with open("constants.json", "r") as f:
                override = json.load(f)
            cprint("info", "Overriding constants.")
            cprint("warn", "If the game crashes, it is your fault!")
            for var in override:
                globals()[var] = override[var]
        except FileNotFoundError:
            B.bottom_text = "Cannot override constants as file does not exist."
            cprint("error",
                   "Cannot override constants as file does not exist.")

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
import pygame as pg
import yaml

# Core modules
from mod.core.save import S, wr
import mod.core.assets as ast

# Other modules
from mod.etc.options_data import OPTS
from mod.etc.magicvars import COLOURS
import mod.etc.etcils as etc
import mod.etc.BTXT as B

# Main variables
global sel, lkpt, DESC
sel, lkpt = 1, 0

def get_numeric_key_value(key): # Turn bools into ints
    return int(key) if isinstance(key, bool) else int(key)

def get_option_clamp(value): # Parse the 'clamp' in options_data
    clamp = OPTS[sel]['clamp'].split(',')
    return max(int(clamp[0]), min(value, int(clamp[1])))

def ACT(rsurface, keys, tick, stage_history):
    global sel, lkpt

    desc_y_start = 42

    # Initialize
    if tick <= 1:
        lkpt = 0

    item_count = OPTS['count'] + 1

    rsurface.blit(ast.ASSETS['opts/bg'], (0, 0))
    if tick > 10:
        # Render text
        text = ast.ASSETS['font1'].render("OPTIONS", False, COLOURS[18])
        rsurface.blit(text, (5, 4))
        # Options list
        for i in range(1, item_count):
            etc.MKTX(rsurface, sel, i, f"`{i} {OPTS[i]['name']}", "options")
        etc.MKTX(rsurface, sel, item_count, "BACK", "options")

        # Show description
        if sel != item_count:
            #? Keeping this just in case it ever ends up useful
            # left = S[OPTS[sel]['key']] - 1
            # left = get_option_clamp(left)
            # left = OPTS[sel]['call'][left]
            # right = S[OPTS[sel]['key']] + 1
            # right = get_option_clamp(right)
            # right = OPTS[sel]['call'][right]

            desc_text = (
                OPTS[sel]['desc']
                + "]]]]Use left/right arrows]]to change."
                + f"]]Currently set to:]]{OPTS[sel]['call'][S[OPTS[sel]['key']]]}"
                # + f"]]LEFT: {left}]]RIGHT:{right}"
            )
            lines = desc_text.split(']]')
            y = desc_y_start
            for line in lines:
                text = ast.ASSETS['font1'].render(line, False, COLOURS[18], COLOURS[0])
                rsurface.blit(text, (119, y))
                y += 6

        # Take input
        # Scroll
        if keys[pg.K_DOWN] and etc.srp(tick, lkpt):
            sel += 1
            lkpt = tick
            ast.ASSETS['mainaud/blip'].play()
        elif keys[pg.K_UP] and etc.srp(tick, lkpt):
            sel -= 1
            lkpt = tick
            ast.ASSETS['mainaud/blip'].play()
        # Change option value
        sel = max(1, min(sel, item_count))
        if sel != item_count: # Ignore controls that do not apply to BACK
            new_value = get_numeric_key_value(S[OPTS[sel]['key']])
            if keys[pg.K_LEFT] and etc.srp(tick, lkpt):
                new_value -= 1
                lkpt = tick
                ast.ASSETS['mainaud/blip'].play()
            if keys[pg.K_RIGHT] and etc.srp(tick, lkpt):
                new_value += 1
                lkpt = tick
                ast.ASSETS['mainaud/blip'].play()
            new_value = get_option_clamp(new_value)
            if OPTS[sel]['bool']:
                new_value = bool(new_value)
            og_value = S[OPTS[sel]['key']]
            S[OPTS[sel]['key']] = new_value

            # Check if display needs to be remade
            keys_needing_remade_disp = ['fullscreen', 'winscale']
            if OPTS[sel]['key'] in keys_needing_remade_disp and og_value != new_value:
                return "remake_display"

        # Leave
        if keys[pg.K_RETURN] and sel == item_count:
            ast.ASSETS['mainaud/blip'].play()
            wr(S)
            return stage_history[-2]

    # RESET LKPT if needed
    if keys[pg.K_l]:
        lkpt = 0
        B.BTX = "Reset LKPT."

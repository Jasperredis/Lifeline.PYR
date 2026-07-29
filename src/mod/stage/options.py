# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
from mod.core.save import save_data, write_save
import mod.core.assets as ast
from mod.etc.options_data import OPTS
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
import mod.etc.BTXT as B

global sel, lkpt, DESC
sel, lkpt = 1, 0


def get_numeric_key_value(key):  # Turn bools into ints
    return int(key) if isinstance(key, bool) else int(key)


def get_option_clamp(value):  # Parse the 'clamp' in options_data
    clamp = OPTS[sel]['clamp'].split(',')
    return max(int(clamp[0]), min(value, int(clamp[1])))


def act(rsurface, keys, tick, stage_history):
    global sel, lkpt
    desc_y_start = 42
    # Initialize
    if tick <= 1:
        lkpt = 0
    item_count = OPTS['count'] + 1

    rsurface.blit(ast.assets_data['opts/bg'], (0, 0))
    if tick > 10:
        # Render text
        text = ast.assets_data['font1'].render("OPTIONS", False, mgv.colours[19])
        rsurface.blit(text, (5, 4))
        # Options list
        for i in range(1, item_count):
            etc.MKTX(rsurface, sel, i, f"`{i} {OPTS[i]['name']}", "options")
        etc.MKTX(rsurface, sel, item_count, "BACK", "options")

        # Show description
        if sel != item_count:
            # Keeping this just in case it ever ends up useful
            # left = save_data[OPTS[sel]['key']] - 1
            # left = get_option_clamp(left)
            # left = OPTS[sel]['call'][left]
            # right = save_data[OPTS[sel]['key']] + 1
            # right = get_option_clamp(right)
            # right = OPTS[sel]['call'][right]

            desc_text = (
                OPTS[sel]['desc']
                + "]]]]Use left/right arrows]]to change."
                + f"]]Currently set to:]]{OPTS[sel]['call'][save_data[OPTS[sel]['key']]]}"
                # + f"]]LEFT: {left}]]RIGHT:{right}"
            )
            lines = desc_text.split(']]')
            y = desc_y_start
            for line in lines:
                if line.startswith("$"):
                    image = ast.assets_data[f'opts/{line[1:]}']
                    rsurface.blit(image, (119, y))
                else:
                    text = ast.assets_data['font1'].render(line, False, mgv.colours[19], mgv.colours[1])
                    rsurface.blit(text, (119, y))
                y += 6

        # Take input
        # Scroll
        if keys[pg.K_DOWN] and etc.srp(tick, lkpt):
            sel += 1
            lkpt = tick
            ast.assets_data['mainaud/blip'].play()
        elif keys[pg.K_UP] and etc.srp(tick, lkpt):
            sel -= 1
            lkpt = tick
            ast.assets_data['mainaud/blip'].play()
        # Change option value
        sel = max(1, min(sel, item_count))
        if sel != item_count:  # Ignore controls that do not apply to BACK
            new_value = get_numeric_key_value(save_data[OPTS[sel]['key']])
            if keys[pg.K_LEFT] and etc.srp(tick, lkpt):
                new_value -= 1
                lkpt = tick
                ast.assets_data['mainaud/blip'].play()
            if keys[pg.K_RIGHT] and etc.srp(tick, lkpt):
                new_value += 1
                lkpt = tick
                ast.assets_data['mainaud/blip'].play()
            new_value = get_option_clamp(new_value)
            if OPTS[sel]['bool']:
                new_value = bool(new_value)
            og_value = save_data[OPTS[sel]['key']]
            save_data[OPTS[sel]['key']] = new_value

            # Check if display or assets need to be remade
            KEYS_NEEDING_REMADE_DISPLAY = ['fullscreen', 'winscale']
            if OPTS[sel]['key'] in KEYS_NEEDING_REMADE_DISPLAY \
               and og_value != new_value:
                return "remake_display"
            KEYS_NEEDING_ASSET_RELOAD = ['palette']
            if OPTS[sel]['key'] in KEYS_NEEDING_ASSET_RELOAD \
               and og_value != new_value:
                ast.load_assets(only_images=True)
        # Leave
        if keys[pg.K_RETURN] and sel == item_count:
            ast.assets_data['mainaud/blip'].play()
            write_save(save_data)
            return stage_history[-2]
    # RESET LKPT if needed
    if keys[pg.K_l]:
        lkpt = 0
        B.bottom_text = "Reset LKPT."

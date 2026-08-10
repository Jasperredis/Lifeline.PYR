# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
from mod.core.save import save_data, write_save
import mod.core.assets as ast
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
import mod.etc.BTXT as B

sel, lkpt = 1, 0
OPTS = {
    "count": 11,
    1: {
        "desc": "Use one of 9]]background options of]]various colours.]]\
$opts/bg_preview",
        "key": "bg",
        "name": "Background",
        "call": {
            1: "Main",
            2: "Alt",
            3: "Alt 2",
            4: "Cotton Candy",
            5: "Blood",
            6: "Cyber",
            7: "Green",
            8: "Red",
            9: "Rust",
            10: "Sand",
            11: "Thunder",
            12: "rain.",
            13: "Engine",
            14: "Jrises",
            15: "Wave",
            16: "Sohappy",
            17: "Deer",
            18: "Nothing",
            19: "Wire",
            20: "Palette Test"
        },
        "clamp": "1,20",
        "bool": False,
    },
    2: {
        "desc": "Use one of 5 colour]]palette options.]]$opts/colour_preview",
        "key": "palette",
        "name": "Colour palette",
        "call": {
            1: "Canonical",
            2: "Classic",
            3: "Inverted",
            4: "Warm",
            5: "Intense"
        },
        "clamp": "1,5",
        "bool": False,
    },
    3: {
        "desc": "Change the appearance]]of the mouse.",
        "key": "mouse-theme",
        "name": "Mouse theme",
        "call": {
            1: "Default",
            2: "Inverted",
            3: "Visibility",
            4: "Arrow",
            5: "Arrow (vis.)",
            6: "Block",
            7: "Block (vis.)",
            8: "L",
            9: "L (vis.)",
            10: "Small",
            11: "Rainbow",
            12: "Rainbow alt"
        },
        "clamp": "1,12",
        "bool": False
    },
    4: {
        "desc": "Move the player with]]your mouse instead]]of keys.",
        "key": "mouse-move",
        "name": "Mouse movement",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True
    },
    5: {
        "desc": "Change the soundtrack]]selection.",
        "key": "ost",
        "name": "Soundtrack",
        "call": {
            1: "Lifeline.PYR (Game A)",
            2: "Lifeline.PYR (Game B)",
            3: "Lifeline.PYR (Bonus)",
            4: "Alternate",
            5: "Lifeline.py"
        },
        "clamp": "1,5",
        "bool": False
    },
    6: {
        "desc": "Scale the window to]]fit your screen.",
        "key": "winscale",
        "name": "Window size",
        "call": {
            1: "1x (256x144) / Base",
            2: "2x (512x288)",
            3: "3x (768x432)",
            4: "4x (1024x576) / Def",
            5: "5x (1280x720) / 720p",
            6: "6x (1536x864)",
            7: "7x (1792x1008) / ~1080p",
            8: "8x (2048x1152)",
            9: "9x (2304x1296)",
            10: "10x (2560x1440) / 1440p",
            11: "11x (2816x1584)",
            12: "12x (3072x1728) ~3k",
        },
        "clamp": "1,12",
        "bool": False,
    },
    7: {
        "desc": "Change the chance of]]enemy spawns.",
        "key": "dif",
        "name": "Difficulty",
        "call": {1: "Mostly heals", 2: "Balanced", 3: "Mostly enemies"},
        "clamp": "1,3",
        "bool": False,
    },
    8: {
        "desc": "Self-explanatory.",
        "key": "fullscreen",
        "name": "Fullscreen",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    9: {
        "desc": "Gives the player]]velocity physics.",
        "key": "inertia",
        "name": "Inertia",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    10: {
        "desc": "Shows icons where]]heals and enemies]]are.",
        "key": "indicators",
        "name": "Indicators",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    11: {
        "desc": "Shows the velocity of]]the player if inertia]]is enabled.",
        "key": "velocity-icon",
        "name": "Velocity icon",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    12: {
        "desc": "Changes the colours in]]the HOW TO PLAY menu.",
        "key": "htp-theme",
        "name": "HTP theme",
        "call": {
            1: "Black-on-White",
            2: "Sand",
            3: "Ocean",
            4: "Watermelon",
            5: "White-on-Black",
            6: "Demo",
            7: "Original"
        },
        "clamp": "1,7",
        "bool": False,
    }
}


def get_numeric_key_value(key):  # Turn bools into ints
    return int(key) if isinstance(key, bool) else int(key)


def get_option_clamp(value):  # Parse the 'clamp' in options_data
    clamp = OPTS[sel]['clamp'].split(',')
    return max(int(clamp[0]), min(value, int(clamp[1])))


def take_input(keys, tick, stage_history):
    global sel, lkpt
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
    return None


def show_screen(rsurface):
    # Title
    text = ast.assets_data['font1'].render("OPTIONS", False, mgv.colours[19])
    rsurface.blit(text, (5, 4))
    # Options list
    for i in range(1, item_count):
        etc.mk_text_option(rsurface, sel, i, f"{i} {OPTS[i]['name']}",
                           mgv.colours[19], False, 5)
    etc.mk_text_option(rsurface, sel, item_count, "BACK", mgv.colours[19],
                       False, 5)
    # Show description
    if sel != item_count:
        current = OPTS[sel]['call'][save_data[OPTS[sel]['key']]]
        desc_text = (
            OPTS[sel]['desc']
            + "]]]]Use left/right arrows]]to change."
            + f"]]Currently set to:]]{current}"
        )
        lines = desc_text.split(']]')
        DESC_X, DESC_Y = 119, 42
        for y, line in enumerate(lines):
            if line.startswith("$"):
                image = ast.assets_data[line[1:]]
                rsurface.blit(image, (DESC_X, DESC_Y + (y * 6)))
            else:
                text = ast.assets_data['font1'].render(
                    line, False, mgv.colours[19], mgv.colours[1])
                rsurface.blit(text, (DESC_X, DESC_Y + (y * 6)))


def act(rsurface, keys, tick, stage_history):
    global lkpt, item_count
    # Initialize
    if tick <= 1:
        lkpt = 0
    item_count = OPTS['count'] + 1

    # RESET LKPT if needed
    if keys[pg.K_l]:
        lkpt = 0
        B.bottom_text = "Reset LKPT."

    rsurface.blit(ast.assets_data['opts/bg'], (0, 0))
    if tick > 5:
        show_screen(rsurface)
        return take_input(keys, tick, stage_history)

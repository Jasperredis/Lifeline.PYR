# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
from mod.core.save import save_data, write_save, keyb, DEFAULT_SAVE
import mod.core.assets as ast
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
import mod.etc.BTXT as B

sel, lkpt = 1, 0
OPTS = [
    {
        "desc": "Use one of 21]]background options.",
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
            12: "Rain",
            13: "Engine",
            14: "Jrises",
            15: "Wave",
            16: "Sohappy",
            17: "Deer",
            18: "Nothing",
            19: "Wire",
            20: "Palette Test",
            21: "Gradient"
        },
        "clamp": "1,21",
        "bool": False,
    },
    {
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
    {
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
    {
        "desc": "Move the player with]]your mouse instead]]of keys.",
        "key": "mouse-move",
        "name": "Mouse movement",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True
    },
    {
        "desc": "Navigate menus with]]your mouse.]]You may still use the]]\
keyboard with this on.]]Can be buggy!",
        "key": "mouse-nav",
        "name": "Mouse menu nav",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True
    },
    {
        "desc": "Change the soundtrack]]selection.",
        "key": "ost",
        "name": "Soundtrack",
        "call": {
            1: "Lifeline.PYR (Game A)",
            2: "Lifeline.PYR (Game B)",
            3: "Lifeline.PYR (Bonus)",
            4: "Lifeline.py",
            5: "No music"
        },
        "clamp": "1,5",
        "bool": False
    },
    {
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
    {
        "desc": "Make the game harder.]]Or easier.]]Score bonuses and\
]]pentalties apply.",
        "key": "dif",
        "name": "Difficulty",
        "call": {1: "Easy", 2: "Normal", 3: "Hard", 4: "Intense"},
        "clamp": "1,4",
        "bool": False,
    },
    {
        "desc": "Self-explanatory.",
        "key": "fullscreen",
        "name": "Fullscreen",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    {
        "desc": "Gives the player]]velocity physics.",
        "key": "inertia",
        "name": "Inertia",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    {
        "desc": "Shows icons where]]heals and enemies]]are.",
        "key": "indicators",
        "name": "Indicators",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    {
        "desc": "Shows the velocity of]]the player if inertia]]is enabled.",
        "key": "velocity-icon",
        "name": "Velocity icon",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    {
        "desc": "Plays a sound every]]time your life ticks.",
        "key": "life-tick-sound",
        "name": "Life tick sound",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    {
        "desc": "Show small pop-up]]numbers/symbols]]upon gaining/losing]]\
points or hitting]]falling objects.",
        "key": "notifs",
        "name": "Notifs",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True
    }
]
KEYS = [
    {
        "name": "Menu Up",
        "key": "menu-up"
    },
    {
        "name": "Menu Down",
        "key": "menu-down"
    },
    {
        "name": "Menu Left",
        "key": "menu-left"
    },
    {
        "name": "Menu Right",
        "key": "menu-right"
    },
    {
        "name": "Menu Increase",
        "key": "menu-increase"
    },
    {
        "name": "Menu Decrease",
        "key": "menu-decrease"
    },
    {
        "name": "Menu Exit",
        "key": "menu-exit"
    },
    {
        "name": "Screenshot",
        "key": "screenshot"
    },
    {
        "name": "Game Move Left",
        "key": "game-move-left"
    },
    {
        "name": "Game Move Right",
        "key": "game-move-right"
    },
    {
        "name": "Game Move Up (2D)",
        "key": "game-2d-move-up"
    },
    {
        "name": "Game Move Down (2D)",
        "key": "game-2d-move-down"
    },
    {
        "name": "Game Jump (1D)",
        "key": "game-1d-jump"
    },
    {
        "name": "Game Slow/Land (1D)",
        "key": "game-1d-slow"
    },
    {
        "name": "Game Jump (2D)",
        "key": "game-2d-jump"
    },
    {
        "name": "Game Slow/Land (2D)",
        "key": "game-2d-slow"
    },
    {
        "name": "Game Dash",
        "key": "game-dash"
    },
    {
        "name": "Game Pause",
        "key": "game-pause"
    }
]
setting_key = False


def get_numeric_key_value(key):  # Turn bools into ints
    return int(key) if isinstance(key, bool) else int(key)


def get_option_clamp(value):  # Parse the 'clamp' in options_data
    clamp = OPTS[sel - 1]['clamp'].split(',')
    return max(int(clamp[0]), min(value, int(clamp[1])))


def take_input(keys, key, tick, stage_history, context):
    global sel, lkpt, setting_key
    data = OPTS if context == "options" else KEYS
    # Scroll
    if keyb(keys, "menu-down") and etc.srp(tick, lkpt):
        sel += 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    elif keyb(keys, "menu-up") and etc.srp(tick, lkpt):
        sel -= 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    sel = max(1, min(sel, item_count))
    # Change option value
    if context == "options" and (
            keyb(keys, "menu-increase") or keyb(keys, "menu-decrease")):
        new_value = get_numeric_key_value(save_data[data[sel - 1]['key']])
        if keyb(keys, "menu-decrease") and etc.srp(tick, lkpt):
            new_value -= 1
            lkpt = tick
            ast.assets_data['mainaud/blip'].play()
        if keyb(keys, "menu-increase") and etc.srp(tick, lkpt):
            new_value += 1
            lkpt = tick
            ast.assets_data['mainaud/blip'].play()
        new_value = get_option_clamp(new_value)
        if data[sel - 1]['bool']:
            new_value = bool(new_value)
        og_value = save_data[data[sel - 1]['key']]
        save_data[data[sel - 1]['key']] = new_value

        # Check if display or assets need to be remade
        KEYS_NEEDING_REMADE_DISPLAY = ['fullscreen', 'winscale']
        if data[sel - 1]['key'] in KEYS_NEEDING_REMADE_DISPLAY \
           and og_value != new_value:
            return "remake_display"
        KEYS_NEEDING_ASSET_RELOAD = ['palette']
        if data[sel - 1]['key'] in KEYS_NEEDING_ASSET_RELOAD \
           and og_value != new_value:
            ast.load_assets(only_images=True)
    elif context == "keybindings":
        if keys[pg.K_r]:
            save_data["keybindings"] = DEFAULT_SAVE["keybindings"]
        elif setting_key:
            if key is not None:
                save_data["keybindings"][data[sel - 1]["key"]] = \
                    pg.key.name(key)
                setting_key = False
        elif keys[pg.K_RETURN] and not setting_key:
            setting_key = True
    # Leave
    if keyb(keys, "menu-exit"):
        ast.assets_data['mainaud/blip'].play()
        write_save(save_data)
        return stage_history[-2]
    return None


def show_screen(rsurface, context, mx, my):
    global sel
    data = OPTS if context == "options" else KEYS
    # Background
    bg_asset = "opts/bg-keys" if context == "keybindings" else "opts/bg"
    rsurface.blit(ast.assets_data[bg_asset], (0, 0))
    # Title
    title_text = "KEYBINDINGS" if context == "keybindings" else "OPTIONS"
    text = ast.assets_data['font1'].render(title_text, False, mgv.colours[19])
    rsurface.blit(text, (5, 4))
    # Options list
    for i in range(item_count):
        rect = etc.mk_text_option(rsurface, sel, i + 1, data[i]['name'],
                                  mgv.colours[19], False, 5, return_rect=True)
        # I have genuinely no idea why I need "- 8" in the condition below, but
        # it wasn't working and I just tried that to see if it'd work and it
        # just did????
        if save_data["mouse-nav"] and rect.collidepoint(mx, my - 8):
            sel = i + 1
    # Show description
    current = data[sel - 1]['call'][save_data[data[sel - 1]['key']]] \
        if context == "options" else (
           save_data["keybindings"][data[sel - 1]['key']])
    exit_key = save_data['keybindings']['menu-exit'].upper()
    desc_text = (
        data[sel - 1]['desc']
        + "]]]]Use left/right arrows]]to change."
        + f"]]Currently set to:]]{current}"
        + f"]]]]Press [{exit_key}] to leave."
    ) if context == "options" else (
        "Press [RETURN] ]]"
        + "followed by any key]]to set to said key."
        + f"]]]]Currently set to:]][{current.upper()}] "
        + f"]]]]Press [{exit_key}] to leave.]]]]"
        + "Press [R] to reset]]all keybindings (you]]"
        + "may have to restart]]the game)."
    )
    lines = desc_text.split(']]')
    DESC_X = 119 if context == "options" else 128
    DESC_Y = 42 if context == "options" else 46
    for y, line in enumerate(lines):
        if line.startswith("$"):
            image = ast.assets_data[line[1:]]
            rsurface.blit(image, (DESC_X, DESC_Y + (y * 6)))
        else:
            text = ast.assets_data['font1'].render(
                line, False, mgv.colours[19], mgv.colours[1])
            rsurface.blit(text, (DESC_X, DESC_Y + (y * 6)))


def act(rsurface, keys, key, tick, mx, my, stage_history, context):
    global lkpt, item_count, sel, setting_key
    # Initialize
    if tick <= 1:
        lkpt = 0
        sel = 1
        setting_key = False
    if tick < 5:
        return
    item_count = len(KEYS) if context == "keybindings" else len(OPTS)

    # RESET LKPT if needed
    if keys[pg.K_l]:
        lkpt = 0
        B.bottom_text = "Reset LKPT."

    show_screen(rsurface, context, mx, my)
    return take_input(keys, key, tick, stage_history, context)

# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
from mod.core.save import save_data, keyb

sel = 1
lkpt = 0
game_type = None

def act(rsurface, keys, tick, mx, my, mb):
    global sel, lkpt, game_type

    # Fix lkpt
    if lkpt > tick:
        lkpt = 0

    # Show top text
    text_y = 4
    text_surf = ast.assets_data['font1'].render(
        "Select Game Type:", False, mgv.colours[19], mgv.colours[1]
    )
    rsurface.blit(
        text_surf, (etc.centrexy(text_surf, onecoord='x'), text_y)
    )

    # Get input
    if keyb(keys, "menu-right") and etc.srp(tick, lkpt):
        sel += 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    elif keyb(keys, "menu-left") and etc.srp(tick, lkpt):
        sel -= 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    sel = max(1, min(sel, 3))

    # Options
    # Base variables
    opt_y = etc.centrexy(ast.assets_data['game/normal_game'], onecoord='y')
    base_x_offset = 11
    options = ["normal_game", "2d", "back"]
    return_chart = {
        "normal_game": "game",
        "2d": "game",
        "back": "back"
    }
    count = 0
    closeness = 7
    # Render & act
    for i in options:
        count += 1
        # Get position
        y = opt_y - 2 if sel == count else opt_y
        x = base_x_offset + (
            ast.assets_data['game/normal_game'].get_width() *
            0.75 *
            (count - 1)
        ) - (count * closeness)
        # Render
        rect = ast.assets_data[f"game/{i}"].get_rect(topleft=(x, y))
        rsurface.blit(ast.assets_data[f"game/{i}"], rect)
        if save_data["mouse-nav"] and rect.collidepoint(mx, my - 8):
            sel = count
        # Act
        if ((keys[pg.K_RETURN] or (save_data["mouse-nav"] and mb[0]))
                and etc.srp(tick, lkpt) and sel == count):
            lkpt = tick
            ast.assets_data['mainaud/blip'].play()
            game_type = i
            return return_chart[i]

    # Exit if the user didn't select anything
    return "select"

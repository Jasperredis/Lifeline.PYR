# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.0.1

import pygame as pg
import mod.core.assets as ast
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc

sel = 1
lkpt = 0
game_type = None

def ACT(rsurface, keys, tick):
    global sel, lkpt, game_type

    # Fix lkpt
    if lkpt > tick:
        lkpt = 0

    # Show top text
    text_y = 4
    text_surf = ast.ASSETS['font1'].render(
        "Select Game Type:", False, mgv.COLOURS[18], mgv.COLOURS[0]
    )
    rsurface.blit(
        text_surf, (etc.centrexy(text_surf, onecoord='x'), text_y)
    )

    # Get input
    if keys[pg.K_RIGHT] and etc.srp(tick, lkpt):
        sel += 1
        lkpt = tick
        ast.ASSETS['mainaud/blip'].play()
    elif keys[pg.K_LEFT] and etc.srp(tick, lkpt):
        sel -= 1
        lkpt = tick
        ast.ASSETS['mainaud/blip'].play()
    sel = max(1, min(sel, 3))

    # Options
    # Base variables
    opt_y = etc.centrexy(ast.ASSETS['game/normal_game'], onecoord='y')
    base_x_offset = 11
    options = ["normal_game", "2d", "back"]
    return_chart = {
        "normal_game": "game",
        "2d": "game",
        "back": "back"
    }
    count = 0
    closeness = 7 # i was gonna give this a funny name but decided against it
    # Render & act
    for i in options:
        count += 1
        # Get position
        y = opt_y - 2 if sel == count else opt_y
        x = base_x_offset + (
            ast.ASSETS['game/normal_game'].get_width() * 
            0.75 * 
            (count - 1)
        ) - ( count * closeness )
        # Render
        rsurface.blit(ast.ASSETS[f"game/{i}"], (x, y))
        # Act
        if keys[pg.K_RETURN] and etc.srp(tick, lkpt) and sel == count:
            lkpt = tick
            ast.ASSETS['mainaud/blip'].play()
            game_type = i
            return return_chart[i]

    # Exit if the user didn't select anything
    return "select"

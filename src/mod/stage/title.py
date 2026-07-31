# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import webbrowser
import mod.core.assets as ast
from mod.core.save import save_data
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
import mod.etc.BTXT as B

friction, sel, lkpt = 1, 1, 0
stats, done_text, done_animation, show_cat = False, False, False, False
INTRO_TEXT = """
Welcome to Lifeline.PYR!
Made by jasperredis, in open-source.
See info at:
- Github     : https://github.com/jasperredis/Lifeline.PYR
- Website    : https://lifelinepyr.jasperredis.net
- Itch.io    : https://jasperredis.itch.io/lifelinepyr
- jasperredis: https://www.jasperredis.net
This game is licensed under the GNU General Public License v3.0 or later.
For more information, do any of the following:
- Visit the packaged LICENSE file
- See the 'License' section on the 'ABOUT' screen
- Go to the GNU website at: https://gnu.org/licenses/gpl-3.0.en.html
----
Lifeline.PYR  Copyright (C) 2025  jasperredis
This program comes with ABSOLUTELY NO WARRANTY; for details, see the GPLv3.
This is free software, and you are welcome to redistribute it
under certain conditions; see the GPLv3 for details.
"""
HOW_TO_PLAY_URL = "https://lifelinepyr.jasperredis.net/how-to-play.html"
WEBSITE_URL = "https://lifelinepyr.jasperredis.net"


def act(rsurface, keys, tick, mx, my):
    global friction, sel, lkpt, stats, done_text, done_animation, show_cat

    # Initialise
    if tick <= 1:
        friction = 1
        lkpt = 0
        show_cat = etc.chance(20)
    if not done_text:
        print(INTRO_TEXT)
        done_text = True

    # Render BG
    rsurface.blit(mgv.bgs[str(save_data['bg'])], (0, 0))
    # Render title
    tick_stages = [30, 80]
    friction_increment = 0.013

    if tick <= tick_stages[0] and not done_animation:
        rsurface.blit(ast.assets_data['title/title'],
                      etc.centrexy(ast.assets_data['title/title']))
    elif tick <= tick_stages[1] and not done_animation:
        x = etc.centrexy(ast.assets_data['title/title'], onecoord='x')
        y = etc.centrexy(
            ast.assets_data['title/title'], onecoord='y') - ((tick - 30) / friction)
        rsurface.blit(ast.assets_data['title/title'], (x, y))
        friction += friction_increment
    else:
        if not done_animation:
            done_animation = True
        if stats:
            box_asset = ast.assets_data['title/stats']
            rsurface.blit(box_asset, etc.centrexy(box_asset))
            text_x = etc.centrexy(box_asset, onecoord='x') + 3
            text_y = etc.centrexy(box_asset, onecoord='y') + 11
            text = [
                f"Highscore   : {save_data['high']}",
                f"Totalscore  : {save_data['total']}",
                f"Games Played: {save_data['played']}",
                "Press [X] to close."
            ]
            for line in text:
                text_surf = ast.assets_data['font1'].render(
                    line, False, mgv.colours[19])
                rsurface.blit(text_surf, (text_x, text_y))
                text_y += 6
            if keys[pg.K_x]:
                stats = False
        else:
            rsurface.blit(ast.assets_data['title/title'], (
                etc.centrexy(ast.assets_data['title/title'], onecoord='x'), 17))
            etc.MKTX(rsurface, sel, 1, "START", "title")
            etc.MKTX(rsurface, sel, 2, "OPTIONS", "title")
            etc.MKTX(rsurface, sel, 3, "STATS", "title")
            etc.MKTX(rsurface, sel, 4, "LICENSE", "title")
            etc.MKTX(rsurface, sel, 5, "HOW TO PLAY", "title")
            etc.MKTX(rsurface, sel, 6, "WEBSITE", "title")
            etc.MKTX(rsurface, sel, 7, "QUIT", "title")

            # Take input
            if keys[pg.K_DOWN] and etc.srp(tick, lkpt):
                sel += 1
                lkpt = tick
                ast.assets_data['mainaud/blip'].play()
            elif keys[pg.K_UP] and etc.srp(tick, lkpt):
                sel -= 1
                lkpt = tick
                ast.assets_data['mainaud/blip'].play()
            sel = max(1, min(sel, 7))
            if keys[pg.K_RETURN] and etc.srp(tick, lkpt):
                ast.assets_data['mainaud/blip'].play()
                if sel == 1:
                    return "game"
                elif sel == 2:
                    return "options"
                elif sel == 3:
                    stats = True
                elif sel == 4:
                    return "license"
                elif sel == 5:
                    webbrowser.open(HOW_TO_PLAY_URL)
                elif sel == 6:
                    webbrowser.open(WEBSITE_URL)
                elif sel == 7:
                    etc.close()

    # Title cat !!!!!!!! :3c
    if show_cat:
        cat_rect = ast.assets_data["title/cat"].get_rect()
        cat_rect.y = rsurface.get_height() - (ast.assets_data["title/cat"].get_height() + 1)
        cat_rect.x = 1
        cat_image = ast.assets_data["title/cat_pet"] if cat_rect.collidepoint(mx, my) else ast.assets_data["title/cat"]
        rsurface.blit(cat_image, cat_rect)

    # RESET LKPT if needed
    if keys[pg.K_l]:
        lkpt = 0
        B.bottom_text = "Reset LKPT."

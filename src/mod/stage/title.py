# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

from cerbose import cprint
import pygame as pg
import sys
import mod.core.assets as ast
from mod.core.save import S
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
import mod.etc.BTXT as B

friction, sel, lkpt, stats, done_text, done_animation, show_cat = 1, 1, 0, False, False, False, False

def ACT(rsurface, keys, tick, mx, my):
    global friction, sel, lkpt, stats, done_text, done_animation, show_cat
    
    # Initialise
    if tick <= 1:
        friction = 1
        lkpt = 0
        show_cat = etc.chance(20)
        
    if not done_text:
        print(
            "Welcome to Lifeline.PYR!\n" +
            "Made by jasperredis, in open-source.\n" +
            "See info at: \n" +
            "- Github     : https://github.com/jasperredis/Lifeline.PYR \n" +
            "- Website    : https://jasperredis.github.io/Lifeline.PYR \n" +
            "- Itch.io    : https://jasperredis.itch.io/lifelinepyr \n" +
            "- jasperredis: https://jris.straw.page/a \n" +
            "This game is licensed under the GNU General Public License v3.0 or later. \n" +
            "For more information, do any of the following:\n" +
            "- Visit the packaged LICENSE file\n" +
            "- See the 'License' section on the 'ABOUT' screen\n" +
            "- Go to the GNU website at: https://gnu.org/licenses/gpl-3.0.en.html\n" +
            "---- \n" +
            "Lifeline.PYR  Copyright (C) 2025  jasperredis \n" +
            "This program comes with ABSOLUTELY NO WARRANTY; for details, see the GPLv3. \n" +
            "This is free software, and you are welcome to redistribute it \n" +
            "under certain conditions; see the GPLv3 for details."
        )
        done_text = True

    # Render BG
    rsurface.blit(mgv.BGS[str(S['bg'])], (0, 0))

    # Render title
    tick_stages = [30, 80]
    friction_increment = 0.013

    
    if tick <= tick_stages[0] and not done_animation:
        rsurface.blit(ast.ASSETS['title/title'], etc.centrexy(ast.ASSETS['title/title']))
    elif tick <= tick_stages[1] and not done_animation:
        x = etc.centrexy(ast.ASSETS['title/title'], onecoord='x')
        y = etc.centrexy(ast.ASSETS['title/title'], onecoord='y') - ((tick - 30) / friction)
        rsurface.blit(ast.ASSETS['title/title'], (x, y))
        friction += friction_increment
    else:
        if not done_animation:
            done_animation = True
        if stats:
            box_asset = ast.ASSETS['title/stats']
            rsurface.blit(box_asset, etc.centrexy(box_asset))
            text_x = etc.centrexy(box_asset, onecoord='x') + 3
            text_y = etc.centrexy(box_asset, onecoord='y') + 11
            text = [
                f"Highscore   : {S['high']}",
                f"Totalscore  : {S['total']}",
                f"Games Played: {S['played']}",
                "Press [X] to close."
            ]
            for line in text:
                text_surf = ast.ASSETS['font1'].render(line, False, mgv.COLOURS[18])
                rsurface.blit(text_surf, (text_x, text_y))
                text_y += 6
            if keys[pg.K_x]:
                stats = False
        else:
            rsurface.blit(ast.ASSETS['title/title'], (etc.centrexy(ast.ASSETS['title/title'], onecoord='x'), 17))
            etc.MKTX(rsurface, sel, 1, "START", "title")
            etc.MKTX(rsurface, sel, 2, "OPTIONS", "title")
            etc.MKTX(rsurface, sel, 3, "UPDATES", "title")
            etc.MKTX(rsurface, sel, 4, "HOW TO PLAY", "title")
            etc.MKTX(rsurface, sel, 5, "TIPS", "title")
            etc.MKTX(rsurface, sel, 6, "STATS", "title")
            etc.MKTX(rsurface, sel, 7, "ABOUT", "title")
            etc.MKTX(rsurface, sel, 8, "QUIT", "title")

            # Take input
            if keys[pg.K_DOWN] and etc.srp(tick, lkpt):
                sel += 1
                lkpt = tick
                ast.ASSETS['mainaud/blip'].play()
            elif keys[pg.K_UP] and etc.srp(tick, lkpt):
                sel -= 1
                lkpt = tick
                ast.ASSETS['mainaud/blip'].play()
            sel = max(1, min(sel, 8))
            if keys[pg.K_RETURN] and etc.srp(tick, lkpt):
                ast.ASSETS['mainaud/blip'].play()
                if sel == 1:
                    return "game"
                elif sel == 2:
                    return "options"
                elif sel == 3:
                    return "updates"
                elif sel == 4:
                    return "howtoplay"
                elif sel == 5:
                    return "tips"
                elif sel == 6:
                    stats = True
                elif sel == 7:
                    return "about"
                elif sel == 8:
                    etc.CLOSE()

    # Cat
    if show_cat:
        cat_rect = ast.ASSETS["title/cat"].get_rect()
        cat_rect.y = rsurface.get_height() - (ast.ASSETS["title/cat"].get_height() + 1)
        cat_rect.x = 1
        cat_image = ast.ASSETS["title/cat_pet"] if cat_rect.collidepoint(mx, my) else ast.ASSETS["title/cat"]
        rsurface.blit(cat_image, cat_rect)

    # RESET LKPT if needed
    if keys[pg.K_l]:
        lkpt = 0
        B.BTX = "Reset LKPT."

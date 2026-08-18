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
Welcome to Lifeline.PYR! Game by jasperredis.
See info at:
- Github     : https://github.com/jasperredis/Lifeline.PYR
- Website    : https://lifelinepyr.jasperredis.net
- Itch.io    : https://jasperredis.itch.io/lifelinepyr
- jasperredis: https://www.jasperredis.net
--------------------------------------------------------------------------------
This is FREE SOFTWARE. "Free" refers not to cost, but to FREEDOM.
You are FREE to:
- Run it as you wish and for any purpose
- Study and modify it
- Freely redistribute it
- Freely distribute modifications of it
...under applicable licenses.
If you are not familiar with it, I highly recommend seeing the GNU Project's
Free Software definition at https://www.gnu.org/philosophy/free-sw.html.
--------------------------------------------------------------------------------
This game is licensed under multiple licenses. For more information, see the
packaged LICENSE file.
"""
HOW_TO_PLAY_URL = "https://lifelinepyr.jasperredis.net/how-to-play.html"
WEBSITE_URL = "https://lifelinepyr.jasperredis.net"
BUTTONS = ["START", "OPTIONS", "KEYBINDINGS", "STATS", "LICENSE",
           "HOW TO PLAY", "WEBSITE", "QUIT"]


def do_title_animation(rsurface, tick):
    global done_animation
    TICK_STAGES = [30, 80]
    FRICTION_INCREMENT = 0.013
    global friction
    if tick <= TICK_STAGES[0] and not done_animation:
        rsurface.blit(ast.assets_data['title/title'],
                      etc.centrexy(ast.assets_data['title/title']))
    elif tick <= TICK_STAGES[1] and not done_animation:
        x = etc.centrexy(ast.assets_data['title/title'], onecoord='x')
        y = etc.centrexy(
            ast.assets_data['title/title'], onecoord='y') - \
            ((tick - 30) / friction)
        rsurface.blit(ast.assets_data['title/title'], (x, y))
        friction += FRICTION_INCREMENT
    else:
        done_animation = True
        return True  # Do render like normal (no, this isn't AI
                     # I just need to clarify)
    return False


def show_stats_screen(rsurface, keys):
    global stats
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


def show_title_screen(rsurface, mx, my):
    global sel
    rsurface.blit(ast.assets_data['title/title'], (
        etc.centrexy(ast.assets_data['title/title'], onecoord='x'), 17))
    for i, button in enumerate(BUTTONS):
        rect = etc.mk_text_option(rsurface, sel, i + 1, button, mgv.colours[1],
                                  True, 52, return_rect=True)
        if save_data["mouse-nav"] and rect.collidepoint(mx, my):
            sel = i


def show_title_cat(rsurface, mx, my):
    cat_rect = ast.assets_data["title/cat"].get_rect()
    cat_rect.y = rsurface.get_height() - \
        (ast.assets_data["title/cat"].get_height() + 1)
    cat_rect.x = 1
    cat_image = ast.assets_data["title/cat_pet"] if \
        cat_rect.collidepoint(mx, my) else ast.assets_data["title/cat"]
    rsurface.blit(cat_image, cat_rect)


def take_input(keys, tick, mb):
    global sel, lkpt, stats
    if keys[pg.K_DOWN] and etc.srp(tick, lkpt):
        sel += 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    elif keys[pg.K_UP] and etc.srp(tick, lkpt):
        sel -= 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    sel = max(1, min(sel, len(BUTTONS)))
    if (keys[pg.K_RETURN] or mb[0]) and etc.srp(tick, lkpt):
        ast.assets_data['mainaud/blip'].play()
        if sel == 1:
            return "game"
        elif sel == 2:
            return "options"
        elif sel == 3:
            return "keybindings"
        elif sel == 4:
            stats = True
        elif sel == 5:
            return "license"
        elif sel == 6:
            webbrowser.open(HOW_TO_PLAY_URL)
        elif sel == 7:
            webbrowser.open(WEBSITE_URL)
        elif sel == 8:
            etc.close()
        return None


def act(rsurface, keys, tick, mx, my, mb):
    global friction, lkpt, done_text, show_cat

    # Initialise
    if tick <= 1:
        friction = 1
        lkpt = 0
        show_cat = etc.chance(20)
    if not done_text:
        print(INTRO_TEXT)
        done_text = True

    # Reset lkpt if needed
    if keys[pg.K_l]:
        lkpt = 0
        B.bottom_text = "Reset LKPT."

    rsurface.blit(mgv.bgs[str(save_data['bg'])], (0, 0))
    if show_cat:  # Title cat!!!!! :3c
        show_title_cat(rsurface, mx, my)

    if not done_animation:
        proceed_to_title = do_title_animation(rsurface, tick)
    if done_animation or proceed_to_title:
        if stats:
            show_stats_screen(rsurface, keys)
        else:  # Regular title screen
            show_title_screen(rsurface, mx, my)
            return take_input(keys, tick, mb)

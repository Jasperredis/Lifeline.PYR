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

# Lifeline.PYR v1.0.1

# Import libraries
import pygame as pg
import webbrowser

# Core modules
from mod.core.updates import VERSION
import mod.core.assets as ast
from mod.core.save import S

# Other modules
from mod.etc import about_texts
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
import mod.etc.BTXT as B

text_y_min = 46
text_y = text_y_min
lkpt = 0
sel = 1
tab = 0

def ACT(rsurface, tick, keys, mb, mx, my):
    global text_y, lkpt, sel, tab

    # Take input
    # Scrolling
    if keys[pg.K_DOWN]:
        text_y -= 3 if not keys[pg.K_LSHIFT] else 7
    elif keys[pg.K_UP] and text_y < text_y_min:
        text_y += 3 if not keys[pg.K_LSHIFT] else 7
    # Tab navigation
    if keys[pg.K_LEFT] and etc.srp(tick, lkpt):
        tab -= 1
        lkpt = tick
        text_y = text_y_min
    elif keys[pg.K_RIGHT] and etc.srp(tick, lkpt):
        tab += 1
        lkpt = tick
        text_y = text_y_min
    tab = max(0, min(tab, 2))
    # Other
    if keys[pg.K_x]:  # Close
        return "title"
    elif keys[pg.K_l]:  # Reset LKPT
        lkpt = 0
        B.BTX = "Reset LKPT."

    # Render title
    rsurface.fill(mgv.THEMES[5]['bg'])
    if tab != 2 and tab != 3:
        title_asset = ast.ASSETS["title/title"]
    else:
        title_asset = ast.ASSETS["about/licenses"]
    rsurface.blit(
        title_asset,
        (etc.centrexy(title_asset, onecoord="x"), text_y - 34),
    )
    # Make text
    TEXTS = [
        about_texts.GAME,
        about_texts.CREDITS,
        about_texts.LICENSE,
    ]
    op = etc.make_fullscreen_scroll_text(
        rsurface, TEXTS[tab], text_y, mgv.THEMES[5], specialty_render="links"
    )
    # Handle links
    if op:
        for line, y_pos in op:
            line_parsed = line.split("|")
            button_rect = ast.ASSETS["about/go0"].get_rect()
            button_rect.y = y_pos
            button_rect.x = 2 + (len(line_parsed[0]) * 6)

            if button_rect.collidepoint(mx, my - 8):
                button_asset = ast.ASSETS["about/go0"]
                if mb[0] and etc.srp(tick, lkpt):
                    webbrowser.open(line_parsed[1])
                    lkpt = tick
            else:
                button_asset = ast.ASSETS["about/go1"]

            rsurface.blit(button_asset, button_rect)
    # Render tabs
    tab_box = pg.Rect(0, 0, rsurface.get_width(), 9)
    tab_box_border = pg.Rect(0, 9, rsurface.get_width(), 1)
    pg.draw.rect(rsurface, mgv.COLOURS[2], tab_box)
    pg.draw.rect(rsurface, mgv.COLOURS[18], tab_box_border)
    tabs = ["Game", "Credits", "Licenses"]
    for i in range(len(tabs)):
        x_pos = 3
        for j in tabs[:i]:
            x_pos += ((len(j) * 6) + 3)
        col = 15 if i == tab else 18
        text_surf = ast.ASSETS['font1'].render(
            tabs[i], False, mgv.COLOURS[col]
        )
        rsurface.blit(text_surf, (x_pos, 2))

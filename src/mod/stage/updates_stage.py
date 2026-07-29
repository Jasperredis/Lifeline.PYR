# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import webbrowser
import mod.core.assets as ast
from mod.core import updates
from mod.core.save import save_data
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc

sel = 2
scroll = 0
PAGE_ON = updates.get_latest()
others_tab = False
others_current = 0
contentbox_sprite = 1
contentbox_last_change = 0


def act(rsurface, tick, keys, mx, my):
    global lkpt, sel, scroll, PAGE_ON, others_tab, others_current, contentbox_sprite, contentbox_last_change

    contentbox_change_delay = 90

    # Initialise
    if tick <= 1:
        lkpt = 0

    # Get contentbox sprite
    if contentbox_last_change + contentbox_change_delay <= tick:
        contentbox_sprite = 2 if contentbox_sprite == 1 else 1
        contentbox_last_change = tick

    # Render bg
    rsurface.blit(mgv.bgs[str(save_data["bg"])], (0, 0))
    # Render images
    rsurface.blit(
        ast.assets_data["title/title"],
        (etc.centrexy(ast.assets_data["title/title"], onecoord="x"), 1),
    )
    rsurface.blit(
        ast.assets_data[f"updates/contentbox{contentbox_sprite}"],
        (
            etc.centrexy(ast.assets_data["updates/contentbox1"], onecoord="x"),
            ast.assets_data["title/title"].get_height() + 3,
        ),
    )
    # Add buttons
    padding = 2
    global_offset = 11
    y_pos_base = 113
    # Button data
    buttons = [
        {
            "asset": ast.assets_data["updates/exit"],
            "x": global_offset,
        },
        {
            "asset": ast.assets_data["updates/others"],
            "x": global_offset + padding + ast.assets_data["updates/exit"].get_width()
        },
        {
            "asset": ast.assets_data["updates/install"],
            "x": global_offset + (padding * 2) + ast.assets_data["updates/exit"].get_width() + ast.assets_data["updates/install"].get_width()
        },
        {
            "asset": ast.assets_data["updates/refresh"],
            "x": global_offset + (padding * 3) + ast.assets_data["updates/exit"].get_width() + (ast.assets_data["updates/install"].get_width() * 2)
        }
    ]
    i = 0
    for button in buttons:
        i += 1
        y = y_pos_base if sel == i else y_pos_base + 2
        rsurface.blit(button['asset'], (button['x'], y))
    # Take input
    # Move buttons
    if keys[pg.K_RIGHT] and etc.srp(tick, lkpt):
        sel += 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    elif keys[pg.K_LEFT] and etc.srp(tick, lkpt):
        sel -= 1
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
    sel = max(1, min(sel, len(buttons)))
    # Select
    if keys[pg.K_RETURN] and etc.srp(tick, lkpt):
        lkpt = tick
        ast.assets_data['mainaud/blip'].play()
        if sel == 1:
            return "title"
        elif sel == 2:
            PAGE_ON = updates.get_spec(0)
            others_tab = True
            others_current = max(updates.UPDATA) - 1
        elif sel == 4:
            updates.get_all_data()
    # Render update content
    if updates.UPDATA == "failed":
        rsurface.blit(
            ast.assets_data['updates/nonetwork'],
            (
                etc.centrexy(ast.assets_data['updates/nonetwork'], onecoord='x'),
                ast.assets_data["title/title"].get_height() + 15, 
            )
        )
    else:
        #* Render text
        # Header
        header_text = f"{PAGE_ON['title']} | V{PAGE_ON['version']}"
        header_surf = ast.assets_data['font1'].render(header_text, False, mgv.colours[19])
        rsurface.blit(
            header_surf, 
            (
                etc.centrexy(header_surf, onecoord='x'), 
                ast.assets_data["title/title"].get_height() + 5
            ),
        )
        
        # Take network-requiring input
        if keys[pg.K_RETURN] and sel == 3:
            webbrowser.open(PAGE_ON['install'])

        #* Description
        desc_text = PAGE_ON['desc'].split('\n')

        # Wrap description
        max_character_length = 33
        wrapped_desc = []
        for line in desc_text:
            while len(line) > max_character_length:
                wrapped_desc.append(line[:max_character_length])
                line = line[max_character_length:]
            wrapped_desc.append(line)

        # Scrolling
        max_line_length = 9
        back_desc_text = wrapped_desc[scroll:]
        if len(back_desc_text) > 9:
            scrolled_desc_text = back_desc_text[:max_line_length]
        else:
            scrolled_desc_text = back_desc_text
        desc_x = etc.centrexy(ast.assets_data["updates/contentbox1"], onecoord="x") + 2
        desc_y = ast.assets_data["title/title"].get_height() + 13
        for line in scrolled_desc_text:
            text_surf = ast.assets_data['font1'].render(
                line, False, mgv.colours[19]
            )
            rsurface.blit(text_surf, (desc_x, desc_y))
            desc_y += 6
        
        # Scroll
        if keys[pg.K_UP] and etc.srp(tick, lkpt):
            scroll -= 1
            lkpt = tick
        elif keys[pg.K_DOWN] and etc.srp(tick, lkpt):
            scroll += 1
            lkpt = tick
        scroll = max(0, min(scroll, len(desc_text) - 8))

        # Handle Others tab
        if others_tab:
            if keys[pg.K_x]:
                others_tab = False
                PAGE_ON = updates.get_latest()
            elif keys[pg.K_SPACE]:
                PAGE_ON = updates.get_spec(others_current)
            elif keys[pg.K_q] and etc.srp(tick, lkpt):
                others_current -= 1
                others_current = max(1, min(others_current, max(updates.UPDATA) - 1))
                PAGE_ON = updates.get_spec(others_current)
                lkpt = tick
            elif keys[pg.K_e] and etc.srp(tick, lkpt):
                others_current += 1
                others_current = max(1, min(others_current, max(updates.UPDATA) - 1))
                PAGE_ON = updates.get_spec(others_current)
                lkpt = tick

        # Sample update data for reference
        # {'title': 'test123', 
        # 'version': 1.2, 
        # 'date': '7-30-2025', 
        # 'desc': "hello, this is cool,\nand that's a newline.\n", 
        # 'tags': [
        # {1: None, 'name': 'tagname', 'colour': 19, 'text-colour': 18}, 
        # {1: None, 'name': 'other-tagname', 'colour': 2, 'text-colour': 18}
        # ]}

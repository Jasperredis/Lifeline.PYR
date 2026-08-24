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

# Lifeline.PYR v1.1-dev

from cerbose import cprint
import pygame as pg
from mod.core.save import save_data
import mod.core.assets as ast
import mod.core.args as args
import mod.core.music as music
from mod.stage import game_sel, title, options, license_stage, intro
from mod.stage.game import stage as game
import mod.etc.screenshot as screenshot
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc
import mod.etc.BTXT as B
# ↓↓↓ Responsible for metrics, bottom text display, and window buttons
import mod.etc.wintop as wintop

# Init pygame
pg.init()
pg.font.init()
pg.mixer.init()


# Init window
def make_display():
    global screen, rsurface, winsize, base_winsize
    global game_area, game_base_winsize
    base_winsize = (256, 144)
    game_base_winsize = (256, 128)
    if not save_data["fullscreen"]:
        winsize = (base_winsize[0] * save_data["winscale"],
                   base_winsize[1] * save_data["winscale"])
        screen = pg.display.set_mode((winsize))
    else:
        winsize = base_winsize
        screen = pg.display.set_mode((base_winsize), pg.FULLSCREEN | pg.SCALED)
    rsurface = pg.Surface(base_winsize)
    game_area = pg.Surface(game_base_winsize)


make_display()
pg.display.set_caption("Lifeline.PYR v1.0.1-dev")
pg.mouse.set_visible(False)
pg.display.set_icon(ast.assets_data['global/windicon'])

clock = pg.time.Clock()
done_text_intro = False
stage = "title" if args.no_intro else "intro"
stage_history = [stage]

tick, nc_tick, mb, mx, my, key = 0, 0, 0, 0, 0, None
keys = pg.key.get_pressed()
# nc_tick = non-changing tick


STAGES = {
    "intro": {
        "function": lambda: intro.act(game_area, tick)
    },
    "title": {
        "function": lambda: title.act(game_area, keys, tick, mx, my, mb)
    },
    "game_sel": {
        "function": lambda: game_sel.act(game_area, keys, tick, mx, my, mb)
    },
    "game_1d": {
        "function": lambda: game.act("normal_game", game_area, keys, tick, mx,
                                     my, mb)
    },
    "game_2d": {
        "function": lambda: game.act("2d", game_area, keys, tick, mx, my, mb)
    },
    "options": {
        "function": lambda: options.act(game_area, keys, key, tick, mx, my,
                                        stage_history, "options"),
        "special": {
            "remake_display": make_display
        }
    },
    "keybindings": {
        "function": lambda: options.act(game_area, keys, key, tick, mx, my,
                                        stage_history, "keybindings")
    },
    "license": {
        "function": lambda: license_stage.act(game_area, screen, keys)
    }
}


running = True
while running:
    try:
        mx, my = pg.mouse.get_pos()
        if not save_data['fullscreen']:
            mx //= save_data['winscale']
            my //= save_data['winscale']
        keys = pg.key.get_pressed()
        fps = int(clock.get_fps())
        mb = pg.mouse.get_pressed()
        tick += 1
        nc_tick += 1
        key = None
        # Poll for events
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                key = event.key
            if event.type == pg.QUIT:
                running = False
                etc.close()
        # Wipe surfaces
        rsurface.fill(mgv.colours[1])
        game_area.fill(mgv.colours[1])
        # Stage handler
        new_stage = STAGES[stage]["function"]()
        if new_stage is not None:
            if "special" in STAGES[stage] \
               and new_stage in STAGES[stage]["special"]:
                STAGES[stage]["special"][new_stage]()
            else:
                if new_stage in STAGES:
                    cprint("info", f"Switching to stage: {new_stage}")
                    tick = 0
                    stage = new_stage
                    stage_history.append(stage)
                    music.switch_music(stage)
                    B.bottom_text = f"Set stage to {new_stage}."
        # Render all
        if wintop.act(rsurface, fps, tick, mx, my, mb):  # See line 41
            make_display()
        rsurface.blit(game_area, (0, 8))  # Content
        rsurface.blit(
            mgv.mice[str(save_data['mouse-theme'])], (mx, my))  # Mouse
        # Scale
        scaled_surface = pg.transform.scale(rsurface, winsize)
        screen.blit(scaled_surface, (0, 0))
        # Loop ending
        screenshot.act(keys, rsurface, nc_tick)
        pg.display.flip()
        clock.tick(30)   # Limit FPS to 30

    except KeyboardInterrupt:  # Except ^C
        print()
        cprint("warn", "Game interrupted by ^C.")
        etc.close()

pg.quit()

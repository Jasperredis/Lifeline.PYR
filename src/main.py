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

# Lifeline.PYR v1.0

# Import libraries
from cerbose import cprint, cerbar
import pygame as pg

# Core modules
from mod.core.save import S, wr
import mod.core.assets as ast
import mod.core.args as args
import mod.core.updates as updates
import mod.core.music as music

# Stage modules
import mod.stage.updates_stage as updates_stage
import mod.stage.howtoplay as howtoplay
import mod.stage.etc.wintop as wintop
import mod.stage.game.stage as game
import mod.stage.options as options
import mod.stage.title as title
import mod.stage.about as about
import mod.stage.intro as intro
import mod.stage.begin as begin
import mod.stage.tips as tips

# Other modules
import mod.etc.screenshot as screenshot
import mod.etc.magicvars as mgv 
import mod.etc.etcils as etc
import mod.etc.BTXT as B

# Init pygame
pg.init()
pg.font.init()
pg.mixer.init()

# Init window
def make_disp():
    global screen, rsurface, winsize, winscale, base_winsize, game_area, game_base_winsize
    base_winsize = (256, 144)
    game_base_winsize = (256, 128)
    if not S["fullscreen"]:
        winsize = (base_winsize[0] * S["winscale"], base_winsize[1] * S["winscale"])
        screen = pg.display.set_mode((winsize))
    else:
        winsize = base_winsize
        screen = pg.display.set_mode((base_winsize), pg.FULLSCREEN | pg.SCALED)
    rsurface = pg.Surface(base_winsize)
    game_area = pg.Surface(game_base_winsize)


make_disp()
pg.display.set_caption("Lifeline.PYR")
pg.mouse.set_visible(False)
clock = pg.time.Clock()

pg.display.set_icon(ast.ASSETS['global/windicon'])

# Important variables
if args.no_intro:
    stage = "title" if S["seen_begin"] else "begin"
else:
    stage = "intro"
stage_history = [stage]
done_text_intro = False

# "Dynamic variables"; core variables that rapidly change
tick, nc_tick, mb, mx, my, keys = 0, 0, 0, 0, 0, pg.key.get_pressed()
#? nc_tick = non-changing tick

# Form magic variables
mgv.BGS = mgv.form_BGS()
mgv.mice = mgv.form_mice()

STAGE_DATA = {
    "intro": {
        "function": lambda: intro.ACT(game_area, tick)
    },
    "title": {
        "function": lambda: title.ACT(game_area, keys, tick, mx, my)
    },
    "game": {
        "function": lambda: game.ACT(game_area, keys, tick, mx, my, mb)
    },
    "options": {
        "function": lambda: options.ACT(game_area, keys, tick, stage_history),
        "special": {
            "remake_display": make_disp
        }
    },
    "about": {
        "function": lambda: about.ACT(game_area, tick, keys, mb, mx, my)
    },
    "updates": {
        "function": lambda: updates_stage.ACT(game_area, tick, keys, mx, my)
    },
    "howtoplay": {
        "function": lambda: howtoplay.ACT(game_area, keys, tick)
    },
    "begin": {
        "function": lambda: begin.ACT(game_area, keys, tick)
    },
    "tips": {
        "function": lambda: tips.ACT(game_area, keys, tick)
    }
}

running = True

while running:
    try:
        # Update dynamic variables
        mx, my = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        fps = int(clock.get_fps())
        mb = pg.mouse.get_pressed()
        tick += 1
        nc_tick += 1

        # Poll for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                etc.CLOSE()

        # Wipe surfaces
        rsurface.fill(mgv.COLOURS[0])
        game_area.fill(mgv.COLOURS[0])

        #* Stage handler
        new_stage = STAGE_DATA[stage]["function"]()
        if new_stage is not None:
            if "special" in STAGE_DATA[stage] and new_stage in STAGE_DATA[stage]["special"]:
                STAGE_DATA[stage]["special"][new_stage]()
            else:
                if new_stage in STAGE_DATA:
                    cprint("info", f"Switching to stage: {new_stage}")
                    tick = 0
                    stage = new_stage
                    stage_history.append(stage)
                    music.switch_music(stage)
                    B.BTX = f"Set stage to {new_stage}."

        # Add metrics
        #TODO: This needs to go into a seperate module.
        text = ast.ASSETS["font1"].render(f"FPS: {fps} - Tick: {tick} - Mouse: {mx}, {my}", False, mgv.COLOURS[18])
        rsurface.blit(text, (2, 2))

        # Add front-layered objects
        if wintop.ACT(rsurface, tick, mx, my, mb):  # Window buttons
            make_disp()
        # B.BTX
        text = ast.ASSETS["font1"].render(B.BTX, False, mgv.COLOURS[18])
        rsurface.blit(text, (1, 138)) 

        # Render all
        rsurface.blit(game_area, (0, 8)) # Add content
        rsurface.blit(mgv.mice[str(S['mouse-theme'])], (mx, my))  # Mouse

        # Scale
        scaled_surface = pg.transform.scale(rsurface, winsize)
        screen.blit(scaled_surface, (0, 0))

        # Loop ending
        screenshot.ACT(keys, rsurface, nc_tick)
        pg.display.flip()
        clock.tick(30)   # Limit FPS to 30

    except KeyboardInterrupt: # Except ^C
        print()
        cprint("warn", "Game interrupted by ^C.")
        etc.CLOSE()

pg.quit()

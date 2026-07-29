# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc

TIPS = [
    " Dash doesn't work if its charge is <10.",
    " Dashing in two axis at once in 2D| \
mode doubles your dash usage, making the| \
dash effectively useless. Only use dash| \
in one axis!",
    " This tip looks weird.",
    " Clear all enemies is incredibly useful if| \
you can stack up on heals with a little| \
amount of enemies.",
    " You can't collect heals while jumping.",
    "This tip is 6px further to the left than|\
all of the other tips.",
    " If there is a little number of heals,| \
you could consider intentionally| \
lowering your health to trigger urgency,| \
causing more health powerups.| \
Be careful; this could be risky!",
    " The red shield that appears on the top| \
of your screen indicates that you are| \
in i-frames; you have a mere 10 ticks| \
of invincibility from enemies!",
    " You may be able to not be hurt| \
by an enemy if you dash past it, though| \
this is a bug, and unpredictable, so| \
don't count on it!"
]
tip = 0
lkpt = 0


def act(rsurface, keys, tick):
    global tip, lkpt

    if lkpt > tick:
        lkpt = 0

    # Render static display
    rsurface.blit(
        ast.assets_data["tips/header"], (
            etc.centrexy(ast.assets_data["tips/header"], onecoord='x'), 1
        )
    )

    # Render tip
    tip_y = 15
    tip_added = \
f"Press [RETURN] for a new tip.|\
Press [X] to return to the title.||\
Tip `{tip + 1}/{len(TIPS)}:|" + TIPS[tip]
    tip_proc = tip_added.split('|')
    for line in tip_proc:
        anti_alias = True if tip == 2 else False
        colour = (0, 255, 0) if tip == 2 else mgv.colours[19]
        text_surface = ast.assets_data["font1"].render(
            line, anti_alias, colour
        )
        rsurface.blit(text_surface, (2, tip_y))
        tip_y += 6

    # Change tip
    if keys[pg.K_RETURN] and etc.srp(tick, lkpt):
        tip += 1
        tip = 0 if tip >= len(TIPS) else tip
        lkpt = tick

    # Leave
    if keys[pg.K_x]:
        return "title"

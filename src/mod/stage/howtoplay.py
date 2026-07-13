# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import S
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc

TEXTS = {
    0: [
        "Use the arrow keys to scroll.",
        "You can use shift to scroll faster.",
        "I make this note because every single",
        "person who playtested wouldn't figure this",
        "out on their own!!!!", "",
        "|howtoplay/1d", "",
        "|howtoplay/player",
        "In the red circle (or the circle marked by",
        "the letter R) is you, the player. In",
        "gameplay, you can use the [A] key to move",
        "left, and [D] to move right.",
        "You can also hold [S] to slow down for",
        "precision.", "",
        "|howtoplay/life",
        "This is your life. Each green orb",
        "represents a health point. In gameplay you",
        "may, and should, notice that you are",
        "constantly losing these orbs. On the far",
        "right of the orbs, there is your life",
        "timer. It shows how long you have until",
        "you lose another health point (2 seconds).", "",
        "Note: You can pause using [ESCAPE].", ""
        "|howtoplay/enemy",
        "This is an enemy. It randomly spawns, and",
        "if you run into it, you will lose health.",
        "You get around a third of a second of",
        "immunity from them after running into one.", "",
        "Warning: The + and - indicators are not",
        "there by default. You must go into",
        "OPTIONS and enable Indicators.", "",
        "|howtoplay/heal",
        "This is a heal; it is the one thing",
        "keeping you from dying. Run into it, and",
        "you get healed by 1 health point.", "",
        "|howtoplay/info",
        "This is your current game info. You can",
        "probably assume what SCORE means, but HIGH",
        "is your highscore, TOTAL is every score",
        "you've ever gotten added up, and GAME is",
        "how many games you have played.", "",
        "|howtoplay/jump",
        "This is your jump charge. Once it reaches",
        "full capacity (4/4) (which it starts at),"
        "you can perform a 'jump'. This makes you",
        "invincible for 2 seconds, but you also",
        "cannot collect heals during this time.",
        "You can end the jump early by pressing",
        "[S]. The jump takes 10 seconds to",
        "recharge.", "",
        "|howtoplay/dash",
        "This is your dash bar. It ranges from 0 to",
        "106. When you use it (by holding E), you",
        "can go 3.5x your regular speed. It",
        "depletes in ~0.3 seconds of use, and it",
        "takes ~5 seconds to fully recharge. It",
        "will not do anything if the dash charge is",
        "under 10 (which is marked by the red",
        "line).", "",
        "|howtoplay/falling_object",
        "This is a falling object. They spawn",
        "randomly and have 5 different varieties;",
        "|howtoplay/all_falling_objects",
        "- ow_a: A 31px wide hazard. Kills you on",
        "impact.",
        "- ow_b: A 7px wide hazard. Behaves the",
        "same way as ow_a, just smaller.",
        "- max_life: A powerup that restores your",
        "life to maximum (5).",
        "- max_jump: A powerup that fully charges",
        "your jump charge (4/4).",
        "- clear_enemies: Gets rid of all currently",
        "present enemies. Does not stop more from",
        "spawning.",
        "More powerups will spawn when you need",
        "them!", "",
        "I would say 'this is a laser', but I",
        "am too lazy to get a screenshot of a",
        "laser, so my description will have to",
        "suffice.",
        "Lasers first appear as large",
        "exclamation points over the field/line.",
        "These exclamation points do not hurt",
        "you; they serve to warn you about",
        "where the laser will be.",
        "After a few seconds, the laser will",
        "strike, as a long, vertical line",
        "changing colours from blue to pink.",
        "Do not touch it, or you will die!",
        "Instantly! Wait it out.",
        "",
        "|howtoplay/1d",
        "Congratulations! You have read 9",
        "paragraphs. I assume you now know how to",
        "play this game. Consider reading the guide",
        "for 2D?", "",
        "Have fun! :3"
    ],
    1: [
        "|howtoplay/2d", "",
        "WARNING: Please read the guide for 1D",
        "before reading this! This guide builds on",
        "what you learn from that and assumes you",
        "have already read it; it is essential to",
        "understand and effectively use this",
        "information!!!!!!", "",
        "2D mode is really just like 1D mode,",
        "but...2D. Here's a good look at the UI",
        "layout:",
        "|howtoplay/2dlayout",
        "And here's what everything is (by the",
        "circle colour and letter next to it):",
        "- Green (G): Player",
        "- Red (R): Heal",
        "- Blue (B): Enemy",
        "- Pink (P): Falling object (ow_b)",
        "- Grey (G2): Dash bar",
        "- Orange (O): Game information",
        "- Yellow (Y): Jump charge",
        "- Light blue (B2): Life", "",
        "Along with that, some controls are",
        "different:",
        "Move up: W",
        "Move down: S",
        "Move left (not different, refresher): [A]",
        "Move right (not different, refresher): [D]",
        "Jump: Up arrow",
        "Slow: Down arrow",
        "Stop jump: Down arrow",
        "Dash (not different, just refresher): [E]", "",
        "|howtoplay/2d", "",
        "That's all! Not really much else to cover.",
        "Goodbye, and consider playing 2D mode to",
        "put your new knowledge to use.", "",
        "Have fun! :3c"
    ]
}

text_y, tab, lkpt = 2, 0, 0

def ACT(rsurface, keys, tick):
    global TEXT, text_y, tab, lkpt
    text_y_min = 2

    THEME = mgv.THEMES[S['htp-theme']]
    rsurface.fill(THEME['bg'])

    if lkpt > tick:
        lkpt = 0

    # Take input
    if keys[pg.K_DOWN]:
        text_y -= 3 if not keys[pg.K_LSHIFT] else 7
    elif keys[pg.K_UP] and text_y < 1:
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
    tab = max(0, min(tab, len(TEXTS) - 1))

    TEXT = TEXTS[tab]

    etc.make_fullscreen_scroll_text(rsurface, TEXT, text_y + 10, THEME, specialty_render="images")
    # Note: text_y gets 10 added to account for the tab bar being in the way.
    # Bottom text
    bottom_border_rect = pg.Rect(0, rsurface.get_height() - 7, rsurface.get_width(), 7)
    pg.draw.rect(rsurface, mgv.COLOURS[0], bottom_border_rect)
    text_surf = ast.ASSETS['font1'].render(
        "Press [X] to exit.", False, mgv.COLOURS[18]
    )
    rsurface.blit(text_surf, (1, rsurface.get_height() - 6))

    # Render tabs (yoinked from about.py, wink)
    tab_box = pg.Rect(0, 0, rsurface.get_width(), 9)
    tab_box_border = pg.Rect(0, 9, rsurface.get_width(), 1)
    pg.draw.rect(rsurface, mgv.COLOURS[2], tab_box)
    pg.draw.rect(rsurface, mgv.COLOURS[18], tab_box_border)
    tabs = ["1D", "2D"]
    for i in range(len(tabs)):
        x_pos = 3
        for j in tabs[:i]:
            x_pos += ((len(j) * 6) + 3)
        col = 15 if i == tab else 18
        text_surf = ast.ASSETS['font1'].render(
            tabs[i], False, mgv.COLOURS[col]
        )
        rsurface.blit(text_surf, (x_pos, 2))


    if keys[pg.K_x]:
        ast.ASSETS['mainaud/blip'].play()
        return "title"

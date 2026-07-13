# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

from cerbose import cprint
import random as rd
import sys
from mod.etc.magicvars import COLOURS
from mod.core.assets import ASSETS
from mod.core.save import S, wr

def centrexy(obj, *, onecoord=None): # Centre an object's coordinates
    x = 128 - (obj.get_width() / 2)
    y = 64 - (obj.get_height() / 2)
    if onecoord == None:
        return (x, y)
    elif onecoord == "x":
        return x
    else:
        return y

def srp(tick, lkpt): # Stop repeating (key) presses
    return tick - lkpt >= 3

def MKTX(rsurface, sel, order, txt, context): # Make a text selection in a screen
    if sel == order:
        text = ASSETS['font1'].render(txt, False, COLOURS[15], COLOURS[0])
    else:
        if context == "game" or context == "options":
            text = ASSETS['font1'].render(txt, False, COLOURS[18])
        else:
            text = ASSETS['font1'].render(txt, False, COLOURS[0])
    if context == "title":
        rsurface.blit(text, (centrexy(text, onecoord='x'), 52 + (order * 6)))
    elif context == "game":
        y = (rsurface.get_height() / 2) - 18
        y += order * 6
        rsurface.blit(text, (centrexy(text, onecoord='x'), y))
    elif context == "options":
        rsurface.blit(text, (5, 9 + (order * 6)))

def CLOSE(*, error=False):
    cprint("info", "Updating save for game closing.")
    wr(S)
    cprint("ok", "Goodbye! :3c")
    sys.exit()

def cprint_iv(type, text, *, logfile=None, timestamp=False): # cprint_IfVerbose
    global VERBOSE
    if VERBOSE:
        cprint(type, text, logfile=logfile, timestamp=timestamp)

def make_fullscreen_scroll_text(rsurface, TEXT, text_y, THEME, *, specialty_render):
    text_y_temp = text_y
    links = []

    for line in TEXT:
        if line.startswith('|') and specialty_render == "images" and line[1:] in ASSETS:
            rsurface.blit(ASSETS[line[1:]], (2, text_y_temp))
            text_y_temp += ASSETS[line[1:]].get_height() + 2

        elif specialty_render == "links" and "|" in line:
            links.append([line, text_y_temp])
            line = line.split('|')[0]

            text_surf = ASSETS['font1'].render(
                line, False, THEME['text']
            )
            rsurface.blit(text_surf, (2, text_y_temp))
            text_y_temp += 6

        else:
            text_surf = ASSETS['font1'].render(
                line, False, THEME['text']
            )
            rsurface.blit(text_surf, (2, text_y_temp))
            text_y_temp += 6

    if specialty_render == "links":
        return links

def chance(perc):
    return rd.random() * 100 < perc

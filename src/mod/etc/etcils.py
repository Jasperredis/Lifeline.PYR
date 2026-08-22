# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

from cerbose import cprint
import random as rd
import sys
import mod.etc.magicvars as mgv
from mod.core import assets
from mod.core.save import save_data, write_save


def centrexy(obj, *, onecoord=None):  # Centre an object's coordinates
    x = 128 - (obj.get_width() / 2)
    y = 64 - (obj.get_height() / 2)
    if onecoord is None:
        return (x, y)
    elif onecoord == "x":
        return x
    else:
        return y


def srp(tick, lkpt):  # Stop repeating (key) presses
    return tick - lkpt >= 3


# Make a text option in a screen
def mk_text_option(rsurface, sel, order, txt, unsel_colour, centre_x, start_y,
                   *, return_rect=False):
    if sel == order:
        text = assets.assets_data['font1'].render(
            txt, False, mgv.colours[16], mgv.colours[1])
    else:
        text = assets.assets_data['font1'].render(txt, False, unsel_colour)
    x = centrexy(text, onecoord='x') if centre_x else 5
    y = start_y + (order * 6)
    rsurface.blit(text, (x, y))
    if return_rect:
        return text.get_rect(topleft=(x, y))


def close(*, error=False):
    cprint("info", "Updating save for game closing.")
    write_save(save_data)
    cprint("ok", "Goodbye! :3c")
    sys.exit()


def chance(perc):
    return rd.random() * 100 < perc

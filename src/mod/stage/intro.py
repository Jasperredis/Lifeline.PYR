# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

from mod.core.assets import ASSETS
from mod.core.save import S
from mod.etc import etcils as etc

def ACT(rsurface, tick):
    if tick <= 90:
        rsurface.blit(ASSETS["intro/jris"], etc.centrexy(ASSETS["intro/jris"]))
    elif tick <= 180:
        rsurface.blit(ASSETS["intro/proud"], etc.centrexy(ASSETS["intro/proud"]))
    else:
        return "title" if S["seen_begin"] else "begin"

# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

import pygame as pg
import time
from mod.core.assets import ASSETS
import mod.etc.magicvars as mgv
import mod.etc.etcils as etc

lkpt = 0

def ACT(keys, rsurface, nc_tick):
    global lkpt

    if keys[pg.K_F2] and etc.srp(nc_tick, lkpt):
        lkpt = nc_tick
        ssf = f"screenshots/{int(time.time())}.png"
        pg.image.save(rsurface, ssf)
        ASSETS['mainaud/screenshot'].play()

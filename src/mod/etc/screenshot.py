# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

import pygame as pg
import time
from mod.core.assets import assets_data
import mod.etc.etcils as etc

lkpt = 0


def act(keys, rsurface, nc_tick):
    global lkpt

    if keys[pg.K_F2] and etc.srp(nc_tick, lkpt):
        lkpt = nc_tick
        ssf = f"screenshots/{int(time.time())}.png"
        pg.image.save(rsurface, ssf)
        assets_data['mainaud/screenshot'].play()

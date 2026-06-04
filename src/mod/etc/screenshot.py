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

# Lifeline.PYR v1.0.1

# Import libraries
import pygame as pg
import time

# Core module
from mod.core.assets import ASSETS

# Other modules
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

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

# Core module
from mod.core.assets import ASSETS

COLOURS = [
    (25, 33, 48),    # 0
    (72, 125, 21),   # 1
    (92, 103, 125),  # 2
    (159, 24, 37),   # 3
    (202, 119, 40),  # 4
    (192, 57, 69),   # 5
    (217, 87, 99),   # 6
    (91, 149, 35),   # 7
    (221, 149, 81),  # 8
    (236, 179, 125), # 9
    (161, 217, 107), # 10
    (226, 125, 134), # 11
    (231, 95, 188),  # 12
    (199, 236, 164), # 13
    (255, 162, 226), # 14
    (255, 183, 232), # 15
    (255, 227, 201), # 16
    (203, 219, 252), # 17
    (255, 255, 255), # 18
    (42, 130, 130)  # 19
]

THEMES = {
    1: {"text": COLOURS[0], "bg": COLOURS[18]},
    2: {"text": COLOURS[16], "bg": COLOURS[8]},
    3: {"text": COLOURS[16], "bg": COLOURS[19]},
    4: {"text": COLOURS[13], "bg": COLOURS[11]},
    5: {"text": COLOURS[18], "bg": COLOURS[0]},
    6: {"text": COLOURS[18], "bg": COLOURS[3]},
    7: {"text": COLOURS[0], "bg": COLOURS[4]}
}

BGS = {}
mice = {}

def form_BGS():
    return {
        "1": ASSETS['bg/main'],
        "2": ASSETS['bg/alt'],
        "3": ASSETS['bg/blood'],
        "4": ASSETS['bg/cyber'],
        "5": ASSETS['bg/green'],
        "6": ASSETS['bg/red'],
        "7": ASSETS['bg/rust'],
        "8": ASSETS['bg/sand'],
        "9": ASSETS['bg/thunder'],
        "10": ASSETS['bg/rain'],
        "11": ASSETS['bg/engine'],
        "12": ASSETS['bg/jrises'],
        "13": ASSETS['bg/wave'],
        "14": ASSETS['bg/sohappy'],
        "15": ASSETS['bg/deer'],
        "16": ASSETS['bg/nothing'],
        "17": ASSETS['bg/wire'],
    }

def form_mice():
    return {
        "1": ASSETS['mouse/def'],
        "2": ASSETS['mouse/inverted'],
        "3": ASSETS['mouse/visibility'],
        "4": ASSETS['mouse/arrow'],
        "5": ASSETS['mouse/arrow_visibility'],
        "6": ASSETS['mouse/block'],
        "7": ASSETS['mouse/block_visibility'],
        "8": ASSETS['mouse/l'],
        "9": ASSETS['mouse/l_visibility'],
        "10": ASSETS['mouse/small'],
        "11": ASSETS['mouse/rainbow'],
        "12": ASSETS['mouse/rainbow_alt'],
    }

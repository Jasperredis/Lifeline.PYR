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
from cerbose import cprint, cerbar
import pygame as pg
import os

# Initialise Pygame
pg.init()
pg.mixer.init()

ASSETS = {}

BASE_TYPES = [
    "images", "audio", "fonts"
]

for base_type in BASE_TYPES:
    cprint("proc", f"Loading base type '{base_type}'.")
    base_dir = os.path.join("assets", base_type)
    for folder in os.listdir(base_dir):
        cprint("proc", f"Loading assets of folder '{folder}'.")
        folder_dir = os.path.join(base_dir, folder)
        for i, asset in enumerate(os.listdir(folder_dir), 1):
            name = f"font{i}" if base_type == "fonts" else f"{folder}/{asset[:-4]}"
            asset_path = os.path.join(folder_dir, asset)
            if base_type == "images":
                ASSETS[name] = pg.image.load(asset_path)
            elif base_type == "audio":
                ASSETS[name] = pg.mixer.Sound(asset_path)
            elif base_type == "fonts":
                ASSETS[name] = pg.font.Font(asset_path, 6)
            cprint("ok", f"Loaded asset '{asset}'. Folder progress: \n \
            {cerbar(15, len(os.listdir(folder_dir)), i, perc='l', count='r')}")

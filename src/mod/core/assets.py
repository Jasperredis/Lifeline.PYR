# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.0.1

from cerbose import cprint, cerbar
import pygame as pg
import os

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

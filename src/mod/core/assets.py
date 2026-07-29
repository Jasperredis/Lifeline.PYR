# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

from cerbose import cprint
import pygame as pg
from mod.core.save import save_data
import mod.etc.magicvars as mgv
import os

pg.init()
pg.mixer.init()

assets_data = {}


def load_assets(*, only_images=False):
    BASE_TYPES = ["images"] if only_images else ["images", "audio", "fonts"]
    palette = save_data["palette"]
    for base_type in BASE_TYPES:
        cprint("proc", f"Loading base type '{base_type}'...")
        base_dir = os.path.join("assets", base_type)
        for folder in os.listdir(base_dir):
            cprint("proc", f"Loading assets_data of folder '{folder}'...")
            folder_dir = os.path.join(base_dir, folder)
            for i, asset in enumerate(os.listdir(folder_dir), 1):
                cprint("proc", f"Loading asset '{asset}'...")
                name = f"font{i}" if base_type == "fonts" else \
                    f"{folder}/{asset[:-4]}"
                asset_path = os.path.join(folder_dir, asset)
                if base_type == "images":
                    image = pg.image.load(asset_path)
                    image.set_palette(mgv.COLOURS[palette])
                    assets_data[name] = image
                elif base_type == "audio":
                    assets_data[name] = pg.mixer.Sound(asset_path)
                elif base_type == "fonts":
                    assets_data[name] = pg.font.Font(asset_path, 6)
    mgv.colours = mgv.COLOURS[palette]
    mgv.bgs = mgv.form_backgrounds(assets_data)
    mgv.mice = mgv.form_mice(assets_data)
    mgv.themes = mgv.form_htp_themes(palette)
    cprint("ok", "Assets all ready!")


load_assets()

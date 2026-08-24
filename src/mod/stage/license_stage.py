# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev

import pygame as pg
import mod.core.assets as ast
from mod.core.save import keyb
import mod.etc.magicvars as mgv

# Make surface to render
TEXT = """Lifeline.PYR | Licensing

This is a very short piece of text. For
more information, please refer to the
LICENSE file that should be in the root of
the folder that this game came in.
Each license will be followed by what file
the license text is found in.

GAME CODE: GNU GPLv3    | LICENSE-GPL
ASSETS   : CC-BY-SA 4.0 | LICENSE-CC-BY-SA
FONT     : SIL OFL 1.1  | LICENSE-OFL

See the LICENSE file for links to these
licenses and more info.

Press (Menu Exit) to close this.
  Menu Exit defaults to [X].
"""
y = 1
text_surface = pg.Surface((256, 128))
text_surface.fill(mgv.colours[1])
for line in TEXT.splitlines():
    surf = ast.assets_data['font1'].render(line, False, mgv.colours[19])
    text_surface.blit(surf, (1, y))
    y += 6
gplv3_sprite = ast.assets_data["about/gplv3"]
text_surface.blit(gplv3_sprite,
                  (255 - gplv3_sprite.get_width(),
                   127 - gplv3_sprite.get_height()))


def act(rsurface, screen, keys):
    rsurface.blit(text_surface, (0, 0))
    if keyb(keys, "menu-exit"):
        return "title"

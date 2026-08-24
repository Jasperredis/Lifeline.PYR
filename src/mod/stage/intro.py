# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev
# This is FREE SOFTWARE. See the LICENSE-GPL file for more information.

from mod.core.assets import assets_data
from mod.etc import etcils as etc


def act(rsurface, tick):
    if tick <= 90:
        rsurface.blit(assets_data["intro/jris"],
                      etc.centrexy(assets_data["intro/jris"]))
    elif tick <= 180:
        rsurface.blit(assets_data["intro/proud"],
                      etc.centrexy(assets_data["intro/proud"]))
    else:
        return "title"

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

# Lifeline.PYR v1.0

# Core modules
from mod.core.assets import ASSETS
from mod.core.save import S

# Other module
from mod.etc import etcils as etc

def ACT(rsurface, tick):
    if tick <= 90:
        rsurface.blit(ASSETS["intro/jris"], etc.centrexy(ASSETS["intro/jris"]))
    elif tick <= 180:
        rsurface.blit(ASSETS["intro/proud"], etc.centrexy(ASSETS["intro/proud"]))
    else:
        return "title" if S["seen_begin"] else "begin"

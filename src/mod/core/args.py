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

# Import libraries
from cerbose import cprint
import sys

# Variables
verbose = False
no_intro = False
no_updates = False

# Get and translate args
if len(sys.argv) >= 2:
    args = list(sys.argv[1])

    if 'v' in args:
        verbose = True
    if 'i' in args:
        no_intro = True
    if 'u' in args:
        no_updates = True

else:
    cprint("info", "No args.")

def cprint_iv(type, text, *, logfile=None, timestamp=False): # cprint_IfVerbose
    global verbose
    if verbose:
        cprint(type, text, logfile=logfile, timestamp=timestamp)

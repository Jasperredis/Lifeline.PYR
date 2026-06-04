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
from cerbose import cprint, mprint, cerbar
from datetime import datetime
import yaml
import sys

# Core modules
from mod.core import args

# Other modules
import mod.etc.BTXT as B

args.cprint_iv("proc", "Loading save...")
try:
    with open('save.yaml', 'r') as f: # Read and parse save.yaml
        DATA = f.read()
    args.cprint_iv("ok", "Opened and read save!")
    S = yaml.safe_load(DATA) #* SAVE DATA!!!
    args.cprint_iv("ok", "Fully loaded save!")
except Exception as e:
    cprint("fatal", f"Could not read save because: {e}.", logfile="logs/errors.txt", timestamp=True)
    cprint("debug", "Press [RETURN] to exit.")
    input()
    sys.exit()

def wr(sv): # Write the save to save.yaml
    """
    Writes to the save file. Arguments:
    - sv (dict): Save data.
    """
    cprint("proc", "Writing save...")
    try:
        with open('save.yaml', 'w') as f:
            yaml.dump(sv, f)
        cprint("ok", "Wrote save!")
        time = datetime.now()
        B.BTX = f"Updated save at {time.hour}:{time.minute}:{time.second}."
    except Exception as e:
        cprint("error", f"Could not write save because: {e}", logfile="logs/errors.txt", timestamp=True)
        cprint("warn", f"The game can continue, but it cannot write your save. Below, your save that would have been written will be show:")
        mprint("debug", f"Save:\n{sv}", logfile="logs/errors.txt", timestamp=True)
        B.BTX = "Check logs/errors.txt NOW!"

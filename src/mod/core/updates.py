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
from cerbose import cprint, mprint
import requests
import yaml
import sys

# Core modules
from mod.core import args

VERSION = 1.0

# Get update data
def get_all_data():
    global UPDATA
    if not args.no_updates:
        args.cprint_iv("proc", "Fetching update data...")
        try:
            response = requests.get('https://raw.githubusercontent.com/Jasperredis/Lifeline.PYR/updates/updates.yaml')
            response.raise_for_status()
            UPDATA = yaml.safe_load(response.text)
            args.cprint_iv("ok", "Succesfully fetched update data!")
        except Exception as e:
            mprint("error", 
                f"Could not fetch updates. This is likely a network error on your part.\n \
                More detailed error info here: {e}", \
            logfile="logs/errors.txt", timestamp=True)
            UPDATA = "failed"
    else:
        cprint("warn", "Updates manually skipped.")

def get_latest(): # Function to get latest update
    global UPDATA
    if UPDATA != "failed":
        maxkey = max(map(int, UPDATA.keys()))
        return UPDATA[maxkey]
    else:
        return "failed"

def get_spec(update): # Function to get a specific update
    global UPDATA
    return UPDATA[update]

get_all_data()

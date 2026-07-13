# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev
from cerbose import cprint, mprint
import requests
import yaml
import sys
from mod.core import args

VERSION = "1.0.1"

# Get update data
def get_all_data():
    global UPDATA
    if not args.no_updates:
        args.cprint_iv("proc", "Fetching update data...")
        try:
            response = requests.get('https://lifelinepyr.jasperredis.net/updates.yaml')
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

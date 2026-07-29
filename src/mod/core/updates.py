# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev
from cerbose import cprint, mprint
import requests
import yaml
from mod.core import args

VERSION = "1.0.1"
UPDATES_URL = "https://lifelinepyr.jasperredis.net/updates.yaml"


# Get update data
def get_all_data():
    global UPDATA
    if not args.no_updates:
        try:
            response = requests.get(UPDATES_URL)
            response.raise_for_status()
            UPDATA = yaml.safe_load(response.text)
            cprint("ok", "Fetched update data!")
        except Exception as e:
            mprint("error",
                   f"Could not fetch updates.\n \
                   This is likely a network error on your part.\n \
                   More detailed error info here: {e}",
                   logfile="logs/errors.txt", timestamp=True)
            UPDATA = "failed"
    else:
        cprint("warn", "Updates manually skipped.")


def get_latest():  # Function to get latest update
    if UPDATA != "failed":
        maxkey = max(map(int, UPDATA.keys()))
        return UPDATA[maxkey]
    else:
        return "failed"


def get_spec(update):  # Function to get a specific update
    return UPDATA[update]


get_all_data()

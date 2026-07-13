# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

from cerbose import cprint, mprint, cerbar
from datetime import datetime
import yaml
import sys
from mod.core import args
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

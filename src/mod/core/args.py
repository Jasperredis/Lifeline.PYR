# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

from cerbose import cprint
import sys

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

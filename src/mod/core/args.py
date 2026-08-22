# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.1-dev

from cerbose import cprint
import sys

no_intro = False
no_updates = False
constants_override = False

# Get and translate args
if len(sys.argv) >= 2:
    args = list(sys.argv[1])
    if 'i' in args:
        no_intro = True
    if 'u' in args:
        no_updates = True
    if 'c' in args:
        constants_override = True
else:
    cprint("info", "No args.")

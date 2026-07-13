# SPDX-License-Identifier: GPL-3.0-or-later

# Lifeline.PYR v1.1-dev

OPTS = {
    "count": 10,
    1: {
        "desc": "Use one of 9]]background options of]]various colours.",
        "key": "bg",
        "name": "Background",
        "call": {
            1: "Main",
            2: "Alt",
            3: "Blood",
            4: "Cyber",
            5: "Green",
            6: "Red",
            7: "Rust",
            8: "Sand",
            9: "Thunder",
            10: "rain.",
            11: "Engine",
            12: "Jrises",
            13: "Wave",
            14: "Sohappy",
            15: "Deer",
            16: "Nothing",
            17: "Wire",
            18: "Expirimental"
        },
        "clamp": "1,17",
        "bool": False,
    },
    2: {
        "desc": "Change the appearance]]of the mouse.",
        "key": "mouse-theme",
        "name": "Mouse theme",
        "call": {
            1: "Default",
            2: "Inverted",
            3: "Visibility",
            4: "Arrow",
            5: "Arrow (vis.)",
            6: "Block",
            7: "Block (vis.)",
            8: "L",
            9: "L (vis.)",
            10: "Small",
            11: "Rainbow",
            12: "Rainbow alt"
        },
        "clamp": "1,12",
        "bool": False
    },
    3: {
        "desc": "Move the player with]]your mouse instead]]of keys.",
        "key": "mouse-move",
        "name": "Mouse movement",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True
    },
    4: {
        "desc": "Change the soundtrack]]selection.",
        "key": "ost",
        "name": "Soundtrack",
        "call": {
            1: "Lifeline.PYR (Game A)",
            2: "Lifeline.PYR (Game B)",
            3: "Lifeline.PYR (Bonus)",
            4: "Alternate",
            5: "Lifeline.py"
        },
        "clamp": "1,5",
        "bool": False
    },
    5: {
        "desc": "Scale the window to]]fit your screen.",
        "key": "winscale",
        "name": "Window size",
        "call": {
            1: "1x (256x144) / Base",
            2: "2x (512x288)",
            3: "3x (768x432)",
            4: "4x (1024x576) / Def",
            5: "5x (1280x720) / 720p",
            6: "6x (1536x864)",
            7: "7x (1792x1008) / ~1080p",
            8: "8x (2048x1152)",
            9: "9x (2304x1296)",
            10: "10x (2560x1440) / 1440p",
            11: "11x (2816x1584)",
            12: "12x (3072x1728) ~3k",
        },
        "clamp": "1,12",
        "bool": False,
    },
    6: {
        "desc": "Change the chance of]]enemy spawns.",
        "key": "dif",
        "name": "Difficulty",
        "call": {1: "Mostly heals", 2: "Balanced", 3: "Mostly enemies"},
        "clamp": "1,3",
        "bool": False,
    },
    7: {
        "desc": "Self-explanatory.",
        "key": "fullscreen",
        "name": "Fullscreen",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    8: {
        "desc": "Gives the player]]velocity physics.",
        "key": "inertia",
        "name": "Inertia",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    9: {
        "desc": "Shows icons where]]heals and enemies]]are.",
        "key": "indicators",
        "name": "Indicators",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    10: {
        "desc": "Shows the velocity of]]the player if inertia]]is enabled.",
        "key": "velocity-icon",
        "name": "Velocity icon",
        "call": {0: "Off", 1: "On"},
        "clamp": "0,1",
        "bool": True,
    },
    11: {
        "desc": "Changes the colours in]]the HOW TO PLAY menu.",
        "key": "htp-theme",
        "name": "HTP theme",
        "call": {
            1: "Black-on-White",
            2: "Sand",
            3: "Ocean",
            4: "Watermelon",
            5: "White-on-Black",
            6: "Demo",
            7: "Original"
        },        
        "clamp": "1,7",
        "bool": False,
    }
}

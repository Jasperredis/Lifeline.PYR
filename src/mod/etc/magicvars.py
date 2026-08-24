# SPDX-License-Identifier: GPL-3.0-or-later
# Lifeline.PYR v1.2-dev
# This is FREE SOFTWARE. See the LICENSE-GPL file for more information.

COLOURS = {
    1: [  # Canonical
        (0, 0, 0),        # idx 0
        (20, 25, 35),     # idx 1
        (15, 103, 61),    # idx 2
        (74, 86, 110),    # idx 3
        (117, 15, 15),    # idx 4
        (163, 79, 24),    # idx 5
        (177, 47, 58),    # idx 6
        (217, 87, 108),   # idx 7
        (30, 135, 52),    # idx 8
        (209, 137, 71),   # idx 9
        (236, 186, 125),  # idx 10
        (119, 217, 107),  # idx 11
        (234, 138, 161),  # idx 12
        (205, 70, 166),   # idx 13
        (211, 236, 164),  # idx 14
        (241, 120, 177),  # idx 15
        (255, 171, 204),  # idx 16
        (255, 239, 201),  # idx 17
        (199, 216, 251),  # idx 18
        (255, 255, 255),  # idx 19
        (43, 130, 130)    # idx 20
    ],
    2: [  # Classic
        (0, 0, 0),        # idx 0
        (25, 33, 48),     # idx 1
        (72, 125, 21),    # idx 2
        (92, 103, 125),   # idx 3
        (159, 24, 37),    # idx 4
        (202, 119, 40),   # idx 5
        (192, 57, 69),    # idx 6
        (217, 87, 99),    # idx 7
        (91, 149, 35),    # idx 8
        (221, 149, 81),   # idx 9
        (236, 179, 125),  # idx 10
        (161, 217, 107),  # idx 11
        (226, 125, 134),  # idx 12
        (231, 95, 188),   # idx 13
        (199, 236, 164),  # idx 14
        (255, 162, 226),  # idx 15
        (255, 183, 232),  # idx 16
        (255, 227, 201),  # idx 17
        (203, 219, 252),  # idx 18
        (255, 255, 255),  # idx 19
        (42, 130, 130)    # idx 20
    ],
    3: [  # Inverted
        (255, 255, 255),  # idx 0
        (235, 230, 220),  # idx 1
        (240, 152, 194),  # idx 2
        (181, 169, 145),  # idx 3
        (138, 240, 240),  # idx 4
        (92, 176, 231),   # idx 5
        (78, 208, 197),   # idx 6
        (38, 168, 147),   # idx 7
        (225, 120, 203),  # idx 8
        (46, 118, 184),   # idx 9
        (19, 69, 130),    # idx 10
        (136, 38, 148),   # idx 11
        (21, 117, 94),    # idx 12
        (50, 185, 89),    # idx 13
        (44, 19, 91),     # idx 14
        (14, 135, 78),    # idx 15
        (0, 84, 51),      # idx 16
        (0, 16, 54),      # idx 17
        (56, 39, 4),      # idx 18
        (0, 0, 0),        # idx 19
        (212, 125, 125),  # idx 20
    ],
    4: [  # Warm
        (0, 0, 0),        # idx 0
        (35, 20, 20),     # idx 1
        (59, 103, 15),    # idx 2
        (110, 74, 83),    # idx 3
        (117, 15, 15),    # idx 4
        (163, 79, 24),    # idx 5
        (177, 47, 58),    # idx 6
        (217, 87, 108),   # idx 7
        (110, 135, 30),   # idx 8
        (209, 137, 71),   # idx 9
        (236, 186, 125),  # idx 10
        (201, 217, 107),  # idx 11
        (234, 138, 161),  # idx 12
        (205, 70, 141),   # idx 13
        (236, 234, 164),  # idx 14
        (241, 120, 163),  # idx 15
        (255, 171, 193),  # idx 16
        (251, 232, 199),  # idx 17
        (255, 239, 201),  # idx 18
        (255, 255, 255),  # idx 19
        (48, 67, 51)      # idx 20
    ],
    5: [  # Intense
        (0, 0, 0),        # idx 0
        (0, 0, 0),        # idx 1
        (0, 113, 29),     # idx 2
        (21, 56, 128),    # idx 3
        (134, 0, 0),      # idx 4
        (216, 47, 0),     # idx 5
        (255, 0, 0),      # idx 6
        (255, 10, 59),    # idx 7
        (0, 183, 0),      # idx 8
        (255, 138, 0),    # idx 9
        (255, 218, 95),   # idx 10
        (70, 255, 40),    # idx 11
        (255, 112, 161),  # idx 12
        (255, 0, 216),    # idx 13
        (255, 255, 153),  # idx 14
        (255, 95, 200),   # idx 15
        (255, 192, 241),  # idx 16
        (255, 255, 237),  # idx 17
        (228, 255, 255),  # idx 18
        (255, 255, 255),  # idx 19
        (0, 195, 195)     # idx 20
    ]
}

themes = {}
bgs = {}
mice = {}
colours = {}
bg_isdark = {
    1: False,   # Main
    2: False,   # Alt
    3: False,   # Alt 2
    4: False,   # Cotton Candy
    5: False,   # Blood
    6: False,   # Cyber
    7: False,   # Green
    8: False,   # Red
    9: False,   # Rust
    10: False,  # Sand
    11: False,  # Thunder
    12: True,   # Rain
    13: False,  # Engine
    14: True,   # Jrises
    15: True,   # Wave
    16: True,   # Sohappy
    17: True,   # Deer
    18: False,  # Nothing
    19: True,   # Wire
    20: False,  # Palette Test
    21: False   # Gradient
}


def form_backgrounds(assets_data):
    return {
        "1": assets_data['bg/main'],
        "2": assets_data['bg/alt'],
        "3": assets_data['bg/alt2'],
        "4": assets_data['bg/cottoncandy'],
        "5": assets_data['bg/blood'],
        "6": assets_data['bg/cyber'],
        "7": assets_data['bg/green'],
        "8": assets_data['bg/red'],
        "9": assets_data['bg/rust'],
        "10": assets_data['bg/sand'],
        "11": assets_data['bg/thunder'],
        "12": assets_data['bg/rain'],
        "13": assets_data['bg/engine'],
        "14": assets_data['bg/jrises'],
        "15": assets_data['bg/wave'],
        "16": assets_data['bg/sohappy'],
        "17": assets_data['bg/deer'],
        "18": assets_data['bg/nothing'],
        "19": assets_data['bg/wire'],
        "20": assets_data['bg/palette_test'],
        "21": assets_data['bg/gradient']
    }


def form_mice(assets_data):
    return {
        "1": assets_data['mouse/def'],
        "2": assets_data['mouse/inverted'],
        "3": assets_data['mouse/visibility'],
        "4": assets_data['mouse/arrow'],
        "5": assets_data['mouse/arrow_visibility'],
        "6": assets_data['mouse/block'],
        "7": assets_data['mouse/block_visibility'],
        "8": assets_data['mouse/l'],
        "9": assets_data['mouse/l_visibility'],
        "10": assets_data['mouse/small'],
        "11": assets_data['mouse/rainbow'],
        "12": assets_data['mouse/rainbow_alt'],
    }


def form_htp_themes(palette):
    return {
        1: {"text": colours[1], "bg": colours[19]},
        2: {"text": colours[17], "bg": colours[9]},
        3: {"text": colours[17], "bg": colours[20]},
        4: {"text": colours[14], "bg": colours[12]},
        5: {"text": colours[19], "bg": colours[1]},
        6: {"text": colours[19], "bg": colours[4]},
        7: {"text": colours[1], "bg": colours[5]}
    }

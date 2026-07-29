from pprint import pprint
from mod.etc.magicvars import COLOURS

def invert_palette(palette):
    return [(255 - r, 255 - g, 255 - b) for r, g, b in palette]

def print_palette(palette):
    print("[")
    for i, (r, g, b) in enumerate(palette):
        print(f"    ({r}, {g}, {b}),  # idx {i}")
    print("]")

if __name__ == "__main__":
    source_key = 1        # which palette to invert
    inverted = invert_palette(COLOURS[source_key])
    print_palette(inverted)

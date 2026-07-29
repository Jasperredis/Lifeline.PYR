from pathlib import Path
from PIL import Image

root = Path("assets")
non_indexed = []

for f in sorted(root.rglob("*.png")):
    try:
        img = Image.open(f)
        if img.mode != "P":
            non_indexed.append((f, img.mode))
    except Exception as e:
        print(f"ERROR reading {f}: {e}")

if non_indexed:
    print("Non-indexed PNGs found:")
    for f, mode in non_indexed:
        print(f"  {mode:6s}  {f}")
else:
    print("All PNGs are indexed (mode P).")

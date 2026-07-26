"""
Stage 3a: Clean a source photo for ASCII conversion.
  - Crops to a head-and-shoulders region (tweak CROP below to reframe)
  - Removes the background with rembg
  - Boosts local contrast with CLAHE so the face has real light/dark range
  - Composites onto a WHITE canvas so empty space maps to blank characters
Writes: assets/photo-ready.png
Usage:  python tools/clean_photo.py assets/me.jpg.jpeg
"""
import sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image
from rembg import remove

# Crop as fractions of (width, height). 0 = top/left edge, 1 = bottom/right.
# Shrink the box to zoom into the face; grow it to include more shoulder.
CROP = dict(left=0.20, right=0.82, top=0.13, bottom=0.60)

def main():
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "assets/me.jpg.jpeg")
    img = Image.open(src).convert("RGB")
    w, h = img.size

    # 1) Crop to head & shoulders
    box = (int(CROP["left"] * w), int(CROP["top"] * h),
           int(CROP["right"] * w), int(CROP["bottom"] * h))
    img = img.crop(box)
    print(f"cropped to {img.size}")

    # 2) CLAHE local-contrast boost on the L (lightness) channel
    lab = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(l)
    img = Image.fromarray(cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2RGB))

    # 3) Remove background -> RGBA (subject + transparency)
    cut = remove(img)
    print("background removed")

    # 4) Composite onto a white canvas (alpha as the mask)
    white = Image.new("RGB", cut.size, (255, 255, 255))
    white.paste(cut, mask=cut.split()[-1])

    out = Path("assets/photo-ready.png")
    white.save(out)
    print(f"wrote {out}  ({white.size[0]}x{white.size[1]})")

if __name__ == "__main__":
    main()
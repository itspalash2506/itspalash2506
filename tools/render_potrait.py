"""
Stage 3b: Convert assets/photo-ready.png into a self-drawing ASCII portrait SVG.
White characters on a dark panel; rows reveal top-to-bottom, then freeze.
Writes: portrait.svg
"""
from pathlib import Path
import numpy as np
from PIL import Image

# ---- Look & feel (all the knobs live here) -----------------------
COLS        = 110                   # detail. 90=chunky, 120=finer, keeps ASCII feel
GLYPHS      = " .,:;~+*xoXO#@"      # short ramp = discrete "ASCII" look
ACCENT      = "#ffffff"             # character color (white)
BG          = "#0d1117"             # panel background (dark)
FONT_SIZE   = 11
CHAR_ASPECT = 0.52                  # controls height/width proportion
PLOW, PHIGH = 4, 96                 # contrast-stretch percentiles
GAMMA       = 0.9                   # higher = softer shadows (<1 brightens)
ROW_DELAY   = 0.03                  # seconds between each row starting
DRAW_DUR    = 0.5                   # seconds for one row to draw in
PAD         = 16
# ------------------------------------------------------------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def main():
    im = Image.open("assets/photo-ready.png").convert("L")
    w, h = im.size
    rows = max(1, round(COLS * (h / w) * CHAR_ASPECT))
    im = im.resize((COLS, rows), Image.LANCZOS)
    px = np.asarray(im).astype(float)

    subj = px < 245
    lo, hi = np.percentile(px[subj], [PLOW, PHIGH])
    s = np.clip((px - lo) / max(1, (hi - lo)), 0, 1) ** GAMMA
    n = len(GLYPHS) - 1

    lines = []
    for r in range(rows):
        lines.append("".join(
            " " if not subj[r, c] else GLYPHS[int(round(s[r, c] * n))]
            for c in range(COLS)))

    char_w = FONT_SIZE * 0.6
    art_w = COLS * char_w
    W = art_w + PAD * 2
    H = rows * FONT_SIZE + PAD * 2

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
           f'font-family="ui-monospace,Menlo,Consolas,monospace">']
    out.append(f'<rect width="{W:.0f}" height="{H:.0f}" rx="10" fill="{BG}"/>')

    out.append('<defs>')
    for r in range(rows):
        y = PAD + r * FONT_SIZE
        out.append(f'<clipPath id="r{r}"><rect x="{PAD}" y="{y:.1f}" width="0" '
                   f'height="{FONT_SIZE}"><animate attributeName="width" from="0" '
                   f'to="{art_w:.1f}" begin="{r*ROW_DELAY:.3f}s" dur="{DRAW_DUR}s" '
                   f'fill="freeze"/></rect></clipPath>')
    out.append('</defs>')

    for r in range(rows):
        y = PAD + r * FONT_SIZE + FONT_SIZE * 0.8
        out.append(f'<text x="{PAD}" y="{y:.1f}" fill="{ACCENT}" font-size="{FONT_SIZE}" '
                   f'textLength="{art_w:.1f}" lengthAdjust="spacing" xml:space="preserve" '
                   f'clip-path="url(#r{r})">{esc(lines[r])}</text>')
    out.append('</svg>')

    Path("portrait.svg").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote portrait.svg  grid {COLS}x{rows}  {W:.0f}x{H:.0f}px")

if __name__ == "__main__":
    main()
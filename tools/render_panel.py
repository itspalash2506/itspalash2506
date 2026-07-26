"""
Step 4: Terminal-style profile card that animates in.
Writes: sysinfo.svg
  python tools/render_panel.py                  -> animated SVG (view in browser)
  set PREVIEW=1 & python tools/render_panel.py  -> static frame (view in image viewer)
"""
import os
from pathlib import Path

# ---- Your info: edit freely ---------------------------------------
NAME  = "Palash Ghoshdastidar"
ROLE  = "Software Engineer"
TITLE = "itspalash2506 — zsh"
FOCUS = "Mission-critical, low-latency AI systems"
NOW   = "Carrier-grade, fault-tolerant AI with fallbacks"
STACK = [
    ("backend",  ["Python", "FastAPI", "Flask", "gRPC"]),
    ("frontend", ["React", "Next.js"]),
    ("infra",    ["Elasticsearch", "GCP", "AWS", "Linux"]),
]
STATUS = "Open to mission-critical / AI-Systems Roles"
# ---- Look & feel --------------------------------------------------
BG0="#0b0f17"; BG1="#0d1117"; BAR="#161b22"
ACCENT="#39d3c3"; VALUE="#e6edf3"; MUTED="#8b949e"
PILLBG="#11212a"; PILLBD="#25454d"
FONT="ui-monospace,Menlo,Consolas,monospace"
W=740; PADX=34; BAR_H=46
# ------------------------------------------------------------------
PREVIEW = os.environ.get("PREVIEW") == "1"
op = "1" if PREVIEW else "0"

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def tw(s, fs): return len(s) * fs * 0.6                       # monospace text width
def fade(b):
    return "" if PREVIEW else (f'<animate attributeName="opacity" from="0" to="1" '
                               f'begin="{b:.2f}s" dur="0.3s" fill="freeze"/>')

def main():
    o = []
    y = BAR_H + 46

    # name + role, with accent bar
    o.append(f'<g opacity="{op}">{fade(0.15)}')
    o.append(f'<rect x="{PADX}" y="{y-26}" width="5" height="46" rx="2.5" fill="{ACCENT}"/>')
    o.append(f'<text x="{PADX+20}" y="{y}" font-size="30" font-weight="bold" fill="{VALUE}">{esc(NAME)}</text>')
    o.append(f'<text x="{PADX+20}" y="{y+26}" font-size="16" fill="{ACCENT}">{esc(ROLE)}</text>')
    o.append('</g>')
    y += 58
    o.append(f'<line x1="{PADX}" y1="{y}" x2="{W-PADX}" y2="{y}" stroke="#20262e"/>')
    y += 40

    def label(txt, yy, b):
        return (f'<g opacity="{op}">{fade(b)}<text x="{PADX}" y="{yy}" font-size="12" '
                f'letter-spacing="2" fill="{MUTED}">{esc(txt.upper())}</text></g>')
    def value(txt, yy, b):
        return (f'<g opacity="{op}">{fade(b)}<text x="{PADX}" y="{yy}" font-size="17" '
                f'fill="{VALUE}">{esc(txt)}</text></g>')

    o.append(label("focus", y, 0.5)); y += 26
    o.append(value(FOCUS, y, 0.6)); y += 42

    o.append(label("stack", y, 0.75)); y += 24
    FS=14.5; PH=30; padx=13; gap=9; rgap=12; maxx=W-PADX; b=0.85
    for sub, items in STACK:
        x = PADX
        o.append(f'<g opacity="{op}">{fade(b)}<text x="{x}" y="{y+PH*0.68:.0f}" '
                 f'font-size="12.5" fill="{MUTED}">{esc(sub)}</text></g>')
        x += 92
        for it in items:
            w = tw(it, FS) + 2*padx
            if x + w > maxx:
                x = PADX + 92; y += PH + rgap
            o.append(f'<g opacity="{op}">{fade(b)}'
                     f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{PH}" rx="{PH/2}" '
                     f'fill="{PILLBG}" stroke="{PILLBD}"/>'
                     f'<text x="{x+w/2:.0f}" y="{y+PH*0.68:.0f}" font-size="{FS}" '
                     f'fill="{ACCENT}" text-anchor="middle">{esc(it)}</text></g>')
            x += w + gap; b += 0.05
        y += PH + rgap
    y += 12

    o.append(label("now", y, b)); y += 26
    o.append(value(NOW, y, b+0.1)); y += 44
    o.append(f'<line x1="{PADX}" y1="{y-14}" x2="{W-PADX}" y2="{y-14}" stroke="#20262e"/>')

    # pulsing status footer
    o.append(f'<g opacity="{op}">{fade(b+0.2)}')
    o.append(f'<circle cx="{PADX+6}" cy="{y+6}" r="5" fill="#27c93f">'
             f'<animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite"/></circle>')
    o.append(f'<text x="{PADX+20}" y="{y+11}" font-size="14" fill="{MUTED}">{esc(STATUS)}</text>')
    o.append('</g>')
    y += 34
    H = y + 8

    head = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    head.append(f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient></defs>')
    head.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#bg)" stroke="#222b35"/>')
    head.append(f'<path d="M1 15 Q1 1 15 1 H{W-15} Q{W-1} 1 {W-1} 15 V{BAR_H} H1 Z" fill="{BAR}"/>')
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        head.append(f'<circle cx="{26+i*22}" cy="{BAR_H/2}" r="6.5" fill="{c}"/>')
    head.append(f'<text x="{W/2}" y="{BAR_H/2+5}" fill="{MUTED}" font-size="13.5" text-anchor="middle">{esc(TITLE)}</text>')

    Path("sysinfo.svg").write_text("\n".join(head + o + ["</svg>"]), encoding="utf-8")
    print(f"wrote sysinfo.svg  {W}x{int(H)}px  ({'preview' if PREVIEW else 'animated'})")

if __name__ == "__main__":
    main()
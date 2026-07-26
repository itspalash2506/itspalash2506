"""Step 5b: assets/contributions.json -> graph.svg (animated, column-by-column)."""
import json, os, datetime as dt
from pathlib import Path

LEVELS = ["#161b22", "#0b3b39", "#12716c", "#22b3a8", "#39d3c3"]   # 0..4 (cyan ramp)
ACCENT="#39d3c3"; TEXT="#e6edf3"; MUTED="#8b949e"; BG="#0d1117"
FONT="ui-monospace,Menlo,Consolas,monospace"
CELL=13; GAP=3; PAD=22; TOP=54; BOTTOM=54; COL_DELAY=0.018
MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def main(preview=False):
    data = json.loads(Path("assets/contributions.json").read_text())
    days = data["days"]
    d0 = dt.date.fromisoformat(days[0]["date"])
    start = d0 - dt.timedelta(days=(d0.weekday() + 1) % 7)     # back up to a Sunday
    col = lambda s: (dt.date.fromisoformat(s) - start).days // 7
    row = lambda s: (dt.date.fromisoformat(s).weekday() + 1) % 7   # Sun=0 .. Sat=6

    ncols = max(col(x["date"]) for x in days) + 1
    W = ncols * (CELL + GAP) - GAP + PAD * 2
    H = TOP + 7 * (CELL + GAP) - GAP + BOTTOM

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    o.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="#222b35"/>')

    seen = set()
    for x in days:
        d = dt.date.fromisoformat(x["date"])
        if d.day <= 7 and d.month not in seen:
            seen.add(d.month)
            o.append(f'<text x="{PAD+col(x["date"])*(CELL+GAP)}" y="{TOP-10}" '
                     f'font-size="11" fill="{MUTED}">{MONTHS[d.month-1]}</text>')

    for c in range(ncols):
        op = '1' if preview else '0'
        anim = '' if preview else (f'<animate attributeName="opacity" from="0" to="1" '
                                   f'begin="{c*COL_DELAY:.3f}s" dur="0.35s" fill="freeze"/>')
        o.append(f'<g opacity="{op}">{anim}')
        for x in days:
            if col(x["date"]) != c:
                continue
            xx = PAD + c * (CELL + GAP)
            yy = TOP + row(x["date"]) * (CELL + GAP)
            o.append(f'<rect x="{xx}" y="{yy}" width="{CELL}" height="{CELL}" rx="3" '
                     f'fill="{LEVELS[x["level"]]}"/>')
        o.append('</g>')

    ly = H - 30
    o.append(f'<text x="{W-PAD-160}" y="{ly+CELL-2}" font-size="11" fill="{MUTED}">Less</text>')
    for i, c in enumerate(LEVELS):
        o.append(f'<rect x="{W-PAD-120+i*16}" y="{ly}" width="12" height="12" rx="3" fill="{c}"/>')
    o.append(f'<text x="{W-PAD-30}" y="{ly+CELL-2}" font-size="11" fill="{MUTED}">More</text>')

    s = (f'{data["total"]} contributions in the last year   •   '
         f'Current streak: {data["current_streak"]}d   •   Longest: {data["longest_streak"]}d   •   '
         f'Most active: {data["busiest_day"]}')
    o.append(f'<text x="{PAD}" y="{ly+CELL-2}" font-size="12.5" fill="{TEXT}">{esc(s)}</text>')
    o.append('</svg>')

    Path("graph.svg").write_text("\n".join(o), encoding="utf-8")
    print(f"wrote graph.svg  {W}x{H}px  {ncols} weeks")

if __name__ == "__main__":
    main(preview=os.environ.get("PREVIEW") == "1")
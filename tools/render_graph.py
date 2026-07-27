"""assets/contributions.json -> graph.svg + graph-light.svg (animated)."""
import json, os, datetime as dt
from pathlib import Path
DARK=dict(levels=["#161b22","#0b3b39","#12716c","#22b3a8","#39d3c3"],bg="#0d1117",
          text="#e6edf3",muted="#8b949e",border="#222b35")
LIGHT=dict(levels=["#ebedf0","#a5e8e1","#5ccabd","#2bb6ac","#12716c"],bg="#ffffff",
           text="#1f2328",muted="#57606a",border="#d0d7de")
THEMES=[("",DARK),("-light",LIGHT)]
FONT="ui-monospace,Menlo,Consolas,monospace"
CELL=13; GAP=3; PAD=22; TOP=54; BOTTOM=54; COL_DELAY=0.018
MONTHS=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def build(data,T,preview=False):
    LV=T["levels"]; days=data["days"]
    d0=dt.date.fromisoformat(days[0]["date"]); start=d0-dt.timedelta(days=(d0.weekday()+1)%7)
    col=lambda s:(dt.date.fromisoformat(s)-start).days//7
    row=lambda s:(dt.date.fromisoformat(s).weekday()+1)%7
    ncols=max(col(x["date"]) for x in days)+1
    W=ncols*(CELL+GAP)-GAP+PAD*2; H=TOP+7*(CELL+GAP)-GAP+BOTTOM
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    o.append(f'<rect width="{W}" height="{H}" rx="12" fill="{T["bg"]}" stroke="{T["border"]}"/>')
    seen=set()
    for x in days:
        d=dt.date.fromisoformat(x["date"])
        if d.day<=7 and d.month not in seen:
            seen.add(d.month); o.append(f'<text x="{PAD+col(x["date"])*(CELL+GAP)}" y="{TOP-10}" font-size="11" fill="{T["muted"]}">{MONTHS[d.month-1]}</text>')
    for c in range(ncols):
        op='1' if preview else '0'
        anim='' if preview else f'<animate attributeName="opacity" from="0" to="1" begin="{c*COL_DELAY:.3f}s" dur="0.35s" fill="freeze"/>'
        o.append(f'<g opacity="{op}">{anim}')
        for x in days:
            if col(x["date"])!=c: continue
            xx=PAD+c*(CELL+GAP); yy=TOP+row(x["date"])*(CELL+GAP)
            o.append(f'<rect x="{xx}" y="{yy}" width="{CELL}" height="{CELL}" rx="3" fill="{LV[x["level"]]}"/>')
        o.append('</g>')
    ly=H-30
    o.append(f'<text x="{W-PAD-160}" y="{ly+CELL-2}" font-size="11" fill="{T["muted"]}">Less</text>')
    for i,c in enumerate(LV): o.append(f'<rect x="{W-PAD-120+i*16}" y="{ly}" width="12" height="12" rx="3" fill="{c}"/>')
    o.append(f'<text x="{W-PAD-30}" y="{ly+CELL-2}" font-size="11" fill="{T["muted"]}">More</text>')
    s=(f'{data["total"]} contributions in the last year   •   Current streak: {data["current_streak"]}d   •   '
       f'Longest: {data["longest_streak"]}d   •   Most active: {data["busiest_day"]}')
    o.append(f'<text x="{PAD}" y="{ly+CELL-2}" font-size="12.5" fill="{T["text"]}">{esc(s)}</text>')
    o.append('</svg>'); return "\n".join(o)
def main():
    data=json.loads(Path("assets/contributions.json").read_text())
    preview=os.environ.get("PREVIEW")=="1"
    for suf,T in THEMES: Path(f"graph{suf}.svg").write_text(build(data,T,preview),encoding="utf-8")
    print("wrote graph.svg + graph-light.svg")
if __name__=="__main__": main()
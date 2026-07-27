import json, math
from pathlib import Path
from theme import THEMES
FONT="ui-monospace,Menlo,Consolas,monospace"
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def build(d,T):
    langs=d.get("languages",[])[:6]; SH=T["shades"]
    W,H=440,300; cxc,cyc,r,th=112,172,74,26
    css=["@keyframes app{from{opacity:0}to{opacity:1}}"]; segs=[]; ang=-90
    for i,(name,pct) in enumerate(langs):
        sweep=pct/100*360; a0=math.radians(ang); a1=math.radians(ang+sweep)
        x0,y0=cxc+r*math.cos(a0),cyc+r*math.sin(a0); x1,y1=cxc+r*math.cos(a1),cyc+r*math.sin(a1)
        large=1 if sweep>180 else 0; L=math.radians(sweep)*r
        css.append(f'@keyframes d{i}{{from{{stroke-dashoffset:{L:.1f}}}to{{stroke-dashoffset:0}}}}.d{i}{{animation:d{i} .7s ease {0.2+i*0.16:.2f}s both}}')
        segs.append(f'<path class="d{i}" d="M {x0:.1f} {y0:.1f} A {r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" stroke="{SH[i%len(SH)]}" stroke-width="{th}" stroke-dasharray="{L:.1f}" stroke-dashoffset="0"/>')
        ang+=sweep
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    o.append(f'<defs><style>{"".join(css)} .lg{{animation:app .5s ease both}}</style><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg0"]}"/><stop offset="1" stop-color="{T["bg1"]}"/></linearGradient></defs>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#bg)" stroke="{T["border"]}"/>')
    o.append(f'<path d="M1 15 Q1 1 15 1 H{W-15} Q{W-1} 1 {W-1} 15 V42 H1 Z" fill="{T["bar"]}"/>')
    for i,c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]): o.append(f'<circle cx="{22+i*20}" cy="21" r="5.5" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="26" fill="{T["muted"]}" font-size="13" text-anchor="middle">$ gh languages --top</text>')
    o.extend(segs)
    o.append(f'<text x="{cxc}" y="{cyc+5}" fill="{T["value"]}" font-size="17" font-weight="bold" text-anchor="middle">TOP {len(langs)}</text>')
    ly=92
    for i,(name,pct) in enumerate(langs):
        o.append(f'<g class="lg" style="animation-delay:{0.4+i*0.12:.2f}s"><rect x="230" y="{ly-11}" width="12" height="12" rx="3" fill="{SH[i%len(SH)]}"/>'
                 f'<text x="250" y="{ly}" fill="{T["value"]}" font-size="13.5">{esc(name)}</text>'
                 f'<text x="{W-24}" y="{ly}" fill="{T["muted"]}" font-size="13.5" text-anchor="end">{pct}%</text></g>')
        ly+=33
    o.append('</svg>'); return "\n".join(o)
def main():
    d=json.loads(Path("assets/stats.json").read_text())
    for suf,T in THEMES: Path(f"langs{suf}.svg").write_text(build(d,T),encoding="utf-8")
    print("wrote langs.svg + langs-light.svg")
if __name__=="__main__": main()
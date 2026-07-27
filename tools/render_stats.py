import json, math
from pathlib import Path
from theme import THEMES
FONT="ui-monospace,Menlo,Consolas,monospace"
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def build(d,T):
    W,H=440,300; cxr,cyr,r=104,180,64; pct=d.get("rank_pct",0.4); rank=d.get("rank","B")
    dash=2*math.pi*r; target=dash*(1-pct)
    rows=[("Total contributions",d.get("contributions",0)),("Public repos",d.get("public_repos",0)),
          ("Stars earned",d.get("stars",0)),("Followers",d.get("followers",0))]
    css=(f'@keyframes ring{{from{{stroke-dashoffset:{dash:.1f}}}to{{stroke-dashoffset:{target:.1f}}}}}'
         f'@keyframes app{{from{{opacity:0;transform:translateX(6px)}}to{{opacity:1;transform:translateX(0)}}}}'
         f'.ring{{animation:ring 1.5s cubic-bezier(.4,0,.2,1) .2s both}}'
         + "".join(f'.r{i}{{transform-box:fill-box;animation:app .5s ease {0.5+i*0.18:.2f}s both}}' for i in range(len(rows))))
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    o.append(f'<defs><style>{css}</style><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{T["bg0"]}"/><stop offset="1" stop-color="{T["bg1"]}"/></linearGradient></defs>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#bg)" stroke="{T["border"]}"/>')
    o.append(f'<path d="M1 15 Q1 1 15 1 H{W-15} Q{W-1} 1 {W-1} 15 V42 H1 Z" fill="{T["bar"]}"/>')
    for i,c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]): o.append(f'<circle cx="{22+i*20}" cy="21" r="5.5" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="26" fill="{T["muted"]}" font-size="13" text-anchor="middle">$ gh stats</text>')
    o.append(f'<circle cx="{cxr}" cy="{cyr}" r="{r}" fill="none" stroke="{T["track"]}" stroke-width="10"/>')
    o.append(f'<circle class="ring" cx="{cxr}" cy="{cyr}" r="{r}" fill="none" stroke="{T["accent"]}" stroke-width="10" stroke-linecap="round" stroke-dasharray="{dash:.1f}" stroke-dashoffset="{target:.1f}" transform="rotate(-90 {cxr} {cyr})"/>')
    o.append(f'<text x="{cxr}" y="{cyr-3}" fill="{T["value"]}" font-size="36" font-weight="bold" text-anchor="middle">{esc(rank)}</text>')
    o.append(f'<text x="{cxr}" y="{cyr+22}" fill="{T["muted"]}" font-size="12" text-anchor="middle">rank</text>')
    ry=98
    for i,(k,v) in enumerate(rows):
        o.append(f'<g class="r{i}"><text x="200" y="{ry}" fill="{T["muted"]}" font-size="14">{esc(k)}</text>'
                 f'<text x="{W-24}" y="{ry}" fill="{T["accent"]}" font-size="17" font-weight="bold" text-anchor="end">{esc(v)}</text>'
                 f'<line x1="200" y1="{ry+13}" x2="{W-24}" y2="{ry+13}" stroke="{T["line"]}"/></g>')
        ry+=44
    o.append('</svg>'); return "\n".join(o)
def main():
    d=json.loads(Path("assets/stats.json").read_text())
    for suf,T in THEMES: Path(f"stats{suf}.svg").write_text(build(d,T),encoding="utf-8")
    print("wrote stats.svg + stats-light.svg")
if __name__=="__main__": main()
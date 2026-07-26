"""assets/stats.json -> trophies.svg  (local achievement tiers, cyan theme)."""
import json
from pathlib import Path
BG0="#0b0f17"; BG1="#0d1117"; BAR="#161b22"; VALUE="#e6edf3"; MUTED="#8b949e"
FONT="ui-monospace,Menlo,Consolas,monospace"
TIERCOL={"C":"#5b7f7b","B":"#2f9f96","A":"#2bc0b4","S":"#39d3c3","SS":"#8bece2","SSS":"#c7f7f1"}
def tier(v, thr):
    t="C"
    for lim,name in thr:
        if v>=lim: t=name
    return t
def laurel(cxx, cyy, sgn, col):
    p=[f'<path d="M{cxx+sgn*30} {cyy-30} Q{cxx+sgn*52} {cyy} {cxx+sgn*30} {cyy+30}" fill="none" stroke="{col}" stroke-width="2" stroke-linecap="round" opacity="0.85"/>']
    for k in range(5):
        t=k/4.0; ly=cyy-24+t*48; bulge=(1-abs(t-0.5)*2); lx=cxx+sgn*(34+bulge*14); rot=sgn*(-52)+(t-0.5)*sgn*40
        p.append(f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="8.5" ry="3.3" fill="{col}" opacity="0.9" transform="rotate({rot:.0f} {lx:.1f} {ly:.1f})"/>')
    return "".join(p)
def main():
    d=json.loads(Path("assets/stats.json").read_text())
    langs=len(d.get("languages",[]))
    cats=[("Commits",d.get("contributions",0),"commits",[(1,"C"),(30,"B"),(100,"A"),(300,"S"),(1000,"SS")]),
        ("Repositories",d.get("public_repos",0),"repos",[(1,"C"),(10,"B"),(30,"A"),(70,"S"),(150,"SS")]),
        ("Stars",d.get("stars",0),"stars",[(0,"C"),(10,"B"),(50,"A"),(200,"S")]),
        ("Followers",d.get("followers",0),"followers",[(0,"C"),(10,"B"),(50,"A"),(200,"S")]),
        ("Languages",langs,"langs",[(1,"C"),(3,"B"),(6,"A"),(10,"S")])]
    cw,ch,gap,pad,top=164,188,18,28,68; n=len(cats); W=pad*2+n*cw+(n-1)*gap; H=top+ch+pad
    css=["@keyframes pop{from{opacity:0;transform:translateY(10px) scale(.92)}to{opacity:1;transform:translateY(0) scale(1)}}"]
    for i in range(n): css.append(f'.c{i}{{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.34,1.3,.5,1) {0.15+i*0.13:.2f}s both}}')
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    o.append(f'<defs><style>{"".join(css)}</style><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG0}"/><stop offset="1" stop-color="{BG1}"/></linearGradient>'
             f'<filter id="cardsh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="5" stdDeviation="8" flood-color="#000" flood-opacity="0.45"/></filter></defs>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="url(#bg)" stroke="#222b35"/>')
    o.append(f'<path d="M1 15 Q1 1 15 1 H{W-15} Q{W-1} 1 {W-1} 15 V42 H1 Z" fill="{BAR}"/>')
    for i,c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]): o.append(f'<circle cx="{22+i*20}" cy="21" r="5.5" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="26" fill="{MUTED}" font-size="13" text-anchor="middle">$ gh trophies</text>')
    for i,(name,val,unit,thr) in enumerate(cats):
        t=tier(val,thr); col=TIERCOL[t]; x=pad+i*(cw+gap); cxx=x+cw/2; cyy=top+90
        o.append(f'<g class="c{i}">')
        o.append(f'<rect x="{x}" y="{top}" width="{cw}" height="{ch}" rx="12" fill="#0e151d" stroke="{col}" stroke-opacity="0.45" filter="url(#cardsh)"/>')
        o.append(f'<rect x="{x+cw/2-16}" y="{top+8}" width="32" height="3" rx="1.5" fill="{col}" opacity="0.8"/>')
        o.append(f'<circle cx="{cxx}" cy="{cyy-4}" r="40" fill="{col}" opacity="0.10"/>')
        o.append(f'<text x="{cxx}" y="{top+30}" fill="{MUTED}" font-size="11.5" letter-spacing="1.5" text-anchor="middle">{name.upper()}</text>')
        o.append(laurel(cxx,cyy,-1,col)); o.append(laurel(cxx,cyy,1,col))
        o.append(f'<text x="{cxx}" y="{cyy+15}" fill="{col}" font-size="42" font-weight="bold" text-anchor="middle">{t}</text>')
        o.append(f'<line x1="{x+28}" y1="{top+ch-58}" x2="{x+cw-28}" y2="{top+ch-58}" stroke="#1c2530"/>')
        o.append(f'<text x="{cxx}" y="{top+ch-34}" fill="{VALUE}" font-size="18" font-weight="bold" text-anchor="middle">{val}</text>')
        o.append(f'<text x="{cxx}" y="{top+ch-16}" fill="{MUTED}" font-size="11" text-anchor="middle">{unit}</text>')
        o.append('</g>')
    o.append('</svg>')
    Path("trophies.svg").write_text("\n".join(o),encoding="utf-8"); print("wrote trophies.svg")
if __name__=="__main__": main()
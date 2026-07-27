"""banner.svg + banner-light.svg  (all-SMIL terminal header)."""
import random
from pathlib import Path
from theme import THEMES
FONT="ui-monospace,Menlo,Consolas,monospace"
NAME="PALASH GHOSH DASTIDAR"; PROMPT="./whoami.sh --verbose"; USERHOST="itspalash2506@github: ~"
ROLES=["Software Engineer","AI Systems Engineer","Backend · Distributed Systems","Building carrier-grade systems"]
W,H=920,250; CH=10.8
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def pulse(i,n,delta=0.028):
    s=i/n; e=(i+1)/n; ks=[0.0]; vs=[0]
    def add(k,v):
        k=max(0.0,min(1.0,k))
        if k>ks[-1]+1e-4: ks.append(round(k,4)); vs.append(v)
        else: vs[-1]=v
    add(s-delta,0); add(s+delta,1); add(e-delta,1); add(e+delta,0)
    if ks[-1]<1.0: add(1.0,0)
    return ";".join(f"{k:.4f}" for k in ks), ";".join(str(v) for v in vs)
def build(T):
    ACC=T["accent"]; VAL=T["value"]; MUT=T["muted"]
    n=len(PROMPT); cmdw=n*CH
    vals=";".join(str(round(k*CH+4)) for k in range(n+1)); kt=";".join(f"{k/n:.4f}" for k in range(n+1))
    nr=len(ROLES); RT=nr*2.8; RB=2.7
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">']
    o.append('<defs>'
             f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{T["bg0"]}"/><stop offset="1" stop-color="{T["bg1"]}"/></linearGradient>'
             f'<radialGradient id="glow" cx="0.75" cy="0.2" r="0.6"><stop offset="0" stop-color="{ACC}" stop-opacity="0.14"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>'
             f'<clipPath id="typ" clipPathUnits="userSpaceOnUse"><rect x="66" y="77" width="0" height="22">'
             f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="1.5s" begin="0.4s" fill="freeze" calcMode="discrete"/></rect></clipPath></defs>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#bg)" stroke="{T["border"]}"/>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#glow)"/>')
    for gx in range(0,W,40): o.append(f'<line x1="{gx}" y1="46" x2="{gx}" y2="{H}" stroke="{T["grid"]}" stroke-opacity="{T["gridop"]}"/>')
    for gy in range(60,H,40): o.append(f'<line x1="0" y1="{gy}" x2="{W}" y2="{gy}" stroke="{T["grid"]}" stroke-opacity="{T["gridop"]}"/>')
    rnd=random.Random(7)
    for _ in range(26):
        x=rnd.uniform(20,W-20); y=rnd.uniform(55,H-20); r=rnd.choice([0.7,1.0,1.4])
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{T["star"]}" opacity="{rnd.uniform(0.15,0.5):.2f}"/>')
    o.append(f'<path d="M1 17 Q1 1 17 1 H{W-17} Q{W-1} 1 {W-1} 17 V42 H1 Z" fill="{T["bar"]}"/>')
    for i,c in enumerate(["#ff5f56","#ffbd2e","#27c93f"]): o.append(f'<circle cx="{24+i*22}" cy="21" r="6" fill="{c}"/>')
    o.append(f'<text x="{W/2}" y="26" fill="{MUT}" font-size="13.5" text-anchor="middle">{esc(USERHOST)}</text>')
    o.append(f'<text x="44" y="92" font-size="18" fill="{ACC}">$</text>')
    o.append(f'<text x="70" y="92" font-size="18" fill="{VAL}" clip-path="url(#typ)">{esc(PROMPT)}</text>')
    o.append(f'<rect x="{70+cmdw+4:.0f}" y="77" width="10" height="20" fill="{ACC}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" dur="0.9s" repeatCount="indefinite"/></rect>')
    o.append(f'<text x="44" y="160" font-size="44" font-weight="bold" fill="{VAL}" letter-spacing="1" opacity="0">'
             f'<animate attributeName="opacity" values="0;1" dur="0.6s" begin="1.8s" fill="freeze"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 16;0 0" keyTimes="0;1" keySplines="0.2 0.7 0.3 1" calcMode="spline" dur="0.7s" begin="1.8s" fill="freeze"/>{esc(NAME)}</text>')
    o.append(f'<text x="44" y="202" font-size="19" fill="{MUT}" opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" begin="2.5s" fill="freeze"/>&gt;</text>')
    for i,r in enumerate(ROLES):
        ks,vs=pulse(i,nr); cx2=70+len(r)*CH+4
        o.append(f'<g opacity="0"><animate attributeName="opacity" values="{vs}" keyTimes="{ks}" dur="{RT:.1f}s" begin="{RB}s" repeatCount="indefinite"/>'
                 f'<text x="70" y="202" font-size="19" fill="{ACC}">{esc(r)}</text>'
                 f'<rect x="{cx2:.0f}" y="187" width="10" height="19" fill="{ACC}"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.49;0.5;1" dur="0.9s" repeatCount="indefinite"/></rect></g>')
    o.append('</svg>'); return "\n".join(o)
def main():
    for suf,T in THEMES: Path(f"banner{suf}.svg").write_text(build(T),encoding="utf-8")
    print("wrote banner.svg + banner-light.svg")
if __name__=="__main__": main()

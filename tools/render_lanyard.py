"""Swinging ID badge -> lanyard.svg (smooth sway + full-card 1.5s SMIL shine)."""
import base64, io, random
from pathlib import Path
from PIL import Image

ACCENT="#39d3c3"; VALUE="#e6edf3"; MUTED="#8b949e"; STRAPTXT="#062024"
N1="Palash"; N2="Ghosh Dastidar"; ROLE="SOFTWARE ENGINEER"; HANDLE="@itspalash2506"
IDNO="PG-2506"; SKILLS=["Python · gRPC","React · AWS"]; STRAP="SDE · SDE · SDE · SDE"
FACE_CROP=(280,205,700,625); MONO="ui-monospace,Consolas,monospace"

W,H=390,660; cx=W/2
cardx,cardy,cardw,cardh=40,240,310,372; pad=24
av_cy=cardy+112; av_r=58; strapW=42; strapBot=cardy-64
inner=cardw-2*pad
fs1=min(31, inner*0.85/(0.6*len(N1))); fs2=min(25, inner*0.85/(0.6*len(N2)))
ny1=av_cy+av_r+36
rcx=cx; rcy=cardy+cardh/2
SH_Y=cardy-90; SH_H=cardh+180; SH_W=62; SH_X0=cardx-150; SH_X1=cardx+cardw+150
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def body(b64):
    o=[]
    o.append(f'<rect x="{cx-strapW/2}" y="-6" width="{strapW}" height="{strapBot+6}" fill="{ACCENT}" opacity="0.95"/>')
    o.append(f'<line x1="{cx-strapW/2+6}" y1="0" x2="{cx-strapW/2+6}" y2="{strapBot}" stroke="#eafffb" stroke-opacity="0.75" stroke-width="1.2" stroke-dasharray="1.5 4" stroke-linecap="round"/>')
    o.append(f'<line x1="{cx+strapW/2-6}" y1="0" x2="{cx+strapW/2-6}" y2="{strapBot}" stroke="#eafffb" stroke-opacity="0.75" stroke-width="1.2" stroke-dasharray="1.5 4" stroke-linecap="round"/>')
    o.append(f'<text x="0" y="0" font-family="{MONO}" font-size="11" font-weight="bold" fill="{STRAPTXT}" letter-spacing="3" transform="translate({cx+4.5},24) rotate(90)">{esc(STRAP)}</text>')
    clh=30; clw=54; cly=strapBot
    o.append(f'<rect x="{cx-clw/2}" y="{cly}" width="{clw}" height="{clh}" rx="7" fill="url(#metal)" stroke="#4a4f5c" stroke-width="1.5"/>')
    o.append(f'<rect x="{cx-13}" y="{cly+8}" width="26" height="7" rx="3.5" fill="#3c414e"/>')
    o.append(f'<circle cx="{cx}" cy="{cardy-8}" r="15" fill="none" stroke="url(#metal)" stroke-width="6"/>')
    o.append(f'<rect x="{cardx}" y="{cardy}" width="{cardw}" height="{cardh}" rx="18" fill="url(#cardbg)" stroke="{ACCENT}" stroke-width="1.5" filter="url(#sh)"/>')
    o.append(f'<rect x="{cx-32}" y="{cardy+12}" width="64" height="10" rx="5" fill="#0a0714" stroke="#26424a" stroke-width="1"/>')
    o.append(f'<text x="{cardx+pad}" y="{cardy+42}" font-family="{MONO}" fill="{MUTED}" font-size="11" letter-spacing="2">DEVELOPER ID</text>')
    o.append(f'<text x="{cardx+cardw-pad}" y="{cardy+42}" font-family="{MONO}" fill="{ACCENT}" font-size="12" text-anchor="end" font-weight="bold">{esc(IDNO)}</text>')
    o.append(f'<circle cx="{cx}" cy="{av_cy}" r="{av_r}" fill="none" stroke="{ACCENT}" stroke-width="3" filter="url(#glow)"/>')
    o.append(f'<image href="data:image/png;base64,{b64}" x="{cx-av_r+3}" y="{av_cy-av_r+3}" width="{2*(av_r-3)}" height="{2*(av_r-3)}" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>')
    o.append(f'<text x="{cx}" y="{ny1}" fill="{ACCENT}" font-size="{fs1:.1f}" text-anchor="middle" font-weight="bold" filter="url(#glow)" font-family="Segoe UI,Verdana,sans-serif">{esc(N1)}</text>')
    o.append(f'<text x="{cx}" y="{ny1+30}" fill="{ACCENT}" font-size="{fs2:.1f}" text-anchor="middle" font-weight="bold" filter="url(#glow)" font-family="Segoe UI,Verdana,sans-serif">{esc(N2)}</text>')
    o.append(f'<text x="{cx}" y="{ny1+56}" font-family="{MONO}" fill="{VALUE}" font-size="12.5" text-anchor="middle" letter-spacing="3">{esc(ROLE)}</text>')
    o.append(f'<text x="{cx}" y="{ny1+74}" font-family="{MONO}" fill="{MUTED}" font-size="11.5" text-anchor="middle">{esc(HANDLE)}</text>')
    random.seed(11); bx=cardx+pad; by=cardy+cardh-52
    while bx<cardx+pad+118:
        w=random.choice([1,1,2,3]); o.append(f'<rect x="{bx}" y="{by}" width="{w}" height="34" fill="#cfd8dd"/>'); bx+=w+2
    for i,s in enumerate(SKILLS):
        o.append(f'<text x="{cardx+cardw-pad}" y="{cardy+cardh-44+i*18}" font-family="{MONO}" fill="{VALUE}" font-size="11.5" text-anchor="end">{esc(s)}</text>')
    return "\n".join(o)

def main():
    im=Image.open("assets/me.jpeg").convert("RGB")
    buf=io.BytesIO(); im.crop(FACE_CROP).resize((240,240)).save(buf,format="PNG")
    b64=base64.b64encode(buf.getvalue()).decode()

    rnd=random.Random(42); stars=[]
    for _ in range(80):
        stars.append((rnd.uniform(6,W-6),rnd.uniform(6,H-6),rnd.choice([0.7,0.9,1.1,1.4,1.8]),
                      round(rnd.uniform(2.2,4.2),2),round(rnd.uniform(0,3),2),rnd.random()<0.14))

    css=(f'@keyframes sway{{0%,100%{{transform:rotate(-3.2deg)}}50%{{transform:rotate(3.2deg)}}}}'
         f'@keyframes app{{from{{opacity:0}}to{{opacity:1}}}}'
         f'@keyframes tw{{0%,100%{{opacity:.2}}50%{{opacity:.9}}}}'
         f'.appear{{animation:app .8s ease-out forwards}}'
         f'.sway{{transform-origin:{cx}px 8px;animation:sway 3s ease-in-out infinite}}'
         f'.st{{animation:tw ease-in-out infinite}}')
    defs=(f'<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="2.3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
     f'<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000" flood-opacity="0.5"/></filter>'
     f'<clipPath id="av"><circle cx="{cx}" cy="{av_cy}" r="{av_r-3}"/></clipPath>'
     f'<clipPath id="card"><rect x="{cardx}" y="{cardy}" width="{cardw}" height="{cardh}" rx="18"/></clipPath>'
     f'<linearGradient id="shineg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.32"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
     f'<linearGradient id="cardbg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#123039"/><stop offset="1" stop-color="#0c1a20"/></linearGradient>'
     f'<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e4e8f0"/><stop offset="45%" stop-color="#9aa0b0"/><stop offset="55%" stop-color="#6a7080"/><stop offset="100%" stop-color="#aeb4c4"/></linearGradient>'
     f'<radialGradient id="vign" cx="0.5" cy="0.4" r="0.72"><stop offset="0" stop-color="#0f1626"/><stop offset="1" stop-color="#070a12"/></radialGradient>')

    o=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Palash Ghosh Dastidar ID badge">']
    o.append(f'<defs><style>{css}</style>{defs}</defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#vign)"/>')
    for (x,y,r,dur,dl,big) in stars:
        if big:
            s=r*3.4
            o.append(f'<path class="st" style="animation-duration:{dur}s;animation-delay:{dl}s" d="M{x:.1f} {y-s:.1f}L{x+s*0.28:.1f} {y-s*0.28:.1f}L{x+s:.1f} {y:.1f}L{x+s*0.28:.1f} {y+s*0.28:.1f}L{x:.1f} {y+s:.1f}L{x-s*0.28:.1f} {y+s*0.28:.1f}L{x-s:.1f} {y:.1f}L{x-s*0.28:.1f} {y-s*0.28:.1f}Z" fill="{ACCENT}"/>')
        else:
            o.append(f'<circle class="st" style="animation-duration:{dur}s;animation-delay:{dl}s" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#dfe8ff"/>')
    o.append('<g class="appear"><g class="sway">')
    o.append(body(b64))
    o.append(f'<g clip-path="url(#card)"><g transform="rotate(18 {rcx} {rcy})">'
             f'<rect x="{SH_X0}" y="{SH_Y}" width="{SH_W}" height="{SH_H}" fill="url(#shineg)" opacity="0">'
             f'<animate attributeName="x" values="{SH_X0};{SH_X1};{SH_X1}" keyTimes="0;0.4;1" dur="1.5s" repeatCount="indefinite" calcMode="linear"/>'
             f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.35;0.42;1" dur="1.5s" repeatCount="indefinite"/>'
             f'</rect></g></g>')
    o.append('</g></g></svg>')
    Path("lanyard.svg").write_text("\n".join(o),encoding="utf-8")
    print("wrote lanyard.svg")

if __name__=="__main__":
    main()
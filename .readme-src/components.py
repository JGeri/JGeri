import json, os, random
from lib import *

ICONS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons.json")))
CARD_R = 20
MB = 12  # transparent bottom margin so stacked cards breathe like the side-by-side gap


def card(d, P, x, y, w, h, r=CARD_R):
    d.add(f'<rect x="{f2(x)}" y="{f2(y)}" width="{f2(w)}" height="{f2(h)}" rx="{r}" fill="{P.bg}" stroke="{P.line}"/>')


# =============================================================== section header
def header(theme, num, title, caption):
    P = THEMES[theme]
    W, H = 1000, 76
    d = Doc(W, H, f"{num} {title}", f"{num} {title}: {caption.lower()}")
    nx = tw(num, "serif-i", 36)
    d.add(d.text(2, 48, num, "serif-i", 36, P.red))
    d.add(d.text(2 + nx + 12, 48, title, "serif", 36, P.ink, ls=-0.3))
    d.add(d.text(998, 45, caption, "mono", 10.5, P.muted, weight=500, ls=1.6, anchor="end"))
    d.add(f'<line x1="0" y1="66.5" x2="1000" y2="66.5" stroke="{P.line2}"/>')
    d.add(f'<line x1="0" y1="66.5" x2="56" y2="66.5" stroke="{P.red}" stroke-width="2"/>')
    return d.render()


# =============================================================== I. prelude
def prelude(theme):
    P = THEMES[theme]
    W, H = 1000, 384
    d = Doc(W, H, "Prelúdium",
            "A kódolás számomra olyan, mint a zeneszerzés: struktúrát, ritmust és hibátlan végrehajtást követel.")
    card(d, P, .5, .5, W - 1, H - 1)
    d.add(d.text(40, 84, "", "serif", 33, P.ink, ls=-0.3, inner=[
        ("serif", "„", f'fill="{P.red}"'), ("serif", "A kódolás számomra olyan, mint a zeneszerzés:", "")]))
    d.add(d.text(40, 126, "", "serif-i", 33, P.ink, ls=-0.3, inner=[
        ("serif-i", "struktúrát, ritmust és hibátlan végrehajtást követel.", ""),
        ("serif", "”", f'fill="{P.red}"')]))
    d.add(f'<line x1="40" y1="166.5" x2="960" y2="166.5" stroke="{P.line}"/>')
    cols = [
        ("ÉPÍTEM", "VibeSite: AI-alapú weboldal- és digitális jelenlét platform magyar KKV-knak."),
        ("KUTATOM", "Protokollkövető klinikai LLM-ágens, ellenőrizhető döntési utakkal. BSc szakdolgozat."),
        ("VEZETEM", "Fejlesztési vezetőként kis csapattal építünk munkahelyi AI és gépi látás rendszereket."),
        ("JÁTSZOM", "Több mint 10 éve klasszikus gitáron. A frekvenciák matematikája innen indult."),
    ]
    cw, gap = 206, 32
    for i, (lab, txt) in enumerate(cols):
        x = 40 + i * (cw + gap)
        d.add(d.text(x, 204, f"0{i+1}", "mono", 10, P.red, weight=500, ls=1))
        d.add(d.text(x + 26, 204, lab, "mono", 10, P.ink2, weight=500, ls=1.8))
        for j, ln in enumerate(wrap(txt, cw, "sans", 14.5)):
            d.add(d.text(x, 234 + j * 21.5, ln, "sans", 14.5, P.muted, ls=-0.1))
    d.add(f'<line x1="40" y1="324.5" x2="960" y2="324.5" stroke="{P.line}"/>')
    d.add(d.text(40, 352, "BME VIK · MÉRNÖKINFORMATIKUS BSc · 2023–2027 · AI/ML SPECIALIZÁCIÓ", "mono", 10,
                 P.muted, weight=500, ls=1.5))
    d.add(d.text(960, 352, "", "mono", 10, P.muted, weight=500, ls=1.5, anchor="end", inner=[
        ("mono", "ÁTLAG ", ""), ("mono", "4.5+", f'fill="{P.red}"')]))
    return d.render()


# =============================================================== II. opus — featured VibeSite
def sparkle(cx, cy, r, fill):
    k = r * 0.22
    return (f'<path d="M{cx} {cy-r} Q{cx+k} {cy-k} {cx+r} {cy} Q{cx+k} {cy+k} {cx} {cy+r} '
            f'Q{cx-k} {cy+k} {cx-r} {cy} Q{cx-k} {cy-k} {cx} {cy-r}Z" fill="{fill}"/>')


def appear(inner, ta, T, out=9.2, dy=8):
    return ('<g opacity="0">'
            + anim("opacity", [(0, 0), (ta, 0), (ta + .35, 1), (out, 1), (out + .4, 0)], T)
            + anim_tf("translate", [(0, f"0 {dy}"), (ta, f"0 {dy}"), (ta + .35, "0 0"), (out + .4, "0 0"),
                                    (out + .41, f"0 {dy}")], T, "spline", ".2 .7 .3 1")
            + inner + "</g>")


def op_vibesite(theme):
    P = THEMES[theme]
    W, H = 1000, 404
    T = 10.0
    d = Doc(W, H + MB, "Op. 1: VibeSite",
            "VibeSite: AI-alapú weboldal- és digitális jelenlét platform magyar KKV-knak. vibesite.hu")
    card(d, P, .5, .5, W - 1, H - 1)
    d.add(d.text(40, 58, "OP. 1 — ZÁSZLÓSHAJÓ", "mono", 10.5, P.red, weight=500, ls=1.6))
    d.add(d.text(40, 124, "VibeSite", "serif", 66, P.ink, ls=-0.8))
    tx = 40 + tw("VibeSite", "serif", 66, ls=-0.8) + 16
    # live pill
    d.add(f'<rect x="{f2(tx)}" y="94" width="78" height="22" rx="11" fill="none" stroke="{P.line2}"/>')
    d.add(f'<circle cx="{f2(tx+13)}" cy="105" r="3.2" fill="{P.red}"><animate attributeName="opacity" '
          f'values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    d.add(d.text(tx + 23, 108.6, "ÉLESBEN", "mono", 9.5, P.ink2, weight=500, ls=1.2))
    for j, ln in enumerate(wrap("AI-alapú weboldal- és digitális jelenlét platform magyar KKV-knak: "
                                "egyetlen leírásból kész, élő weboldal.", 430, "sans", 15.5)):
        d.add(d.text(40, 164 + j * 23, ln, "sans", 15.5, P.ink2, ls=-0.1))
    feats = ["AI weboldal-generátor: landing, webshop, blog", "AI e-mail asszisztens",
             "Időpontfoglalás · Google Cégprofil"]
    for j, f in enumerate(feats):
        d.add(d.text(40, 230 + j * 22, "", "mono", 11.5, P.ink2, ls=0.2, inner=[
            ("mono", "→  ", f'fill="{P.red}"'), ("mono", f, "")]))
    x = 40
    for c in ["Astro", "React", "Tailwind", "Python", "MongoDB", "Docker"]:
        x += pill(d, x, 304, c, P, size=10, ls=0.4, h=23, padx=10) + 6
    d.add(d.text(40, 370, "", "mono", 12, P.ink, weight=500, ls=0.4, inner=[
        ("mono", "vibesite.hu ", ""), ("mono", "↗", f'fill="{P.red}"')]))
    bx = 40 + tw("vibesite.hu ↗", "mono", 12, 500, 0.4) + 18
    pill(d, bx, 355, "TV · CÁPÁK KÖZÖTT", P, size=9.5, ls=1.2, h=22, padx=10, stroke=P.red, color=P.red)

    # ---- browser mock
    ox, oy, bw, bh = 500, 36, 460, 332
    d.defs.append(f'<clipPath id="bw"><rect x="{ox}" y="{oy}" width="{bw}" height="{bh}" rx="12"/></clipPath>')
    d.add(f'<rect x="{ox}" y="{oy}" width="{bw}" height="{bh}" rx="12" fill="{P.panel}" stroke="{P.line2}"/>')
    for k in range(3):
        d.add(f'<circle cx="{ox+18+k*13}" cy="{oy+17}" r="4" fill="{P.line2}"/>')
    d.add(f'<rect x="{ox+130}" y="{oy+8}" width="200" height="18" rx="9" fill="{P.panel2}"/>')
    d.add(d.text(ox + 230, oy + 20.5, "pelda.vibesite.hu", "mono", 9.5, P.muted, anchor="middle", ls=0.3))
    d.add(f'<line x1="{ox}" y1="{oy+34.5}" x2="{ox+bw}" y2="{oy+34.5}" stroke="{P.line}"/>')
    # prompt bar
    px, py = ox + 16, oy + 48
    d.add(f'<rect x="{px}" y="{py}" width="{bw-32}" height="36" rx="10" fill="{P.bg}" stroke="{P.line2}"/>')
    d.add(sparkle(px + 17, py + 18, 6.5, P.red))
    prompt = "Fodrászszalon Budapesten, online foglalással"
    tx0, tyb, fs = px + 32, py + 22.5, 12.5
    d.add(d.text(tx0, tyb, prompt, "sans", fs, P.ink2, extra='clip-path="url(#tp)"'))
    # typing: discrete reveal per character
    t_a, t_b = 0.6, 2.7
    ks, cur = [(0, 0)], [(0, tx0)]
    for i in range(1, len(prompt) + 1):
        t = t_a + (t_b - t_a) * i / len(prompt)
        wv = tw(prompt[:i], "sans", fs)
        ks.append((t, round(wv + 1, 1)))
        cur.append((t, round(tx0 + wv + 1.5, 1)))
    ks += [(9.55, ks[-1][1]), (9.6, 0)]
    cur += [(9.55, cur[-1][1]), (9.6, tx0)]
    d.defs.append(f'<clipPath id="tp"><rect x="{tx0}" y="{py+4}" width="0" height="28">'
                  + anim("width", ks, T, "discrete") + "</rect></clipPath>")
    d.css.append(".cur{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    d.add(f'<rect class="cur" x="{tx0}" y="{py+11}" width="1.4" height="15" fill="{P.red}">'
          + anim("x", cur, T, "discrete") + "</rect>")
    # generate button
    gbx = ox + bw - 16 - 6 - 72
    d.add(f'<g><rect x="{gbx}" y="{py+6}" width="72" height="24" rx="7" fill="{P.red}">'
          + anim("opacity", [(0, 1), (2.85, 1), (2.95, .55), (3.15, 1)], T) + "</rect>"
          + d.text(gbx + 36, py + 21.8, "Generálás", "sans", 10.5, "#FFFFFF", weight=600, anchor="middle")
          + "</g>")
    # progress
    d.add(f'<rect x="{ox}" y="{oy+92}" width="0" height="2" fill="{P.red}">'
          + anim("width", [(0, 0), (2.95, 0), (5.3, bw), (5.6, bw), (5.61, 0)], T, "spline", ".3 .1 .3 1")
          + anim("opacity", [(0, 1), (5.3, 1), (5.6, 0), (5.61, 1)], T) + "</rect>")
    # site skeleton (relative coords inside viewport)
    sx, sy = ox + 16, oy + 104

    def R(x, y, w, h, fill, r=3, extra=""):
        return f'<rect x="{f2(sx+x)}" y="{f2(sy+y)}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'

    nav = (f'<circle cx="{sx+6}" cy="{sy+8}" r="5.5" fill="{P.red}"/>' + R(16, 4.5, 52, 7, P.ink)
           + R(262, 5.5, 26, 5, P.faint) + R(296, 5.5, 26, 5, P.faint) + R(330, 5.5, 26, 5, P.faint)
           + R(370, 0, 58, 16, P.red, 8))
    d.add(appear(nav, 3.15, T))
    d.add(appear(R(0, 32, 196, 14, P.ink, 3), 3.4, T))
    d.add(appear(R(0, 52, 150, 14, P.ink, 3), 3.55, T))
    d.add(appear(R(0, 78, 204, 5, P.faint, 2.5) + R(0, 89, 176, 5, P.faint, 2.5) + R(0, 100, 120, 5, P.faint, 2.5),
                 3.75, T))
    d.add(appear(R(0, 118, 78, 22, P.red, 11) + R(16, 127, 46, 4, "#FFFFFF", 2, 'opacity=".85"')
                 + R(86, 118, 66, 22, "none", 11, f'stroke="{P.line2}"'), 3.95, T))
    img = (R(232, 28, 196, 116, P.panel2, 9)
           + f'<circle cx="{sx+392}" cy="{sy+58}" r="11" fill="{P.red}" opacity=".85"/>'
           + f'<path d="M{sx+232} {sy+132} L{sx+290} {sy+82} L{sx+330} {sy+112} L{sx+360} {sy+92} L{sx+428} {sy+136} '
             f'L{sx+428} {sy+144} L{sx+232} {sy+144}Z" fill="{P.line2}"/>')
    d.add(f'<g clip-path="url(#bw)">' + appear(img, 4.15, T) + "</g>")
    for k in range(3):
        cx = 146 * k
        c = (R(cx, 160, 136, 58, P.bg, 8, f'stroke="{P.line}"') + R(cx + 12, 172, 12, 12, P.red, 3)
             + R(cx + 12, 192, 92, 5, P.ink2, 2.5, 'opacity=".7"') + R(cx + 12, 203, 64, 5, P.faint, 2.5))
        d.add(appear(c, 4.45 + k * .15, T))
    # toast
    tw_ = 214
    tx_, ty_ = ox + bw - 16 - tw_, oy + bh - 16 - 34
    toast = (f'<rect x="{tx_}" y="{ty_}" width="{tw_}" height="34" rx="9" fill="{P.ink}"/>'
             f'<circle cx="{tx_+18}" cy="{ty_+17}" r="7" fill="{P.red}"/>'
             f'<path d="M{tx_+14.6} {ty_+17.2} l2.4 2.4 l4.4 -4.6" stroke="#FFF" stroke-width="1.6" '
             f'stroke-linecap="round" stroke-linejoin="round"/>'
             + d.text(tx_ + 32, ty_ + 21.2, "Közzétéve · pelda.vibesite.hu", "sans", 11, P.bg, weight=500))
    d.add('<g opacity="0">' + anim("opacity", [(0, 0), (5.7, 0), (6.0, 1), (8.4, 1), (8.7, 0)], T)
          + anim_tf("translate", [(0, "0 10"), (5.7, "0 10"), (6.0, "0 0"), (8.7, "0 0"), (8.71, "0 10")], T,
                    "spline", ".2 .7 .3 1") + toast + "</g>")
    return d.render()


# =============================================================== II. opus — small cards
def small_card(theme, side, kicker, status, title, desc, tags, visual, title_alt, link_hint=None):
    P = THEMES[theme]
    W, H = 500, 344
    d = Doc(W, H + MB, title_alt, f"{title}: {desc}")
    x0 = .5 if side == "L" else 8.5
    card(d, P, x0, .5, 491, H - 1)
    ox = x0 + 28
    d.add(d.text(ox, 50, kicker, "mono", 10, P.red, weight=500, ls=1.5))
    d.add(d.text(x0 + 491 - 28, 50, status, "mono", 9.5, P.muted, weight=500, ls=1.2, anchor="end"))
    d.add(d.text(ox, 92, title, "serif", 34, P.ink, ls=-0.4))
    for j, ln in enumerate(wrap(desc, 432, "sans", 13.5)):
        d.add(d.text(ox, 122 + j * 20, ln, "sans", 13.5, P.muted, ls=-0.05))
    visual(d, P, ox)
    d.add(f'<line x1="{ox}" y1="300.5" x2="{x0+491-28}" y2="300.5" stroke="{P.line}"/>')
    d.add(d.text(ox, 324, tags, "mono", 9.5, P.muted, weight=500, ls=1.1))
    if link_hint:
        d.add(d.text(x0 + 491 - 28, 324, "", "mono", 9.5, P.ink2, weight=500, ls=1.1, anchor="end", inner=[
            ("mono", link_hint + " ", ""), ("mono", "↗", f'fill="{P.red}"')]))
    return d.render()


def vis_decision(d, P, ox):
    T = 9.0
    cx = [ox + 14, ox + 116, ox + 218, ox + 320, ox + 418]
    mid = 232
    N = {"S": (cx[0], mid), "A1": (cx[1], mid - 26), "A2": (cx[1], mid + 26), "B1": (cx[2], mid - 38),
         "B2": (cx[2], mid), "B3": (cx[2], mid + 38), "C1": (cx[3], mid - 20), "C2": (cx[3], mid + 22),
         "E": (cx[4], mid)}
    E = [("S", "A1"), ("S", "A2"), ("A1", "B1"), ("A1", "B2"), ("A2", "B2"), ("A2", "B3"), ("B1", "C1"),
         ("B2", "C1"), ("B2", "C2"), ("B3", "C2"), ("C1", "E"), ("C2", "E")]

    def seg(a, b):
        (x1, y1), (x2, y2) = N[a], N[b]
        m = (x1 + x2) / 2
        return f"C{m} {y1} {m} {y2} {x2} {y2}"

    for a, b in E:
        d.add(f'<path d="M{N[a][0]} {N[a][1]} {seg(a, b)}" stroke="{P.line2}" stroke-width="1.2"/>')
    route = ["S", "A1", "B2", "C2", "E"]
    p = f"M{N['S'][0]} {N['S'][1]} " + " ".join(seg(route[i], route[i + 1]) for i in range(4))
    t0, t1 = 0.6, 3.6
    d.add(f'<path d="{p}" pathLength="1000" stroke="{P.red}" stroke-width="2.2" stroke-linecap="round" '
          f'stroke-dasharray="1000 1000" stroke-dashoffset="1000">'
          + anim("stroke-dashoffset", [(0, 1000), (t0, 1000), (t1, 0), (8.0, 0), (8.01, 1000)], T)
          + anim("opacity", [(0, 1), (7.6, 1), (8.0, 0), (8.01, 1)], T) + "</path>")
    for k, n in enumerate(N):
        x, y = N[n]
        r = 8 if n == "E" else 4.6
        d.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P.bg}" stroke="{P.line2 if n != "E" else P.faint}" '
              f'stroke-width="1.3"/>')
    for k, n in enumerate(route):
        x, y = N[n]
        tr = t0 + (t1 - t0) * k / 4
        r = 8 if n == "E" else 4.6
        d.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P.red}" opacity="0">'
              + anim("opacity", [(0, 0), (tr - .02, 0), (tr + .12, 1), (7.6, 1), (8.0, 0)], T) + "</circle>")
        if n == "E":
            d.add(f'<path d="M{x-3.4} {y+.2} l2.4 2.5 l4.6 -5" stroke="#FFF" stroke-width="1.7" fill="none" '
                  f'stroke-linecap="round" stroke-linejoin="round" opacity="0">'
                  + anim("opacity", [(0, 0), (tr + .1, 0), (tr + .3, 1), (7.6, 1), (8.0, 0)], T) + "</path>")
            d.add(f'<circle cx="{x}" cy="{y}" r="8" stroke="{P.red}" opacity="0">'
                  + anim("r", [(0, 8), (tr, 8), (tr + 1.0, 22)], T, "spline", ".2 .6 .4 1")
                  + anim("opacity", [(0, 0), (tr, 0), (tr + .02, .7), (tr + 1.0, 0)], T) + "</circle>")
    d.add(d.text(N["S"][0] - 8, mid + 52, "TÜNETEK", "mono", 8.5, P.faint, ls=1))
    d.add(d.text(N["E"][0] + 8, mid + 52, "AJÁNLÁS", "mono", 8.5, P.faint, ls=1, anchor="end"))
    d.add(d.text(cx[2], mid + 52, "PROTOKOLL-ÚT · NAPLÓZVA", "mono", 8.5, P.faint, ls=1, anchor="middle"))


def vis_gpu(d, P, ox):
    T = 6.0
    rnd = random.Random(7)
    ys = [192, 214, 236, 258]
    bx0, bw = ox + 70, 160
    box = (ox + 326, 205, 106, 52)
    for i, y in enumerate(ys):
        # fan
        sp = [0.7, 0.9, 0.6, 1.1][i]
        blades = "".join(
            f'<path d="M{ox+9} {y} q2.8 -5.6 0 -6.6" stroke="{P.ink2}" stroke-width="1.3" stroke-linecap="round" '
            f'transform="rotate({a} {ox+9} {y})"/>' for a in (0, 120, 240))
        d.add(f'<circle cx="{ox+9}" cy="{y}" r="7.5" stroke="{P.line2}"/>')
        d.add(f'<g>{blades}<animateTransform attributeName="transform" type="rotate" from="0 {ox+9} {y}" '
              f'to="360 {ox+9} {y}" dur="{sp}s" repeatCount="indefinite"/></g>')
        d.add(d.text(ox + 24, y + 3.5, f"GPU{i}", "mono", 9.5, P.ink2, weight=500, ls=.6))
        d.add(f'<rect x="{bx0}" y="{y-3}" width="{bw}" height="6" rx="3" fill="{P.panel2}"/>')
        ks = [(0, 0.55)] + [(t, rnd.uniform(0.35, 0.98)) for t in (0.8, 1.7, 2.6, 3.4, 4.3, 5.2)] + [(T, 0.55)]
        d.add(f'<rect x="{bx0}" y="{y-3}" width="{bw*0.55:.1f}" height="6" rx="3" fill="{P.red}">'
              + anim("width", [(t, round(v * bw, 1)) for t, v in ks], T, "spline") + "</rect>")
        path = f"M{bx0+bw+8} {y} C{bx0+bw+50} {y} {box[0]-40} {box[1]+box[3]/2} {box[0]} {box[1]+box[3]/2}"
        d.add(f'<path d="{path}" stroke="{P.line2}" stroke-width="1.1"/>')
        d.add(f'<circle r="2.4" fill="{P.red}"><animateMotion dur="1.5s" begin="-{i*0.37:.2f}s" '
              f'repeatCount="indefinite" path="{path}" keyPoints="0;1" keyTimes="0;1" calcMode="spline" '
              f'keySplines=".5 0 .5 1"/></circle>')
    x, y, w, h = box
    d.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{P.panel}" stroke="{P.line2}"/>')
    d.add(d.text(x + w / 2, y + 23, "LLM API", "mono", 11, P.ink, weight=600, anchor="middle", ls=.6))
    d.add(d.text(x + w / 2, y + 39, "vfio · docker", "mono", 8.5, P.muted, anchor="middle", ls=.4))
    d.add(d.text(ox, 282, "KVM HOST · 4× PCIe PASSTHROUGH", "mono", 8.5, P.faint, ls=1))


def vis_cv(d, P, ox):
    T = 9.0
    vx, vy, vw, vh = ox, 176, 246, 108
    d.add(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="9" fill="{P.panel2}"/>')
    # viewfinder corners
    L = 10
    for (cx, cy, sx, sy) in [(vx + 7, vy + 7, 1, 1), (vx + vw - 7, vy + 7, -1, 1), (vx + 7, vy + vh - 7, 1, -1),
                             (vx + vw - 7, vy + vh - 7, -1, -1)]:
        d.add(f'<path d="M{cx} {cy+sy*L} V{cy} H{cx+sx*L}" stroke="{P.ink2}" stroke-width="1.4" opacity=".7"/>')
    d.add(f'<circle cx="{vx+20}" cy="{vy+20}" r="3" fill="{P.red}"><animate attributeName="opacity" '
          f'values="1;.2;1" dur="1.2s" repeatCount="indefinite"/></circle>')
    d.add(d.text(vx + 28, vy + 23.3, "CAM-01 · YOLOv8", "mono", 8.5, P.ink2, ls=.8))
    shelves = [(vy + 64, 7), (vy + 98, 6)]
    items = []
    for sy, n in shelves:
        d.add(f'<line x1="{vx+12}" y1="{sy+.5}" x2="{vx+vw-12}" y2="{sy+.5}" stroke="{P.line2}" stroke-width="1.5"/>')
        for k in range(n):
            items.append((vx + 30 + k * 31, sy - 8))
    for (x, y) in items:
        d.add(f'<ellipse cx="{x}" cy="{y}" rx="10.5" ry="7" fill="{P.faint}" opacity=".55"/>')
    for k, (x, y) in enumerate(items):
        ta = 0.5 + k * 0.2
        d.add(f'<rect x="{x-13.5}" y="{y-11}" width="27" height="20" rx="2.5" stroke="{P.red}" stroke-width="1.2" '
              f'opacity="0">' + anim("opacity", [(0, 0), (ta, 0), (ta + .08, 1), (7.8, 1), (8.1, 0)], T) + "</rect>")
    # counter
    cx0 = ox + 268
    for v in range(len(items) + 1):
        ta = 0.5 + (v - 1) * 0.2 if v else 0
        tb = 0.5 + v * 0.2 if v < len(items) else 8.1
        ks = [(0, 1 if v == 0 else 0)]
        if v:
            ks += [(ta, 1)]
        ks += [(tb, 0)]
        if v == 0:
            ks += [(8.1, 1)]
        d.add(d.text(cx0, 222, str(v), "serif", 46, P.ink, extra='opacity="0"').replace(
            "</text>", anim("opacity", ks, T, "discrete") + "</text>"))
    d.add(d.text(cx0, 240, "DB A POLCON", "mono", 8.5, P.muted, ls=1))
    # EWMA sparkline
    pts = []
    rnd = random.Random(3)
    v = 13
    for i in range(14):
        v = max(1.5, v - rnd.uniform(0.3, 1.4))
        pts.append((cx0 + i * 12, 252 + (13 - v) * 2.1))
    pl = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    d.add(f'<polyline points="{pl}" stroke="{P.line2}" stroke-width="1.2"/>')
    d.add(f'<polyline points="{pl}" stroke="{P.red}" stroke-width="1.6" pathLength="100" stroke-dasharray="100 100" '
          f'stroke-dashoffset="100" stroke-linejoin="round">'
          + anim("stroke-dashoffset", [(0, 100), (3.3, 100), (5.6, 0), (8.0, 0), (8.01, 100)], T) + "</polyline>")
    d.add(d.text(cx0, 284, "EWMA → UTÁNTÖLTÉS", "mono", 8.5, P.faint, ls=1))


def vis_agents(d, P, ox):
    T = 8.0
    doc = (ox + 216, 230)
    ag = [(ox + 42, 202, "A1"), (ox + 42, 258, "A2"), (ox + 390, 202, "A3"), (ox + 390, 258, "A4")]
    paths = []
    for (x, y, _) in ag:
        side = 1 if x < doc[0] else -1
        ex = doc[0] - side * 20
        p = f"M{x + side*15} {y} C{x + side*80} {y} {ex - side*60} {doc[1]} {ex} {doc[1]}"
        paths.append(p)
        d.add(f'<path d="{p}" stroke="{P.line2}" stroke-width="1.1"/>')
    # document
    dx, dy = doc[0] - 16, doc[1] - 21
    d.add(f'<path d="M{dx} {dy} h22 l10 10 v32 h-32Z" fill="{P.panel}" stroke="{P.ink2}" stroke-width="1.2" '
          f'stroke-linejoin="round"/>')
    d.add(f'<path d="M{dx+22} {dy} v10 h10" stroke="{P.ink2}" stroke-width="1.2" stroke-linejoin="round"/>')
    for k in range(4):
        d.add(f'<rect x="{dx+6}" y="{dy+16+k*6}" width="{20 - (k%2)*6}" height="2" rx="1" fill="{P.faint}"/>')
    d.add(d.text(doc[0], doc[1] + 38, "TP-DOKUMENTÁCIÓ", "mono", 8.5, P.faint, ls=1, anchor="middle"))
    order = [0, 2, 1, 3]
    for k, i in enumerate(order):
        t0 = 0.4 + k * 1.6
        # message to doc, then back
        d.add(f'<circle r="2.8" fill="{P.red}" opacity="0"><animateMotion dur="{T}s" repeatCount="indefinite" '
              f'path="{paths[i]}" keyPoints="0;0;1;1;0;0" keyTimes="0;{t0/T:.3f};{(t0+.6)/T:.3f};{(t0+.75)/T:.3f};'
              f'{(t0+1.35)/T:.3f};1" calcMode="linear"/>'
              + anim("opacity", [(0, 0), (t0 - .01, 0), (t0, 1), (t0 + 1.35, 1), (t0 + 1.36, 0)], T) + "</circle>")
    for i, (x, y, lab) in enumerate(ag):
        k = order.index(i)
        t0 = 0.4 + k * 1.6
        d.add(f'<circle cx="{x}" cy="{y}" r="15" fill="{P.bg}" stroke="{P.line2}" stroke-width="1.3">'
              + anim("stroke", [(0, P.line2), (t0, P.line2), (t0 + .05, P.red), (t0 + .5, P.red), (t0 + .7, P.line2),
                                (t0 + 1.3, P.line2), (t0 + 1.35, P.red), (t0 + 1.9, P.red), (t0 + 2.2, P.line2)], T)
              + "</circle>")
        d.add(d.text(x, y + 3.4, lab, "mono", 9.5, P.ink2, weight=600, anchor="middle"))


def op_cards(theme):
    out = {}
    out["op2"] = small_card(
        theme, "L", "OP. 2 — KUTATÁS", "BSc · BME · 2026", "Klinikai protokoll-ágens",
        "LLM-ágens, amely klinikai protokollt követ, és minden döntését visszakövethető, ellenőrizhető úton hozza "
        "meg. Összevetve a protokoll nélküli ágenssel.",
        "LLM-ÁGENSEK · ONTOLÓGIA · JSON-PROTOKOLL", vis_decision, "Op. 2: Klinikai protokoll-ágens")
    out["op3"] = small_card(
        theme, "R", "OP. 3 — INFRASTRUKTÚRA", "WISE ITC · 2026", "GPU-s LLM-kiszolgálás",
        "LLM-kiszolgáló infrastruktúra egy 4 GPU-s szerveren: KVM/VFIO PCIe passthrough és konténerizált "
        "szolgáltatások.",
        "KVM · VFIO · DOCKER COMPOSE · LINUX", vis_gpu, "Op. 3: GPU-s LLM-kiszolgálás")
    out["op4"] = small_card(
        theme, "L", "OP. 4 — GÉPI LÁTÁS", "CSAPATVEZETÉS", "Polcfigyelő gépi látás",
        "YOLOv8 Raspberry Pi kamerákon: valós idejű termékszámlálás, EWMA-alapú fogyásbecslés és "
        "utántöltés-előrejelzés.",
        "YOLOv8 · RASPBERRY PI · FASTAPI · REACT", vis_cv, "Op. 4: Polcfigyelő gépi látás")
    out["op5"] = small_card(
        theme, "R", "OP. 5 — HACKATHON", "PwC AI HACKATHON", "NECTAR TP",
        "Multi-ágens auditor transzferár-dokumentációhoz, a magyar adózási megfelelés kontextusában. "
        "Csapatmunka.",
        "MULTI-ÁGENS · LLM · COMPLIANCE", vis_agents, "Op. 5: NECTAR TP", link_hint="REPO")
    return out


# =============================================================== III. stack as a score
ROWS = [
    ("Intelligencia", "AI · ML · EDGE", "mf",
     [("python", "Python"), ("ultralytics", "YOLOv8"), ("raspberrypi", "Raspberry Pi"), ("claude", "Claude"),
      ("gemini", "Gemini")], [0, 2, 1, -1, 1]),
    ("Backend", "API · SZOLGÁLTATÁS", "f",
     [("fastapi", "FastAPI"), ("springboot", "Spring Boot"), ("go", "Go"), ("rust", "Rust")], [1, -1, 2, 0]),
    ("Frontend", "WEB · MOBIL", "mp",
     [("react", "React"), ("nextjs", "Next.js"), ("astro", "Astro"), ("tailwind", "Tailwind"),
      ("svelte", "Svelte"), ("flutter", "Flutter")], [-1, 1, 2, 0, 1, -2]),
    ("Adat", "TÁROLÁS · CACHE", "p",
     [("postgresql", "PostgreSQL"), ("redis", "Redis"), ("mongodb", "MongoDB"), ("sqlite", "SQLite"),
      ("firebase", "Firebase")], [0, 2, -1, 1, 0]),
    ("Infrastruktúra", "DEVOPS · FELHŐ", "ff",
     [("linux", "Linux"), ("docker", "Docker"), ("kubernetes", "Kubernetes"), ("nginx", "NGINX"),
      ("cloudflare", "Cloudflare"), ("githubactions", "Actions")], [2, 0, 1, -1, 1, 2]),
]


def stack(theme):
    P = THEMES[theme]
    W, H = 1000, 556
    T = 13.0
    d = Doc(W, H, "Hangszerelés: technológiák",
            "Technológiák partitúraként: " + "; ".join(f"{r[0]}: " + ", ".join(n for _, n in r[3]) for r in ROWS))
    card(d, P, .5, .5, W - 1, H - 1)
    # tempo marking
    d.add(d.text(214, 58, "Allegro con brio", "serif-i", 22, P.ink))
    qx = 214 + tw("Allegro con brio", "serif-i", 22) + 18
    d.add(f'<ellipse cx="{qx}" cy="{53.5}" rx="5.2" ry="3.7" transform="rotate(-22 {qx} 53.5)" fill="{P.ink}"/>')
    d.add(f'<line x1="{qx+4.6}" y1="52" x2="{qx+4.6}" y2="33" stroke="{P.ink}" stroke-width="1.3"/>')
    d.add(d.text(qx + 12, 58, "= 140", "serif", 18, P.ink2))
    d.add(d.text(960, 56, "PARTITÚRA · 5 SZÓLAM · 26 HANGSZER", "mono", 10, P.muted, weight=500, ls=1.5,
                 anchor="end"))
    ys = [140 + r * 86 for r in range(5)]
    top, bot = ys[0] - 14, ys[-1] + 14
    X0, X1 = 200, 958
    BAR = 600
    # bracket + system barlines
    d.add(f'<path d="M187 {top-10} V{bot+10}" stroke="{P.ink}" stroke-width="4.5"/>')
    d.add(f'<path d="M185 {top-10} q10 -1 15 -9" stroke="{P.ink}" stroke-width="2.2" stroke-linecap="round"/>')
    d.add(f'<path d="M185 {bot+10} q10 1 15 9" stroke="{P.ink}" stroke-width="2.2" stroke-linecap="round"/>')
    d.add(f'<line x1="{X0}" y1="{top}" x2="{X0}" y2="{bot}" stroke="{P.ink2}" stroke-width="1.2"/>')
    d.add(f'<line x1="{BAR}" y1="{top}" x2="{BAR}" y2="{bot}" stroke="{P.faint}" stroke-width="1.1"/>')
    d.add(f'<line x1="{X1-8}" y1="{top}" x2="{X1-8}" y2="{bot}" stroke="{P.ink2}" stroke-width="1.2"/>')
    d.add(f'<line x1="{X1-1.8}" y1="{top}" x2="{X1-1.8}" y2="{bot}" stroke="{P.ink}" stroke-width="4"/>')
    PX0, PX1, S0, S1 = 236, X1 - 12, 0.6, 11.4
    notes_all = []
    for r, (name, sub, dyn, items, contour) in enumerate(ROWS):
        y = ys[r]
        for k in range(5):
            d.add(f'<line x1="{X0}" y1="{y+(k-2)*7}" x2="{X1}" y2="{y+(k-2)*7}" stroke="{P.line2}"/>')
        d.add(d.text(168, y + 4, name, "serif-i", 20, P.ink, anchor="end"))
        d.add(d.text(168, y + 21, sub, "mono", 8.5, P.muted, weight=500, ls=1, anchor="end"))
        d.add(d.text(214, y - .5, "4", "serif", 20.5, P.ink2))
        d.add(d.text(214, y + 13.5, "4", "serif", 20.5, P.ink2))
        d.add(d.text(234, y + 37, dyn, "serif-i", 15, P.muted))
        n = len(items)
        n1 = (n + 1) // 2
        n2 = n - n1
        xs = [252 + (k + .5) * (BAR - 14 - 252) / n1 for k in range(n1)] + \
             [BAR + 14 + (k + .5) * (X1 - 22 - BAR - 14) / n2 for k in range(n2)]
        nys = [y - c * 3.5 for c in contour]
        for grp in (range(0, n1), range(n1, n)):
            g = list(grp)
            if len(g) < 2:
                continue
            xa, xb = xs[g[0]], xs[g[-1]]
            ya, yb = nys[g[0]] - 19, nys[g[-1]] - 19
            peak = max(min(min(nys[i] for i in g) - 33, ya - 10, yb - 10), y - 44)
            d.add(f'<path d="M{xa:.1f} {ya:.1f} Q{(xa+xb)/2:.1f} {2*peak-(ya+yb)/2:.1f} {xb:.1f} {yb:.1f}" '
                  f'stroke="{P.muted}" stroke-width="1.1" stroke-linecap="round" opacity=".8"/>')
        for k, ((slug, label), x, ny) in enumerate(zip(items, xs, nys)):
            tp = S0 + (x - PX0) / (PX1 - PX0) * (S1 - S0)
            notes_all.append((x, ny, slug, label, tp, y))
    for (x, ny, slug, label, tp, y) in notes_all:
        ck = [(0, P.ink2), (tp - .02, P.ink2), (tp + .05, P.red), (tp + .9, P.red), (tp + 1.8, P.ink2)]
        fk = [(0, 0), (tp - .02, 0), (tp + .05, .16), (tp + 1.8, 0)]
        d.add(f'<circle cx="{x:.1f}" cy="{ny:.1f}" r="15.5" fill="{P.bg}" stroke="{P.ink2}" stroke-width="1.3">'
              + anim("stroke", ck, T) + "</circle>")
        d.add(f'<circle cx="{x:.1f}" cy="{ny:.1f}" r="15.5" fill="{P.red}" opacity="0">' + anim("opacity", fk, T)
              + "</circle>")
        s = 15 / 24
        d.add(f'<path d="{ICONS[slug]}" fill="{P.ink2}" transform="translate({x-7.5:.2f} {ny-7.5:.2f}) scale({s:.4f})">'
              + anim("fill", ck, T) + "</path>")
        d.add(d.text(x, y + 37, label, "mono", 9, P.muted, ls=.3, anchor="middle"))
    # playhead
    d.defs.append(f'<linearGradient id="ph" x1="0" x2="1"><stop offset="0" stop-color="{P.red}" stop-opacity="0"/>'
                  f'<stop offset="1" stop-color="{P.red}" stop-opacity="{.10 if P.name=="dark" else .07}"/></linearGradient>')
    xk = [(0, PX0), (S0, PX0), (S1, PX1), (T, PX1)]
    ok = [(0, 0), (S0, 0), (S0 + .3, 1), (S1, 1), (S1 + .6, 0)]
    d.add(f'<g opacity="0">' + anim("opacity", ok, T)
          + f'<rect x="{PX0-46}" y="{top-22}" width="46" height="{bot-top+44}" fill="url(#ph)">'
          + anim("x", [(t, v - 46) for t, v in xk], T) + "</rect>"
          + f'<line x1="{PX0}" y1="{top-22}" x2="{PX0}" y2="{bot+22}" stroke="{P.red}" stroke-width="1.6">'
          + anim("x1", xk, T) + anim("x2", xk, T) + "</line></g>")
    return d.render()


# =============================================================== V. coda: contact pills + fine
def contact_pill(theme, pos, label, value, icon):
    P = THEMES[theme]
    W, H = 333, 66
    d = Doc(W, H, f"{label}: {value}")
    x0 = {0: .5, 1: 4.5, 2: 8.5}[pos]
    w = 324
    d.defs.append(f'<clipPath id="pc"><rect x="{x0}" y=".5" width="{w}" height="{H-1}" rx="{(H-1)/2}"/></clipPath>')
    d.defs.append(f'<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{P.ink}" stop-opacity="0"/>'
                  f'<stop offset=".5" stop-color="{P.ink}" stop-opacity="{.07 if P.name=="dark" else .05}"/>'
                  f'<stop offset="1" stop-color="{P.ink}" stop-opacity="0"/></linearGradient>')
    d.add(f'<rect x="{x0}" y=".5" width="{w}" height="{H-1}" rx="{(H-1)/2}" fill="{P.bg}" stroke="{P.line2}"/>')
    T = 7.0
    st = 1.0 + pos * 0.5
    d.add(f'<g clip-path="url(#pc)"><rect x="-140" y="0" width="120" height="{H}" fill="url(#sh)" '
          f'transform="skewX(-20)">' + anim("x", [(0, -140), (st, -140), (st + 1.4, W + 60), (T, W + 60)], T, "spline",
                                            ".4 0 .6 1") + "</rect></g>")
    cx, cy = x0 + 33, H / 2
    d.add(f'<circle cx="{cx}" cy="{cy}" r="19" fill="{P.panel2}"/>')
    if icon == "globe":
        d.add(f'<circle cx="{cx}" cy="{cy}" r="8" stroke="{P.ink}" stroke-width="1.4"/>'
              f'<ellipse cx="{cx}" cy="{cy}" rx="3.6" ry="8" stroke="{P.ink}" stroke-width="1.3"/>'
              f'<line x1="{cx-8}" y1="{cy}" x2="{cx+8}" y2="{cy}" stroke="{P.ink}" stroke-width="1.3"/>')
    elif icon == "in":
        d.add(d.text(cx, cy + 4.6, "in", "sans", 14, P.ink, weight=700, anchor="middle", ls=-0.3))
    else:
        d.add(f'<rect x="{cx-8.5}" y="{cy-6}" width="17" height="12" rx="2" stroke="{P.ink}" stroke-width="1.4"/>'
              f'<path d="M{cx-8} {cy-5} l8 6 l8 -6" stroke="{P.ink}" stroke-width="1.4" stroke-linejoin="round"/>')
    d.add(d.text(x0 + 64, 28, label, "mono", 9, P.muted, weight=500, ls=1.4))
    d.add(d.text(x0 + 64, 47, value, "sans", 14.5, P.ink, weight=500, ls=-0.1))
    d.add(d.text(x0 + w - 24, 40, "↗", "sans", 17, P.red, anchor="end"))
    return d.render()


def fine(theme):
    P = THEMES[theme]
    W, H = 1000, 210
    T = 8.0
    d = Doc(W, H, "fine", "Fine. Köszönöm, hogy végighallgattad.")
    pt = (430, 92)
    d.defs.append(f'<linearGradient id="fs" x1="0" y1="0" x2="{pt[0]}" y2="0" gradientUnits="userSpaceOnUse">'
                  f'<stop offset="0" stop-color="{P.string}" stop-opacity="0"/>'
                  f'<stop offset=".45" stop-color="{P.string}"/><stop offset="1" stop-color="{P.red}"/></linearGradient>')
    ws = [0.8, 1.0, 1.2, 1.45, 1.7, 2.0]
    for i in range(6):
        y = 46 + i * 11
        p = f"M20 {y} L300 {y} C380 {y} 400 {pt[1]} {pt[0]} {pt[1]}"
        d.add(f'<path d="{p}" stroke="url(#fs)" stroke-width="{ws[i]}"/>')
        t0 = 0.8 + i * 0.12
        d.add(f'<path d="{p}" pathLength="1000" stroke="{P.red}" stroke-width="{ws[i]+.8}" stroke-linecap="round" '
              f'stroke-dasharray="50 1100" stroke-dashoffset="52" opacity="0">'
              + anim("stroke-dashoffset", [(0, 52), (t0, 52), (t0 + 1.3, -1000)], T, "spline", ".5 0 .9 .6")
              + anim("opacity", [(0, 0), (t0, 0), (t0 + .02, 1), (t0 + 1.25, 1), (t0 + 1.3, 0)], T) + "</path>")
    ta = 0.8 + 5 * 0.12 + 1.3
    d.add(f'<circle cx="{pt[0]}" cy="{pt[1]}" r="4" stroke="{P.red}" stroke-width="1.2" opacity="0">'
          + anim("r", [(0, 4), (ta - .6, 4), (ta + .9, 26)], T, "spline", ".2 .6 .4 1")
          + anim("opacity", [(0, 0), (ta - .62, 0), (ta - .6, .8), (ta + .9, 0)], T) + "</circle>")
    d.add(f'<circle cx="{pt[0]}" cy="{pt[1]}" r="4" fill="{P.red}"/>')
    # fermata above the point
    d.add(f'<path d="M{pt[0]-13} {pt[1]-16} A13 12 0 0 1 {pt[0]+13} {pt[1]-16}" stroke="{P.ink2}" stroke-width="1.6"/>'
          f'<circle cx="{pt[0]}" cy="{pt[1]-19}" r="1.8" fill="{P.ink2}"/>')
    d.add(d.text(pt[0] + 22, pt[1] + 17, "fine", "serif-i", 58, P.ink, ls=-0.5))
    fx = pt[0] + 22 + tw("fine", "serif-i", 58, ls=-0.5) + 4
    d.css.append(".dot{animation:rec 2.6s ease-in-out infinite}@keyframes rec{0%,100%{opacity:1}50%{opacity:.28}}")
    d.add(f'<circle class="dot" cx="{fx:.1f}" cy="{pt[1]+13}" r="4.4" fill="{P.red}"/>')
    d.add(d.text(500, 168, "Köszönöm, hogy végighallgattad.", "serif-i", 19, P.ink2, anchor="middle"))
    d.add(d.text(500, 194, "JÓNÁS GERGELY · BUDAPEST · 2026", "mono", 9.5, P.muted, weight=500, ls=1.8,
                 anchor="middle"))
    return d.render()

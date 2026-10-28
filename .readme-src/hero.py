from lib import *

# Hungarian (Helmholtz) string names, top (thinnest) -> bottom, like guitar tablature
STRINGS = [("e", "¹", "329.63"), ("h", "", "246.94"), ("g", "", "196.00"),
           ("d", "", "146.83"), ("A", "", "110.00"), ("E", "", "82.41")]
WIDTHS = [0.9, 1.1, 1.35, 1.6, 1.95, 2.35]
AMPS = [4.6, 5.1, 5.7, 6.3, 7.0, 7.7]


def hero(theme):
    P = THEMES[theme]
    W, H = 1000, 520
    T = 10.0
    d = Doc(W, H, "Jónás Gergely",
            "Jónás Gergely: mérnökinformatikus (BME), a VibeSite alapítója. Hat animált gitárhúr, "
            "amely egyetlen rendszerbe fut össze.")
    NUT, BR = 108, 868
    MID = (NUT + BR) / 2
    ys = [352 + 17 * i for i in range(6)]
    cy = (ys[0] + ys[-1]) / 2
    NODE = (956, cy)

    d.defs.append(f'<clipPath id="cl"><rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22"/></clipPath>')
    d.defs.append(
        f'<radialGradient id="gl" cx="{NODE[0]}" cy="{NODE[1]}" r="460" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{P.red}" stop-opacity="{P.glow}"/>'
        f'<stop offset=".55" stop-color="{P.red}" stop-opacity="{P.glow*0.25:.3f}"/>'
        f'<stop offset="1" stop-color="{P.red}" stop-opacity="0"/></radialGradient>')
    d.defs.append(
        f'<radialGradient id="gl2" cx="60" cy="40" r="520" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{P.ink}" stop-opacity="{0.045 if P.name=="dark" else 0.0}"/>'
        f'<stop offset="1" stop-color="{P.ink}" stop-opacity="0"/></radialGradient>')
    d.defs.append(
        f'<linearGradient id="cv" x1="{BR}" y1="0" x2="{NODE[0]}" y2="0" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{P.string}"/><stop offset="1" stop-color="{P.red}"/></linearGradient>')
    d.css.append(".dot{animation:rec 2.6s ease-in-out infinite}"
                 "@keyframes rec{0%,100%{opacity:1}50%{opacity:.28}}")

    # frame
    d.add(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="22" fill="{P.bg}" stroke="{P.line}"/>')
    d.add('<g clip-path="url(#cl)">',
          f'<rect width="{W}" height="{H}" fill="url(#gl2)"/>',
          f'<rect width="{W}" height="{H}" fill="url(#gl)"/>', '</g>')

    # ---- meta row
    d.add(f'<circle cx="44" cy="42.5" r="3" fill="{P.red}"/>')
    d.add(d.text(56, 46, "", "mono", 10.5, P.ink2, weight=500, ls=1.6, inner=[
        ("mono", "BUDAPEST, HU", ""), ("mono", "47.4979° N · 19.0402° E", f'fill="{P.muted}" dx="14"')]))
    d.add(d.text(960, 46, "MÉRNÖKINFORMATIKUS · BME VIK · AI/ML", "mono", 10.5, P.muted, weight=500, ls=1.6,
                 anchor="end"))

    # ---- name
    d.add(d.text(34, 178, "Jónás", "serif", 132, P.ink, ls=-1.5))
    gx = 98
    d.add(d.text(gx, 292, "Gergely", "serif-i", 132, P.ink, ls=-1.5))
    dotx = gx + tw("Gergely", "serif-i", 132, ls=-1.5) + 4
    d.add(f'<circle class="dot" cx="{f2(dotx)}" cy="283.5" r="8.5" fill="{P.red}"/>')

    # ---- right column
    rows = [("FOUNDER & CEO", "VibeSite · GVNETWORK AC Kft."),
            ("FEJLESZTÉSI VEZETŐ", "AI és gépi látás rendszerek"),
            ("KUTATÁS · BSc", "Klinikai LLM-ágensek"),
            ("KLASSZIKUS GITÁR", "10+ éve, hat húron")]
    cx0 = 612
    d.add(f'<line x1="{cx0-26}" y1="104" x2="{cx0-26}" y2="288" stroke="{P.line2}"/>')
    for i, (lab, val) in enumerate(rows):
        y = 120 + i * 47
        d.add(d.text(cx0, y, f"0{i+1}", "mono", 10, P.red, weight=500, ls=1))
        d.add(d.text(cx0 + 30, y, lab, "mono", 10, P.muted, weight=500, ls=1.5))
        d.add(d.text(cx0 + 30, y + 23, val, "sans", 18, P.ink, weight=500, ls=-0.2))

    # ---- fretboard
    L = 1100
    for n in range(1, 20):
        x = NUT + L * (1 - 2 ** (-n / 12))
        sw = 1.6 if n == 12 else 1.1
        d.add(f'<line x1="{x:.1f}" y1="342" x2="{x:.1f}" y2="447" stroke="{P.fret}" stroke-width="{sw}"/>')
    roman = {3: "III", 5: "V", 7: "VII", 9: "IX", 12: "XII", 15: "XV", 17: "XVII", 19: "XIX"}
    for n, r in roman.items():
        x0 = NUT + L * (1 - 2 ** (-(n - 1) / 12))
        x1 = NUT + L * (1 - 2 ** (-n / 12))
        d.add(d.text((x0 + x1) / 2, 468, r, "serif", 12, P.faint, anchor="middle"))
    d.add(f'<rect x="{NUT-4}" y="340" width="4.5" height="109" rx="1.2" fill="{P.ink2}" opacity=".5"/>')

    # string labels
    for i, (nm, sup, hz) in enumerate(STRINGS):
        y = ys[i]
        if sup:
            d.add(d.text(40, y + 5, "", "serif-i", 17, P.ink2, inner=[
                ("serif-i", nm, ""), ("serif-i", "1", 'font-size="10" dy="-6.5"')]))
        else:
            d.add(d.text(40, y + 5, nm, "serif-i", 17, P.ink2))
        d.add(d.text(58, y + 3.5, hz, "mono", 8.5, P.faint, ls=0.3))

    # events: arpeggio up (bass->treble), then a quick strum down
    events = []
    for k, s in enumerate([5, 4, 3, 2, 1, 0]):
        events.append((s, 0.5 + k * 0.27, 1.0))
    for k, s in enumerate([5, 4, 3, 2, 1, 0]):
        events.append((s, 5.4 + k * 0.045, 0.8))
    HP, NH, DEC, VIB = 0.085, 24, 0.87, 2.4

    for i, y in enumerate(ys):
        w, A = WIDTHS[i], AMPS[i]
        evs = [(t, a) for s, t, a in events if s == i]
        dk, ck, gk, lk, lo = [], [], [], [], []
        for t0, sc in evs:
            a0 = A * sc
            dk.append((t0, 0.0))
            dk.append((t0 + 0.035, a0))
            for k in range(1, NH):
                dk.append((t0 + 0.035 + k * HP, a0 * ((-DEC) ** k)))
            dk.append((t0 + 0.035 + NH * HP, 0.0))
            ck += [(t0, P.string), (t0 + 0.04, P.red), (t0 + 0.7, P.red), (t0 + 1.9, P.string)]
            gk += [(t0, 0), (t0 + 0.04, 0.38), (t0 + 1.2, 0.12), (t0 + VIB, 0)]
            for j, (dt, f, op) in enumerate([(0, 0, 0), (0.04, 1, .16), (0.4, .6, .1), (0.9, .32, .055),
                                              (1.5, .13, .02), (VIB, 0, 0)]):
                lk.append((t0 + dt, f * a0))
                lo.append((t0 + dt, op))
        dvals = [(t, f"M{NUT} {y} Q{MID} {y + 2*v:.2f} {BR} {y}") for t, v in dk]
        lvals = [(t, f"M{NUT} {y} Q{MID} {y - 2*v:.2f} {BR} {y} Q{MID} {y + 2*v:.2f} {NUT} {y}Z") for t, v in lk]
        rest = f"M{NUT} {y} Q{MID} {y} {BR} {y}"
        # envelope (motion blur lens)
        d.add(f'<path d="{rest}" fill="{P.red}" opacity="0">' + anim("d", lvals, T) + anim("opacity", lo, T) + "</path>")
        # glow copy
        d.add(f'<path d="{rest}" stroke="{P.red}" stroke-width="{w+5}" stroke-linecap="round" opacity="0">'
              + anim("d", dvals, T, "spline") + anim("opacity", gk, T) + "</path>")
        # the string
        d.add(f'<path d="{rest}" stroke="{P.string}" stroke-width="{w}">'
              + anim("d", dvals, T, "spline") + anim("stroke", ck, T) + "</path>")
        # converging tail into the node
        d.add(f'<path d="M{BR} {y} C{BR+44} {y} {BR+52} {cy} {NODE[0]} {cy}" stroke="url(#cv)" '
              f'stroke-width="{max(w*0.8, 0.8):.2f}" opacity=".9"/>')

    # signal pulses travelling into the node, and rings when they land
    for idx, (s, t0, sc) in enumerate(events):
        y = ys[s]
        path = f"M{NUT} {y} L{BR} {y} C{BR+44} {y} {BR+52} {cy} {NODE[0]} {cy}"
        ts, te = t0 + 0.5, t0 + 1.55
        dash = 64
        offs = [(0, dash + 2), (ts, dash + 2), (te, -1000), (te + 0.01, dash + 2)]
        ops = [(0, 0), (ts, 0), (ts + 0.02, 1), (te - 0.05, 1), (te, 0)]
        d.add(f'<path d="{path}" pathLength="1000" stroke="{P.red}" stroke-width="{WIDTHS[s]+0.9:.2f}" '
              f'stroke-linecap="round" stroke-dasharray="{dash} 1200" stroke-dashoffset="{dash+2}" opacity="0">'
              + anim("stroke-dashoffset", offs, T, "spline", ".5 0 .9 .6") + anim("opacity", ops, T) + "</path>")
        if sc == 1.0 or s == 0:
            rk = [(0, 5), (te, 5), (te + 1.0, 30 if sc < 1 else 22)]
            rop = [(0, 0), (te - 0.01, 0), (te, 0.75), (te + 1.0, 0)]
            d.add(f'<circle cx="{NODE[0]}" cy="{cy}" r="5" stroke="{P.red}" stroke-width="1.2" opacity="0">'
                  + anim("r", rk, T, "spline", ".2 .6 .4 1") + anim("opacity", rop, T) + "</circle>")
    d.add(f'<circle cx="{NODE[0]}" cy="{cy}" r="11" fill="{P.red}" opacity=".16"/>')
    d.add(f'<circle cx="{NODE[0]}" cy="{cy}" r="4.6" fill="{P.red}"/>')

    # ---- bottom captions
    d.add(d.text(40, 500, "", "mono", 9.5, P.faint, ls=0.8, inner=[
        ("mono", "ÉRINTŐK", ""), ("mono", "x", 'dx="12"'), ("mono", "n", 'font-size="7" dy="3"'),
        ("mono", " = L · (1 − 2", 'dy="-3"'), ("mono", "−n/12", 'font-size="7" dy="-4"'),
        ("mono", ")", 'dy="4"')]))
    d.add(d.text(960, 500, "", "mono", 9.5, P.faint, ls=0.8, anchor="end", inner=[
        ("mono", "HANGOLÁS", ""), ("mono", "E · A · d · g · h · e", 'dx="12"'), ("mono", "1", 'font-size="7" dy="-4"'),
        ("mono", "·", 'dy="4" dx="10"'), ("mono", "a", 'dx="10"'), ("mono", "1", 'font-size="7" dy="-4"'), ("mono", " = 440 Hz", 'dy="4"')]))
    return d.render()

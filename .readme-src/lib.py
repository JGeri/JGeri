"""Shared helpers: palettes, font measuring/subsetting, SVG document builder, SMIL helpers."""
import base64, io, html, math, os
from functools import lru_cache
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options
from fontTools.varLib import instancer

FONTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts") + os.sep
FONTFILES = {
    "serif": FONTDIR + "InstrumentSerif-Regular.ttf",
    "serif-i": FONTDIR + "InstrumentSerif-Italic.ttf",
    "sans": FONTDIR + "Geist[wght].ttf",
    "mono": FONTDIR + "GeistMono[wght].ttf",
}
FAMILY = {  # css family / style per logical font
    "serif": ("JGSerif", "normal", "Georgia,'Times New Roman',serif"),
    "serif-i": ("JGSerif", "italic", "Georgia,'Times New Roman',serif"),
    "sans": ("JGSans", "normal", "system-ui,-apple-system,'Segoe UI',sans-serif"),
    "mono": ("JGMono", "normal", "ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace"),
}
CLS = {"serif": "s", "serif-i": "si", "sans": "g", "mono": "m"}


class P:
    def __init__(self, **kw):
        self.__dict__.update(kw)


THEMES = {
    "dark": P(
        name="dark", bg="#0B0B0D", panel="#111115", panel2="#17171C", line="#212127", line2="#2E2E36",
        ink="#F3F1EC", ink2="#CFCBC4", muted="#8E8B86", faint="#5C5B62", red="#FF2A2A", red2="#FF6A5C",
        string="#4B4B54", fret="#24242A", glow=0.20, card_shadow=0.0,
    ),
    "light": P(
        name="light", bg="#F7F4ED", panel="#FFFDF8", panel2="#EEEAE0", line="#E2DDD1", line2="#CFC8BA",
        ink="#151413", ink2="#3B3A37", muted="#6E6A62", faint="#A29C90", red="#E0191B", red2="#F0473F",
        string="#A49F94", fret="#DCD6CA", glow=0.11, card_shadow=0.0,
    ),
}


# ---------------------------------------------------------------- fonts
@lru_cache(maxsize=None)
def _metrics(font, weight):
    f = TTFont(FONTFILES[font])
    if "fvar" in f:
        f = instancer.instantiateVariableFont(f, {"wght": weight})
    cmap = f.getBestCmap()
    hmtx = f["hmtx"].metrics
    upm = f["head"].unitsPerEm
    return cmap, hmtx, upm


def tw(txt, font="sans", size=14, weight=400, ls=0.0):
    cmap, hmtx, upm = _metrics(font, weight)
    tot = 0
    for c in txt:
        g = cmap.get(ord(c)) or cmap[ord("?")]
        tot += hmtx[g][0]
    return tot * size / upm + ls * len(txt)


def wrap(txt, width, font="sans", size=14, weight=400, ls=0.0):
    words, lines, cur = txt.split(" "), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, font, size, weight, ls) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


@lru_cache(maxsize=None)
def subset_b64(font, chars):
    f = TTFont(FONTFILES[font])
    o = Options()
    o.flavor = "woff2"
    o.layout_features = ["kern", "liga", "calt", "ccmp", "locl", "mark", "mkmk", "tnum"]
    o.hinting = False
    o.desubroutinize = True
    o.name_IDs = [1, 2]
    o.notdef_outline = True
    s = Subsetter(o)
    s.populate(unicodes=sorted({ord(c) for c in chars} | {32}))
    s.subset(f)
    f.flavor = "woff2"
    b = io.BytesIO()
    f.save(b)
    return base64.b64encode(b.getvalue()).decode()


def esc(s):
    return html.escape(s, quote=False)


def f2(v):
    if isinstance(v, float):
        s = f"{v:.2f}".rstrip("0").rstrip(".")
        return s if s not in ("-0", "") else "0"
    return str(v)


# ---------------------------------------------------------------- doc
class Doc:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.parts, self.defs, self.css = [], [], []
        self.chars = {k: set() for k in FONTFILES}

    def use(self, font, txt):
        self.chars[font] |= set(txt)

    def add(self, *xs):
        self.parts.extend(xs)

    def text(self, x, y, txt, font="sans", size=14, fill="#000", weight=None, ls=None, anchor=None,
             opacity=None, extra="", inner=None):
        """inner: list of (font, txt, attrs) tspans; if given, txt is ignored."""
        a = [f'x="{f2(x)}"', f'y="{f2(y)}"', f'class="{CLS[font]}"', f'font-size="{f2(size)}"', f'fill="{fill}"']
        if weight:
            a.append(f'font-weight="{weight}"')
        if ls:
            a.append(f'letter-spacing="{f2(ls)}"')
        if anchor:
            a.append(f'text-anchor="{anchor}"')
        if opacity is not None:
            a.append(f'opacity="{f2(opacity)}"')
        if extra:
            a.append(extra)
        if inner:
            body = ""
            for fnt, t, attrs in inner:
                self.use(fnt, t)
                body += f'<tspan class="{CLS[fnt]}" {attrs}>{esc(t)}</tspan>'
        else:
            self.use(font, txt)
            body = esc(txt)
        return f'<text {" ".join(a)}>{body}</text>'

    def render(self):
        faces = []
        for font, chars in self.chars.items():
            if not chars:
                continue
            fam, style, _ = FAMILY[font]
            w = ";font-weight:100 900" if font in ("sans", "mono") else ""
            faces.append(
                f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{subset_b64(font, frozenset(chars))}) "
                f"format('woff2');font-style:{style}{w}}}"
            )
        cls = []
        for font, c in CLS.items():
            fam, style, fb = FAMILY[font]
            cls.append(f".{c}{{font-family:'{fam}',{fb};font-style:{style}}}")
        style = "\n".join(faces + cls + self.css + [
            "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
        ])
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
            f'role="img" aria-labelledby="t d" fill="none">',
            f'<title id="t">{esc(self.title)}</title><desc id="d">{esc(self.desc or self.title)}</desc>',
            f"<style>\n{style}\n</style>",
            "<defs>" + "".join(self.defs) + "</defs>",
        ]
        out += self.parts
        out.append("</svg>")
        return "\n".join(out)


# ---------------------------------------------------------------- SMIL
def _norm(keys, T):
    keys = sorted(keys, key=lambda k: k[0])
    if keys[0][0] > 0:
        keys = [(0.0, keys[0][1])] + keys
    if keys[-1][0] < T:
        keys = keys + [(T, keys[-1][1])]
    # strictly increasing keyTimes after rounding
    out, last = [], -1.0
    for t, v in keys:
        kt = round(t / T, 4)
        if kt <= last:
            kt = round(last + 0.0001, 4)
        kt = min(kt, 1.0)
        if out and kt <= last:
            continue
        out.append((kt, v))
        last = kt
    out[-1] = (1.0, out[-1][1])
    out[0] = (0.0, out[0][1])
    return out


def anim(attr, keys, T, calc="linear", spline=None, extra=""):
    ks = _norm(keys, T)
    kt = ";".join(f"{k:.4f}".rstrip("0").rstrip(".") if k not in (0.0, 1.0) else str(int(k)) for k, _ in ks)
    vals = ";".join(f2(v) if not isinstance(v, str) else v for _, v in ks)
    s = f'<animate attributeName="{attr}" dur="{f2(T)}s" repeatCount="indefinite" values="{vals}" keyTimes="{kt}"'
    if calc == "spline":
        s += f' calcMode="spline" keySplines="{";".join([spline or ".45 0 .55 1"] * (len(ks) - 1))}"'
    elif calc != "linear":
        s += f' calcMode="{calc}"'
    return s + f" {extra}/>"


def anim_tf(kind, keys, T, calc="linear", spline=None, extra=""):
    ks = _norm(keys, T)
    kt = ";".join(f"{k:.4f}".rstrip("0").rstrip(".") if k not in (0.0, 1.0) else str(int(k)) for k, _ in ks)
    vals = ";".join(v for _, v in ks)
    s = (f'<animateTransform attributeName="transform" type="{kind}" dur="{f2(T)}s" repeatCount="indefinite" '
         f'values="{vals}" keyTimes="{kt}"')
    if calc == "spline":
        s += f' calcMode="spline" keySplines="{";".join([spline or ".45 0 .55 1"] * (len(ks) - 1))}"'
    elif calc != "linear":
        s += f' calcMode="{calc}"'
    return s + f" {extra}/>"


def pill(d, x, y, txt, P, font="mono", size=10.5, weight=500, ls=0.6, h=24, padx=11, stroke=None, fill=None,
         color=None, r=None):
    w = tw(txt, font, size, weight, ls) + 2 * padx
    r = h / 2 if r is None else r
    d.add(f'<rect x="{f2(x)}" y="{f2(y)}" width="{f2(w)}" height="{h}" rx="{f2(r)}" '
          f'fill="{fill or "none"}" stroke="{stroke or P.line2}"/>')
    d.add(d.text(x + padx, y + h / 2 + size * 0.36, txt, font, size, color or P.ink2, weight=weight, ls=ls))
    return w

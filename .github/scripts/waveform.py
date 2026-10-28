#!/usr/bin/env python3
"""
Hullámforma — a GitHub-hozzájárulásokat hangfájl-hullámformaként rajzolja ki.

Kimenet: assets/waveform-dark.svg és assets/waveform-light.svg
Futtatás:  GITHUB_TOKEN=... GH_LOGIN=JGeri python .github/scripts/waveform.py
           python .github/scripts/waveform.py --demo        (mintaadat, helyi előnézethez)
           python .github/scripts/waveform.py --placeholder (üres állapot)

Csak a Python standard könyvtárát használja, így a GitHub Actions futtatón nincs mit telepíteni.
"""
import base64
import datetime as dt
import json
import math
import os
import random
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "assets"
LOGIN = os.environ.get("GH_LOGIN", "JGeri")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

THEMES = {
    "dark": dict(bg="#0B0B0D", panel2="#17171C", line="#212127", line2="#2E2E36", ink="#F3F1EC",
                 ink2="#CFCBC4", muted="#8E8B86", faint="#5C5B62", red="#FF2A2A", wave="#34343C"),
    "light": dict(bg="#F7F4ED", panel2="#EEEAE0", line="#E2DDD1", line2="#CFC8BA", ink="#151413",
                  ink2="#3B3A37", muted="#6E6A62", faint="#A29C90", red="#E0191B", wave="#D3CDC1"),
}
MONTHS = ["JAN", "FEB", "MÁR", "ÁPR", "MÁJ", "JÚN", "JÚL", "AUG", "SZE", "OKT", "NOV", "DEC"]


# ------------------------------------------------------------------ data
def fetch_graphql():
    q = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
           totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json",
                 "User-Agent": "hullamforma"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(data["errors"])
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]


def fetch_html():
    """Tartalék: a nyilvános kontribúciós naptár HTML-je (token nélkül is működik)."""
    req = urllib.request.Request(f"https://github.com/users/{LOGIN}/contributions",
                                 headers={"User-Agent": "hullamforma"})
    with urllib.request.urlopen(req, timeout=30) as r:
        h = r.read().decode("utf-8", "replace")
    cells = {}
    for m in re.finditer(r"<td[^>]*?data-date=\"(\d{4}-\d\d-\d\d)\"[^>]*?>", h):
        tag = m.group(0)
        i = re.search(r'id="([^"]+)"', tag)
        lv = re.search(r'data-level="(\d)"', tag)
        cells[i.group(1) if i else m.group(1)] = (m.group(1), int(lv.group(1)) if lv else 0)
    counts = {}
    for m in re.finditer(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', h):
        n = re.match(r"\s*(\d[\d,]*)\s+contribution", m.group(2))
        counts[m.group(1)] = int(n.group(1).replace(",", "")) if n else 0
    out = [(date, counts.get(cid, lvl)) for cid, (date, lvl) in cells.items()]
    return sorted(out)


def demo_data():
    rnd = random.Random(42)
    end = dt.date.today()
    days = []
    for i in range(370, -1, -1):
        d = end - dt.timedelta(days=i)
        base = 2.2 + 1.6 * math.sin(i / 23.0) + (1.5 if d.weekday() < 5 else -1.2)
        c = max(0, int(rnd.gauss(base, 2.4))) if rnd.random() > 0.18 else 0
        if rnd.random() < 0.03:
            c += rnd.randint(8, 22)
        days.append((d.isoformat(), c))
    return days


# ------------------------------------------------------------------ stats
def stats(days):
    counts = [c for _, c in days]
    total = sum(counts)
    longest = cur = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # ma még nincs commit: tegnaptól számolunk
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    best_i = max(range(len(counts)), key=lambda k: counts[k]) if counts else 0
    return dict(total=total, longest=longest, current=cur,
                best=counts[best_i] if counts else 0, best_date=days[best_i][0] if days else "",
                active=sum(1 for c in counts if c > 0))


# ------------------------------------------------------------------ svg
def font_face(fam, file, style="normal"):
    b = base64.b64encode((HERE / "fonts" / file).read_bytes()).decode()
    return (f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');"
            f"font-style:{style};font-weight:100 900}}")


def fmt(n):
    return f"{n:,}".replace(",", " ")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(days, theme, mode="live"):
    P = THEMES[theme]
    W, H = 1000, 330
    T = 16.0
    X0, X1, CY, AMP = 40, 960, 192, 50
    s = stats(days) if days else None
    parts = []
    a = parts.append
    a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="20" fill="{P["bg"]}" stroke="{P["line"]}"/>')

    def text(x, y, t, cls, size, fill, extra=""):
        a(f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" {extra}>{esc(t)}</text>')

    if s and s["total"] > 0:
        bd = s["best_date"].replace("-", ".")
        cols = [(fmt(s["total"]), "HOZZÁJÁRULÁS · 12 HÓNAP"), (str(s["longest"]), "LEGHOSSZABB SOROZAT · NAP"),
                (str(s["current"]), "JELENLEGI SOROZAT · NAP"), (str(s["best"]), f"CSÚCSNAP · {bd}")]
        for i, (v, lab) in enumerate(cols):
            x = 40 + i * 232
            text(x, 84, v, "s", 44, P["ink"], 'letter-spacing="-.5"')
            text(x, 106, lab, "m", 9.5, P["muted"], 'letter-spacing="1.3" font-weight="500"')
        n = len(days)
        step = (X1 - X0) / n
        bw = max(1.0, step * 0.6)
        mx = max(c for _, c in days) or 1
        base, hot = [], []
        for i, (_, c) in enumerate(days):
            h = 1.1 if c == 0 else max(2.2, math.sqrt(c / mx) * AMP)
            x = X0 + i * step + (step - bw) / 2
            r = f'<rect x="{x:.2f}" y="{CY-h:.2f}" width="{bw:.2f}" height="{2*h:.2f}" rx="{bw/2:.2f}"/>'
            base.append(r)
        bars = "".join(base)
        a(f'<line x1="{X0}" y1="{CY}" x2="{X1}" y2="{CY}" stroke="{P["line"]}"/>')
        a(f'<g fill="{P["wave"]}">{bars}</g>')
        # played part: same bars in red, revealed by an animated clip (the playhead)
        S0, S1 = 0.6, 12.6
        kt = f"0;{S0/T:.4f};{S1/T:.4f};{(S1+2.2)/T:.4f};{(S1+2.6)/T:.4f};1"
        a(f'<clipPath id="pl"><rect x="{X0}" y="0" width="0" height="{H}">'
          f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" '
          f'values="0;0;{X1-X0};{X1-X0};{X1-X0};0"/></rect></clipPath>')
        a(f'<g clip-path="url(#pl)"><g fill="{P["red"]}">{bars}'
          f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" '
          f'values="1;1;1;1;0;0"/></g></g>')
        a(f'<g><line x1="{X0}" y1="{CY-AMP-14}" x2="{X0}" y2="{CY+AMP+14}" stroke="{P["red"]}" stroke-width="1.5"/>'
          f'<circle cx="{X0}" cy="{CY-AMP-14}" r="3.2" fill="{P["red"]}"/>'
          f'<animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" '
          f'keyTimes="{kt}" values="0 0;0 0;{X1-X0} 0;{X1-X0} 0;{X1-X0} 0;0 0"/>'
          f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" '
          f'values="0;1;1;1;0;0"/></g>')
        # month ticks
        seen = set()
        for i, (ds, _) in enumerate(days):
            d = dt.date.fromisoformat(ds)
            key = (d.year, d.month)
            if d.day == 1 or (i == 0 and d.day < 8):
                if key in seen:
                    continue
                seen.add(key)
                x = X0 + i * step
                if x > X1 - 24:
                    continue
                a(f'<line x1="{x:.1f}" y1="{CY+AMP+16}" x2="{x:.1f}" y2="{CY+AMP+22}" stroke="{P["line2"]}"/>')
                text(f"{x+4:.1f}", CY + AMP + 33, MONTHS[d.month - 1], "m", 9, P["faint"], 'letter-spacing="1"')
    else:
        a(f'<line x1="{X0}" y1="{CY}" x2="{X1}" y2="{CY}" stroke="{P["line2"]}" stroke-dasharray="2 5"/>')
        text(40, 84, "—", "s", 44, P["ink"])
        text(40, 106, "MÉG NINCS ADAT", "m", 9.5, P["muted"], 'letter-spacing="1.3" font-weight="500"')
        text(500, CY - 14, "Az első GitHub Action-futás után itt szól majd az elmúlt év.", "si", 20,
             P["ink2"], 'text-anchor="middle"')

    a(f'<line x1="40" y1="290.5" x2="960" y2="290.5" stroke="{P["line"]}"/>')
    today = dt.date.today().strftime("%Y.%m.%d")
    text(40, 314, f"FRISSÍTVE {today} · GITHUB ACTIONS, NAPONTA", "m", 9.5, P["muted"],
         'letter-spacing="1.3" font-weight="500"')
    text(960, 314, "▶  1 SÁV = 1 NAP · AMPLITÚDÓ = √HOZZÁJÁRULÁS", "m", 9.5, P["muted"],
         'letter-spacing="1.3" font-weight="500" text-anchor="end"')
    if mode == "demo":
        a(f'<rect x="846" y="30" width="114" height="22" rx="11" stroke="{P["red"]}"/>')
        text(903, 44.5, "DEMÓ ADAT", "m", 9.5, P["red"], 'letter-spacing="1.4" font-weight="600" text-anchor="middle"')

    css = "\n".join([
        font_face("JGSerif", "InstrumentSerif-Regular.woff2"),
        font_face("JGSerif", "InstrumentSerif-Italic.woff2", "italic"),
        font_face("JGMono", "GeistMono.woff2"),
        ".s{font-family:'JGSerif',Georgia,serif}.si{font-family:'JGSerif',Georgia,serif;font-style:italic}"
        ".m{font-family:'JGMono',ui-monospace,Menlo,Consolas,monospace}",
    ])
    summary = (f"{s['total']} hozzájárulás az elmúlt évben, leghosszabb sorozat {s['longest']} nap"
               if s and s["total"] else "Még nincs adat")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-labelledby="t d" fill="none"><title id="t">Hullámforma: GitHub-hozzájárulások</title>'
            f'<desc id="d">{esc(summary)}</desc><style>{css}</style>' + "".join(parts) + "</svg>")


def main():
    mode = "live"
    if "--demo" in sys.argv:
        days, mode = demo_data(), "demo"
    elif "--placeholder" in sys.argv:
        days, mode = [], "placeholder"
    else:
        days = None
        if TOKEN:
            try:
                days = fetch_graphql()
            except Exception as e:  # noqa: BLE001
                print(f"GraphQL hiba, HTML-tartalékra váltok: {e}", file=sys.stderr)
        if not days:
            days = fetch_html()
        today = dt.date.today().isoformat()
        days = [d for d in days if d[0] <= today]
    OUT.mkdir(exist_ok=True)
    for theme in THEMES:
        (OUT / f"waveform-{theme}.svg").write_text(render(days, theme, mode), encoding="utf-8")
    if days:
        print(json.dumps(stats(days), ensure_ascii=False))


if __name__ == "__main__":
    main()

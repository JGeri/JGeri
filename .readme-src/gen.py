"""A profil README és az összes SVG újragenerálása.  Futtatás:  python .readme-src/gen.py"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hero import hero
from components import header, prelude, op_vibesite, op_cards, stack, contact_pill, fine

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = OUT + "/assets"
os.makedirs(A, exist_ok=True)
RAW = "https://raw.githubusercontent.com/JGeri/JGeri/HEAD/assets/"

HEADERS = {
    "h1": ("I.", "Prelúdium", "RÓLAM · MOST"),
    "h2": ("II.", "Opus", "VÁLOGATOTT MUNKÁK · 2024–2026"),
    "h3": ("III.", "Hangszerelés", "AMIVEL DOLGOZOM"),
    "h4": ("IV.", "Hullámforma", "AZ ELMÚLT ÉV · NAPONTA FRISSÜL"),
    "h5": ("V.", "Coda", "KAPCSOLAT"),
}
PILLS = [("portfolio", 0, "PORTFÓLIÓ", "jonasgergely.hu", "globe"),
         ("linkedin", 1, "LINKEDIN", "in/jonasgergely", "in"),
         ("email", 2, "E-MAIL", "jonas.gergely@gvnetwork.hu", "mail")]

sizes = {}
for t in ("dark", "light"):
    files = {"hero": hero(t), "prelude": prelude(t), "op1": op_vibesite(t), "stack": stack(t), "fine": fine(t)}
    for k, (n, ti, c) in HEADERS.items():
        files[k] = header(t, n, ti, c)
    files.update(op_cards(t))
    for slug, pos, lab, val, ic in PILLS:
        files[f"contact-{slug}"] = contact_pill(t, pos, lab, val, ic)
    for k, svg in files.items():
        p = f"{A}/{k}-{t}.svg"
        open(p, "w", encoding="utf-8").write(svg)
        sizes[os.path.basename(p)] = len(svg.encode())

# waveform: the GitHub Action owns these files; only create a placeholder if they are missing
wf = OUT + "/.github/scripts/waveform.py"
if not os.path.exists(f"{A}/waveform-dark.svg"):
    subprocess.run([sys.executable, wf, "--placeholder"], check=True)


def pic(name, alt, width="100%", href=None):
    img = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{RAW}{name}-dark.svg">'
           f'<source media="(prefers-color-scheme: light)" srcset="{RAW}{name}-light.svg">'
           f'<img alt="{alt}" src="{RAW}{name}-dark.svg" width="{width}"></picture>')
    return f'<a href="{href}">{img}</a>' if href else img


PORT = "https://jonasgergely.hu/"
readme = f"""<!--
  Jónás Gergely · GitHub profil
  Minden grafika kézzel épített, animált SVG az assets/ mappában (sötét és világos változat,
  a GitHub témájához igazodik). A Hullámforma kártyát a .github/workflows/waveform.yml frissíti naponta.
-->

<div align="center">

{pic("hero", "Jónás Gergely: mérnökinformatikus (BME), a VibeSite alapítója", href=PORT)}

<br>

{pic("h1", "I. Prelúdium")}
{pic("prelude", "A kódolás számomra olyan, mint a zeneszerzés: struktúrát, ritmust és hibátlan végrehajtást követel.")}

<br>

{pic("h2", "II. Opus")}
{pic("op1", "Op. 1: VibeSite, AI-alapú weboldal- és digitális jelenlét platform magyar KKV-knak", href="https://vibesite.hu/")}
{pic("op2", "Op. 2: Klinikai protokoll-ágens", "49.9%", href=PORT)}{pic("op3", "Op. 3: GPU-s LLM-kiszolgálás", "49.9%", href=PORT)}
{pic("op4", "Op. 4: Polcfigyelő gépi látás", "49.9%", href=PORT)}{pic("op5", "Op. 5: NECTAR TP, PwC AI Hackathon", "49.9%", href="https://github.com/snktibor/Nectar-TP-AI-Hackathon")}

<br>

{pic("h3", "III. Hangszerelés")}
{pic("stack", "Technológiák: Python, YOLOv8, Raspberry Pi, Claude, Gemini, FastAPI, Spring Boot, Go, Rust, React, Next.js, Astro, Tailwind, Svelte, Flutter, PostgreSQL, Redis, MongoDB, SQLite, Firebase, Linux, Docker, Kubernetes, NGINX, Cloudflare, GitHub Actions")}

<br>

{pic("h4", "IV. Hullámforma")}
{pic("waveform", "GitHub-hozzájárulások az elmúlt évben, hullámformaként")}

<br>

{pic("h5", "V. Coda")}
{pic("contact-portfolio", "Portfólió: jonasgergely.hu", "33.3%", href=PORT)}{pic("contact-linkedin", "LinkedIn", "33.3%", href="https://www.linkedin.com/in/jonasgergely")}{pic("contact-email", "E-mail: jonas.gergely@gvnetwork.hu", "33.3%", href="mailto:jonas.gergely@gvnetwork.hu")}

<br>

{pic("fine", "fine. Köszönöm, hogy végighallgattad.")}

</div>
"""
open(OUT + "/README.md", "w", encoding="utf-8").write(readme)

for k in sorted(sizes):
    print(f"{k:32s} {sizes[k]/1024:7.1f} KB")
print("total", round(sum(sizes.values()) / 1024), "KB")

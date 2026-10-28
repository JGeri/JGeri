# A profil README forrása

Minden grafika ebből a mappából generálódik (Python + fontTools, a fontok részhalmaza base64-ként kerül az SVG-kbe).

```bash
pip install fonttools brotli
python .readme-src/gen.py
```

- Szövegek: `hero.py` (fejléc, húrok), `components.py` (Prelúdium, Opus kártyák, partitúra, kapcsolat, fine)
- Színek: `lib.py` → `THEMES` (sötét és világos változat)
- A `waveform-*.svg` fájlokat a `.github/workflows/waveform.yml` frissíti naponta; a generátor ezekhez nem nyúl.
- Fontok: Instrument Serif, Geist, Geist Mono (SIL Open Font License 1.1). Ikonok: Simple Icons (CC0).

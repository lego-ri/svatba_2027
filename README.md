# 💒 Kačí & Ričí — Svatba 2027

Statický svatební web generovaný z YAML dat přes Jinja2 šablonu.

## Struktura projektu

```
svatba_2027/
├── build.py              # Python build skript
├── requirements.txt      # Python závislosti
├── data/
│   ├── wedding.yaml      # ← VEŠKERÝ OBSAH SE EDITUJE ZDE
│   └── schema.md         # Dokumentace datového schématu
├── templates/
│   └── index.html.j2     # Jinja2 HTML šablona
├── static/
│   ├── style.css          # CSS styly
│   └── main.js            # Minimální JavaScript
└── dist/                  # ← Vygenerovaný web (git-ignorován)
    ├── index.html
    ├── robots.txt
    └── svatba-kaci-rici-2027.ics
```

## Jak na to

### 1. Příprava prostředí

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. Build

```bash
python build.py
```

Výstup se vygeneruje do `dist/`. Otevřete `dist/index.html` v prohlížeči.

### 3. Automatický rebuild při úpravách

```bash
python build.py --watch
```

## Úprava obsahu

**Veškeré texty, časy, jména a odkazy** se editují v [`data/wedding.yaml`](data/wedding.yaml).
HTML šablonu a CSS **nemusíte měnit** pokud nechcete upravit rozložení/design.

## Fáze projektu

- [x] Phase 1: Datové schéma & informační architektura
- [ ] Phase 2: Vizuální design & šablona
- [ ] Phase 3: Build pipeline & optimalizace obrázků
- [ ] Phase 4: Doména, hosting & nasazení
- [ ] Phase 5: QR kód pro tištěné oznámení
- [ ] Phase 6: Emailová šablona & rozesílka
- [ ] Phase 7: Cross-device testování & launch

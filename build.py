#!/usr/bin/env python3
"""
build.py — Svatební web Kačí & Ričí
Načte data z YAML, vykreslí Jinja2 šablonu a vygeneruje statický HTML.

Použití:
    python build.py              # → dist/index.html
    python build.py --watch      # Sleduje změny a automaticky přestaví
"""

import argparse
import hashlib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

# ── Cesty ────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "wedding.yaml"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
DIST_DIR = ROOT / "dist"


def load_data() -> dict:
    """Načte a vrátí YAML data."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Přidej build metadata
    data["_build"] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "year": datetime.now().year,
    }
    return data


def generate_ics(data: dict, output_dir: Path) -> str:
    """Vygeneruje .ics soubor pro přidání do kalendáře. Vrací název souboru."""
    w = data["wedding"]
    couple = data["couple"]
    venue = data["venue"]

    dt_str = w["datetime"].replace("-", "").replace(":", "").replace("+", "")
    # Jednoduchý ICS — celodenní / s časem
    ics_content = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//KaciRici2027//Wedding//CS\r\n"
        "BEGIN:VEVENT\r\n"
        f"DTSTART;TZID=Europe/Prague:{w['date'].replace('-', '')}T{w['time'].replace(':', '')}00\r\n"
        f"DURATION:PT10H\r\n"
        f"SUMMARY:Svatba {couple['name_a']} & {couple['name_b']}\r\n"
        f"LOCATION:{venue['name']}\r\n"
        f"DESCRIPTION:Svatební den — {venue['name']}\r\n"
        "STATUS:CONFIRMED\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )
    filename = "svatba-kaci-rici-2027.ics"
    (output_dir / filename).write_text(ics_content, encoding="utf-8")
    return filename


def build():
    """Hlavní build pipeline."""
    print("🔨 Načítám data…")
    data = load_data()

    # Připrav výstupní adresář
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)

    # Kopíruj statické soubory (CSS, obrázky, fonty…)
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, DIST_DIR / "static")
        print("📁 Statické soubory zkopírovány.")

    # Vygeneruj .ics kalendář
    ics_filename = generate_ics(data, DIST_DIR)
    data["_ics_file"] = ics_filename
    print(f"📅 Kalendář vygenerován: {ics_filename}")

    # Vykreslení šablony
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # Custom filtry
    def czech_date(iso_date: str) -> str:
        """Převede '2027-06-12' na '12. 6. 2027'."""
        parts = iso_date.split("-")
        return f"{int(parts[2])}. {int(parts[1])}. {parts[0]}"

    env.filters["czech_date"] = czech_date
    template = env.get_template("index.html.j2")
    html = template.render(**data)

    # Cache-busting hash pro CSS
    output_path = DIST_DIR / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Hotovo → {output_path}")

    # robots.txt
    if data.get("privacy", {}).get("robots_noindex"):
        robots = "User-agent: *\nDisallow: /\n"
        (DIST_DIR / "robots.txt").write_text(robots, encoding="utf-8")
        print("🤖 robots.txt (noindex) vygenerován.")

    # .nojekyll pro GitHub Pages (zabraňuje ignorování složek/souborů)
    (DIST_DIR / ".nojekyll").touch()
    print("📦 .nojekyll pro GitHub Pages vytvořen.")

    return 0


def watch():
    """Sleduje změny v data/ a templates/ a automaticky přestaví."""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("❌ Pro --watch nainstalujte: pip install watchdog")
        return 1

    class RebuildHandler(FileSystemEventHandler):
        def on_any_event(self, event):
            if event.is_directory:
                return
            print(f"\n🔄 Změna detekována: {event.src_path}")
            try:
                build()
            except Exception as e:
                print(f"❌ Chyba při buildu: {e}")

    observer = Observer()
    observer.schedule(RebuildHandler(), str(DATA_FILE.parent), recursive=True)
    observer.schedule(RebuildHandler(), str(TEMPLATES_DIR), recursive=True)
    if STATIC_DIR.exists():
        observer.schedule(RebuildHandler(), str(STATIC_DIR), recursive=True)
    observer.start()

    print("👀 Sleduji změny… (Ctrl+C pro ukončení)")
    build()  # První build hned

    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build svatebního webu")
    parser.add_argument("--watch", action="store_true", help="Sleduj změny a automaticky přestavuj")
    args = parser.parse_args()

    sys.exit(watch() if args.watch else build())

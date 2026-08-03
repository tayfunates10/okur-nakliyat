#!/usr/bin/env python3
"""Minyatür tema katmanını statik sayfa üreticisine uygular.

Script tekrar çalıştırılabilir (idempotent) yapıdadır. Üretici dosyasını mümkünse
``origin/main`` kaynağından alır, yalnızca önbellek sürümünü günceller ve bütün
statik sayfaları resmî üreticiyle yeniden oluşturur.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools" / "sayfa.py"
OLD_VERSION = 'ONBELLEK_SURUMU = "36"'
NEW_VERSION = 'ONBELLEK_SURUMU = "37"'
EXPECTED_REFERENCE = "/assets/css/footer-map.css?v=37"


def clean_generator_source() -> str:
    """Main dalındaki üreticiyi al; git yoksa çalışma kopyasına geri dön."""
    try:
        result = subprocess.run(
            ["git", "show", "origin/main:tools/sayfa.py"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return GENERATOR.read_text(encoding="utf-8")


def update_generator_version() -> bool:
    current = GENERATOR.read_text(encoding="utf-8")
    source = clean_generator_source()

    if OLD_VERSION in source:
        updated = source.replace(OLD_VERSION, NEW_VERSION, 1)
    elif NEW_VERSION in source:
        updated = source
    else:
        raise SystemExit("tools/sayfa.py içinde beklenen önbellek sürümü bulunamadı.")

    if updated == current:
        return False

    GENERATOR.write_text(updated, encoding="utf-8", newline="\n")
    return True


def generate_pages() -> None:
    subprocess.run(["python3", str(GENERATOR)], cwd=ROOT, check=True)


def validate_pages() -> list[str]:
    invalid: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if any(part in {"node_modules", ".git", "sablon", "sayfalar"} for part in path.parts):
            continue
        if EXPECTED_REFERENCE not in path.read_text(encoding="utf-8"):
            invalid.append(str(path.relative_to(ROOT)))
    return invalid


def main() -> int:
    version_changed = update_generator_version()
    generate_pages()

    invalid = validate_pages()
    if invalid:
        raise SystemExit(
            "Minyatür tema sürümü bulunmayan statik sayfalar: " + ", ".join(invalid)
        )

    print("Önbellek sürümü:", "37 (güncellendi)" if version_changed else "37 (zaten güncel)")
    print("Tüm statik sayfalar tools/sayfa.py ile yeniden üretildi ve doğrulandı.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

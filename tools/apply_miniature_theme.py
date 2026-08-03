#!/usr/bin/env python3
"""Minyatür tema katmanını tüm statik çıktılarda etkinleştirir.

Script tekrar çalıştırılabilir (idempotent) yapıdadır. HTML dosyalarında yalnızca
footer-map asset sürümünü günceller; mevcut içerik ve SEO metinlerine dokunmaz.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_REFERENCE = "/assets/css/footer-map.css?v=36"
NEW_REFERENCE = "/assets/css/footer-map.css?v=37"


def update_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD_REFERENCE, NEW_REFERENCE)
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    candidates = sorted(ROOT.rglob("*.html"))
    changed: list[str] = []

    for path in candidates:
        if any(part in {"node_modules", ".git"} for part in path.parts):
            continue
        if update_file(path):
            changed.append(str(path.relative_to(ROOT)))

    if changed:
        print("Minyatür tema asset sürümü güncellendi:")
        for item in changed:
            print(f"- {item}")
    else:
        print("Değişiklik gerekmiyor; tüm HTML dosyaları güncel.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

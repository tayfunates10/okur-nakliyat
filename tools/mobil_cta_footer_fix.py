#!/usr/bin/env python3
"""Mobil CTA okunurluluğu ve CTA-footer boşluğunu tek seferde düzeltir."""

from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
STYLE = KOK / "assets/css/style.css"
GENERATOR = KOK / "tools/sayfa.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: beklenen parça {count} kez bulundu; 1 olmalı")
    return text.replace(old, new, 1)


def main() -> int:
    style = STYLE.read_text(encoding="utf-8")

    style = replace_once(
        style,
        "    padding-bottom: calc(4.75rem + env(safe-area-inset-bottom, 0px));",
        "    padding-bottom: 0;",
        "mobil main alt boşluğu",
    )
    style = replace_once(
        style,
        "../images/hero/okur-nakliyat-hero-background.webp?v=33",
        "../images/hero/okur-nakliyat-hero-background.webp?v=34",
        "CSS içi hero varlık sürümü",
    )

    sentinel = "18. Koyu CTA okunurluluğu ve mobil footer birleşimi"
    if sentinel in style:
        raise SystemExit("CTA/footer düzeltme bloğu zaten mevcut")

    override = r'''

/* ==========================================================================
   18. Koyu CTA okunurluluğu ve mobil footer birleşimi
   --------------------------------------------------------------------------
   `.hizmet-bilgi` açık yüzey için yazılmıştır. Koyu bölümün doğrudan çocuğu
   olduğunda beyaz karta dönüşüp beyaz metin ve ikincil butonu görünmez
   bırakıyordu. Koyu bağlam burada geri yüklenir.
   ========================================================================== */

.section-dark > .hizmet-bilgi {
  color: var(--text-on-dark);
  background:
    radial-gradient(circle at 88% 12%, rgba(245, 196, 0, 0.09), transparent 32%),
    rgba(255, 255, 255, 0.045);
  border-color: var(--border-on-dark-strong);
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.34);
}

.section-dark > .hizmet-bilgi .section-title {
  color: var(--text-on-dark);
}

.section-dark > .hizmet-bilgi .hizmet-giris,
.section-dark > .hizmet-bilgi .hizmet-kapanis {
  color: var(--text-on-dark-muted);
}

.section-dark > .hizmet-bilgi .btn-secondary {
  --btn-bg: rgba(255, 255, 255, 0.07);
  --btn-color: var(--color-white);
  --btn-border: rgba(255, 255, 255, 0.34);
}

.section-dark > .hizmet-bilgi .btn-secondary:hover,
.section-dark > .hizmet-bilgi .btn-secondary:focus-visible {
  --btn-bg: rgba(255, 255, 255, 0.13);
  --btn-color: var(--color-white);
  --btn-border: var(--color-yellow);
}

@media (max-width: 720px) {
  main > .section:last-child {
    padding-bottom: clamp(2.25rem, 8vw, 3rem);
  }

  main + .site-footer {
    padding-top: clamp(2.5rem, 8vw, 3.5rem);
  }

  .section-dark > .hizmet-bilgi {
    padding: clamp(1.35rem, 5vw, 1.75rem);
  }
}
'''

    STYLE.write_text(style.rstrip() + override + "\n", encoding="utf-8")

    generator = GENERATOR.read_text(encoding="utf-8")
    generator = replace_once(
        generator,
        'ONBELLEK_SURUMU = "33"',
        'ONBELLEK_SURUMU = "34"',
        "önbellek sürümü",
    )
    GENERATOR.write_text(generator, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

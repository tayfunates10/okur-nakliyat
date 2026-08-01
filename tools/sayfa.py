#!/usr/bin/env python3
"""
Statik sayfa üreticisi.

    sablon/ + sayfalar/  ->  index.html, <slug>/index.html, ...

Neden var: site 15+ sayfaya çıkarken header, mobil menü ve footer'ın her
dosyada tekrar etmesi gerekirdi. Menüye tek bağlantı eklemek 15 dosya
düzenlemek olur ve birini unutmak kaçınılmazdı. Ortak parçalar artık tek
yerde; bu betik statik HTML üretir. Sunucuda hiçbir şey değişmez.

Sayfa dosyası biçimi (sayfalar/<slug>.html):

    <!--json
    { "slug": "evden-eve-nakliyat", "baslik": "...", "aciklama": "...",
      "sema": [ ...schema.org düğümleri... ] }
    -->
    <main id="main"> ... </main>

`slug` boş ise sayfa kök `index.html` olur.

Kullanım:
    python3 tools/sayfa.py            # tümünü üret
    python3 tools/sayfa.py --kontrol  # üretilenler depodakiyle aynı mı?
"""

import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
SABLON = KOK / "sablon"
SAYFALAR = KOK / "sayfalar"
SITE = "https://okurnakliyatedremit.com"

ONBELLEK_SURUMU = "19"  # ?v= — bkz. docs/ekran-denetimi.md

ISLETME = f"{SITE}/#isletme"


def sayfa_oku(yol: Path) -> tuple[dict, str]:
    ham = yol.read_text(encoding="utf-8")
    eslesme = re.match(r"\s*<!--json\s*(\{.*?\})\s*-->\s*", ham, re.S)
    if not eslesme:
        raise SystemExit(f"{yol.name}: başta <!--json ... --> bloğu yok")
    veri = json.loads(eslesme.group(1))
    govde = ham[eslesme.end():]
    return veri, govde


def kirinti(veri: dict) -> dict | None:
    """BreadcrumbList — kök sayfada anlamsız olduğu için üretilmez."""
    yol = veri.get("kirinti")
    if not yol:
        return None
    ogeler = [{"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": SITE + "/"}]
    for i, (ad, baglanti) in enumerate(yol, start=2):
        oge = {"@type": "ListItem", "position": i, "name": ad}
        if baglanti:
            oge["item"] = SITE + baglanti
        ogeler.append(oge)
    return {"@type": "BreadcrumbList", "itemListElement": ogeler}


def sema_uret(veri: dict, kanonik: str) -> str:
    """Sayfaya özel @graph. İşletme düğümü yalnızca ana sayfada tam yazılır;
    diğer sayfalar ona @id ile bağlanır — aynı varlığı iki kez tanımlamak
    Google'ı bölünmüş kimlikle bırakır."""
    graf = []

    sayfa_id = kanonik + "#sayfa"
    sayfa = {
        "@type": veri.get("sayfaTipi", "WebPage"),
        "@id": sayfa_id,
        "url": kanonik,
        "name": veri["baslik"],
        "description": veri["aciklama"],
        "inLanguage": "tr-TR",
        "isPartOf": {"@id": f"{SITE}/#site"},
        "about": {"@id": ISLETME},
        "primaryImageOfPage": f"{SITE}/assets/images/og/okur-nakliyat-og.jpg",
    }

    ekmek = kirinti(veri)
    if ekmek:
        sayfa["breadcrumb"] = {"@id": kanonik + "#kirinti"}
        ekmek["@id"] = kanonik + "#kirinti"

    graf.append(sayfa)
    if ekmek:
        graf.append(ekmek)
    graf.extend(veri.get("sema", []))

    govde = json.dumps({"@context": "https://schema.org", "@graph": graf},
                       ensure_ascii=False, indent=2)
    govde = "\n".join("  " + s for s in govde.split("\n"))
    return '  <script type="application/ld+json">\n' + govde + "\n  </script>"


def uret(veri: dict, govde: str, sablonlar: dict) -> tuple[Path, str]:
    slug = veri["slug"].strip("/")
    kanonik = f"{SITE}/{slug}/" if slug else f"{SITE}/"
    # Ana sayfada bölüm çapaları aynı sayfada; alt sayfalarda köke gitmeli.
    kok = "" if not slug else "/"

    cikti = (KOK / slug / "index.html") if slug else (KOK / "index.html")

    html = sablonlar["taban"]
    for anahtar, deger in (
        ("{{BASLIK}}", veri["baslik"]),
        ("{{ACIKLAMA}}", veri["aciklama"]),
        ("{{KANONIK}}", kanonik),
        ("{{SEMA}}", sema_uret(veri, kanonik)),
        ("{{HEADER}}", sablonlar["header"]),
        ("{{FOOTER}}", sablonlar["footer"]),
        ("{{ICERIK}}", govde.strip("\n")),
    ):
        html = html.replace(anahtar, deger)

    html = html.replace("{{KOK}}", kok)
    # "Ana Sayfa" bağlantısı yalnızca ana sayfada aktif işaretlenir. Şablonda
    # sabit yazılıydı ve alt sayfalarda da aktif görünüyordu.
    html = html.replace("{{ANASAYFA}}", ' aria-current="page"' if not slug else "")
    html = html.replace("{{v}}", ONBELLEK_SURUMU)
    return cikti, html.rstrip("\n") + "\n"


def main() -> int:
    kontrol = "--kontrol" in sys.argv

    sablonlar = {
        ad: (SABLON / f"{ad}.html").read_text(encoding="utf-8").rstrip("\n")
        for ad in ("taban", "header", "footer")
    }

    dosyalar = sorted(SAYFALAR.glob("*.html"))
    if not dosyalar:
        print(f"sayfa bulunamadı ({SAYFALAR})")
        return 1

    fark = []
    for yol in dosyalar:
        veri, govde = sayfa_oku(yol)
        cikti, html = uret(veri, govde, sablonlar)

        if kontrol:
            mevcut = cikti.read_text(encoding="utf-8") if cikti.exists() else ""
            if mevcut != html:
                fark.append(cikti.relative_to(KOK))
            continue

        cikti.parent.mkdir(parents=True, exist_ok=True)
        cikti.write_text(html, encoding="utf-8")
        print(f"{yol.name:<34} -> {cikti.relative_to(KOK)}  ({len(html) / 1024:.1f} KB)")

    if kontrol:
        if fark:
            print("ÜRETİLEN ÇIKTI DEPODAKİNDEN FARKLI:")
            for f in fark:
                print("  ", f)
            print("`python3 tools/sayfa.py` çalıştırıp sonucu işleyin.")
            return 1
        print(f"{len(dosyalar)} sayfa güncel")
        return 0

    print(f"\n{len(dosyalar)} sayfa üretildi")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

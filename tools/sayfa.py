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
GALERI_LISTE = KOK / "galeri-kaynak" / "liste.json"
GALERI_GORSEL = KOK / "assets" / "images" / "gallery"
SITE = "https://okurnakliyatedremit.com"

ONBELLEK_SURUMU = "26"  # ?v= — bkz. docs/ekran-denetimi.md

# Ana sayfada gösterilecek fotoğraf sayısı; kalanı /galeri/ sayfasında.
GALERI_ONIZLEME_ADEDI = 6

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


def galeri_oku() -> list[dict]:
    """galeri-kaynak/liste.json — galerinin tek kaynağı.

    Sona eklenen fotoğraf sitede en başta görünsün diye numaraya göre
    büyükten küçüğe sıralanır. Karşılığı olan WebP üretilmemiş kayıtlar
    sessizce atlanmaz; hata verilir. Sessiz atlama, listeye eklenip
    fotoğrafı unutulan kaydın fark edilmemesine yol açar.
    """
    if not GALERI_LISTE.exists():
        return []

    veri = json.loads(GALERI_LISTE.read_text(encoding="utf-8"))
    fotolar = veri.get("fotograflar") or []
    if not fotolar:
        return []

    eksik = []
    for f in fotolar:
        no = int(f["no"])
        if not (GALERI_GORSEL / f"okur-nakliyat-galeri-{no:02d}-900.webp").exists():
            eksik.append(no)
    if eksik:
        raise SystemExit(
            "galeri-kaynak/liste.json içinde karşılığı olmayan numara(lar): "
            + ", ".join(str(n) for n in eksik)
            + f"\n{GALERI_GORSEL.relative_to(KOK)} altında ilgili WebP yok. "
            "Ham fotoğrafı galeri-kaynak/ içine koyup `python3 tools/cerceve.py` çalıştırın."
        )

    return sorted(fotolar, key=lambda f: int(f["no"]), reverse=True)


def galeri_izgara(fotolar: list[dict], girinti: str = "        ") -> str:
    """Fotoğraf listesinden .gallery-grid işaretlemesi üretir."""
    if not fotolar:
        return ""
    parcalar = [f'{girinti}<ul class="gallery-grid">']
    for f in fotolar:
        no = int(f["no"])
        aciklama = f["aciklama"].strip()
        alt = (f.get("alt") or aciklama).strip()
        taban = f"/assets/images/gallery/okur-nakliyat-galeri-{no:02d}"
        parcalar.append(f"""{girinti}  <li class="gallery-item">
{girinti}    <button class="gallery-trigger" type="button"
{girinti}            data-full="{taban}-1400.webp?v={{{{v}}}}"
{girinti}            data-caption="{aciklama}">
{girinti}      <img class="gallery-image"
{girinti}           src="{taban}-900.webp?v={{{{v}}}}"
{girinti}           srcset="{taban}-600.webp?v={{{{v}}}} 600w,
{girinti}                   {taban}-900.webp?v={{{{v}}}} 900w"
{girinti}           sizes="(max-width: 720px) 100vw, 320px"
{girinti}           width="900" height="675" loading="lazy" decoding="async"
{girinti}           alt="{alt}">
{girinti}      <span class="gallery-caption">{aciklama}</span>
{girinti}    </button>
{girinti}  </li>""")
    parcalar.append(f"{girinti}</ul>")
    return "\n".join(parcalar)


def uret(veri: dict, govde: str, sablonlar: dict, fotolar: list[dict]) -> tuple[Path, str]:
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
        # Kayan şerit yalnızca isteyen sayfada basılır; header'ın üstünde durur.
        ("{{SERIT}}", sablonlar["serit"] if veri.get("serit") else ""),
        ("{{HEADER}}", sablonlar["header"]),
        ("{{FOOTER}}", sablonlar["footer"]),
        ("{{ICERIK}}", govde.strip("\n")),
    ):
        html = html.replace(anahtar, deger)

    # Galeri işaretlemesi listeden üretilir; HTML'de elle fotoğraf durmaz.
    # Fotoğraf yoksa bölüm hiç basılmaz -- boş bir galeri yayınlanmaz.
    bolum = sablonlar["galeri-bolumu"] if fotolar else ""
    html = html.replace("{{GALERI_BOLUMU}}", bolum)
    html = html.replace("{{GALERI_ONIZLEME}}",
                        galeri_izgara(fotolar[:GALERI_ONIZLEME_ADEDI]))
    html = html.replace("{{GALERI_TAM}}", galeri_izgara(fotolar))

    html = html.replace("{{KOK}}", kok)
    # "Ana Sayfa" bağlantısı yalnızca ana sayfada aktif işaretlenir. Şablonda
    # sabit yazılıydı ve alt sayfalarda da aktif görünüyordu.
    html = html.replace("{{ANASAYFA}}", ' aria-current="page"' if not slug else "")
    html = html.replace("{{v}}", ONBELLEK_SURUMU)
    return cikti, html.rstrip("\n") + "\n"


def css_surumlerini_dogrula() -> list[str]:
    """CSS içindeki url() referansları da ?v= taşımalı ve sürüm güncel olmalı.

    HTML'deki ?v= şablondan geliyor, ama CSS şablonlanmıyor: oradaki sürüm
    elle güncelleniyor ve unutuluyor. Bu tam olarak yaşandı -- harita yeniden
    çizildiğinde CSS'teki eski sürüm yüzünden ziyaretçide bir yıl boyunca
    eski görsel kaldı.
    """
    sorunlar = []
    for css in sorted((KOK / "assets" / "css").glob("*.css")):
        metin = css.read_text(encoding="utf-8")
        for ham in re.findall(r'url\(\s*["\']?([^"\')]+)["\']?\s*\)', metin):
            if ham.startswith("data:"):
                continue
            if "?v=" not in ham:
                sorunlar.append(f"{css.name}: {ham} — ?v= yok")
            elif ham.rsplit("?v=", 1)[1] != ONBELLEK_SURUMU:
                sorunlar.append(
                    f"{css.name}: {ham} — sürüm {ONBELLEK_SURUMU} olmalı"
                )
    return sorunlar


def kaynak_surumlerini_dogrula() -> list[str]:
    """Şablon ve sayfa kaynaklarında sabit ?v= yazılmamalı; {{v}} kullanılmalı.

    Sabit yazılan sürüm, ONBELLEK_SURUMU'nü etkisiz bırakıyor: sabit
    artırılıyor ama HTML eski sürümü istemeye devam ediyor. Yayındaki dosya
    yenilense bile ziyaretçi `immutable` önbellek yüzünden bir yıl boyunca
    eskisini görüyor.

    Tam olarak bu yaşandı: bölüm 16'daki tasarım değişikliği sunucuya
    yüklendi ama sayfalar hâlâ style.css?v=19 istiyordu.
    """
    sorunlar = []
    for kok in (SABLON, SAYFALAR):
        for yol in sorted(kok.glob("*.html")):
            metin = yol.read_text(encoding="utf-8")
            for eslesme in re.finditer(r"\?v=(\d+)", metin):
                satir = metin[: eslesme.start()].count("\n") + 1
                sorunlar.append(
                    f"{yol.relative_to(KOK)}:{satir}: "
                    f"?v={eslesme.group(1)} sabit yazılmış — {{{{v}}}} olmalı"
                )
    return sorunlar


def main() -> int:
    kontrol = "--kontrol" in sys.argv

    kaynak_sorunlari = kaynak_surumlerini_dogrula()
    if kaynak_sorunlari:
        print("KAYNAKTA SABİT VARLIK SÜRÜMÜ:")
        for s in kaynak_sorunlari:
            print("  ", s)
        return 1

    css_sorunlari = css_surumlerini_dogrula()
    if css_sorunlari:
        print("CSS İÇİNDEKİ VARLIK SÜRÜMÜ HATALI:")
        for s in css_sorunlari:
            print("  ", s)
        return 1

    sablonlar = {
        ad: (SABLON / f"{ad}.html").read_text(encoding="utf-8").rstrip("\n")
        for ad in ("taban", "header", "footer", "serit", "galeri-bolumu")
    }

    fotolar = galeri_oku()

    dosyalar = sorted(SAYFALAR.glob("*.html"))
    if not dosyalar:
        print(f"sayfa bulunamadı ({SAYFALAR})")
        return 1

    # Fotoğraf yokken galeri sayfası üretilmez: boş bir sayfa yayınlamak
    # hem ziyaretçi hem arama motoru için değersiz. Ana sayfadaki bölüm de
    # {{GALERI_ONIZLEME}} boş kaldığı için kendiliğinden görünmez olur.
    if not fotolar:
        dosyalar = [d for d in dosyalar if d.stem != "galeri"]
        print("galeri-kaynak/liste.json boş — /galeri/ sayfası üretilmedi.")
        print("Fotoğraf eklendiğinde sitemap.xml'e /galeri/ satırı da eklenmeli.")

    fark = []
    for yol in dosyalar:
        veri, govde = sayfa_oku(yol)
        cikti, html = uret(veri, govde, sablonlar, fotolar)

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

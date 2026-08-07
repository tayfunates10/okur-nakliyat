#!/usr/bin/env python3
"""
Galeri fotoğraflarını siteye uygun boyutlara indirger.

    galeri-kaynak/*.jpg  ->  assets/images/gallery/okur-nakliyat-galeri-NN-{600,900,1400}.webp

Kaynak klasör yayına kopyalanmaz (bkz. deploy.yml); yalnızca çıktılar siteye
gider.

Fotoğrafın altına marka bandı (logo, telefon, adres) basan bir sürümü vardı;
bant istenmediği için kaldırıldı. Bu araç artık yalnızca kırpma, ölçekleme ve
WebP'ye çevirme yapıyor.

Oran çıktının tamamı için geçerlidir: galeri kartı CSS'te 4:3 ve
`object-fit: cover` kullanıyor, kaynak ne olursa olsun 4:3'e getirilir.

Bazı galeri görselleri doğrudan hazır WebP çıktıları olarak depoya eklenebilir.
Bu durumda `--temiz`, liste.json'da kayıtlı numaraların hazır çıktılarını
silmez; yalnızca listeden kaldırılmış numaralara ait eski çıktıları temizler.
Böylece daha sonra yeni ham fotoğraf eklendiğinde manuel yüklenen hazır
görseller kaybolmaz.

Kullanım:
    python3 tools/galeri-goruntu.py                 # galeri-kaynak/ içindeki her şey
    python3 tools/galeri-goruntu.py foto.jpg        # tek dosya
    python3 tools/galeri-goruntu.py --temiz         # listede olmayan eski çıktıları siler
"""

import json
import re
import sys
from pathlib import Path

from PIL import Image

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "galeri-kaynak"
CIKTI = KOK / "assets" / "images" / "gallery"
LISTE = KAYNAK / "liste.json"
AYAR = json.loads((KOK / "tools" / "galeri-goruntu.json").read_text(encoding="utf-8"))

UZANTILAR = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"}
CIKTI_DESENI = re.compile(r"^okur-nakliyat-galeri-(\d+)-(\d+)\.webp$")


def kaynak_numarasi(yol: Path) -> int:
    """Kaynak dosya adının başındaki sıra numarasını döndürür."""
    onek = yol.name.split("-", 1)[0]
    if not onek.isdigit():
        raise ValueError(
            f"galeri kaynak dosyası sıra numarasıyla başlamalı: {yol.name}"
        )
    return int(onek)


def liste_numaralari() -> set[int]:
    """liste.json içinde yayınlanması istenen galeri numaralarını döndürür."""
    if not LISTE.exists():
        return set()

    veri = json.loads(LISTE.read_text(encoding="utf-8"))
    fotograflar = veri.get("fotograflar", [])
    numaralar = {int(foto["no"]) for foto in fotograflar}

    if len(numaralar) != len(fotograflar):
        raise ValueError("galeri-kaynak/liste.json içinde tekrar eden 'no' değeri var")

    return numaralar


def kirp_oranla(im: Image.Image, en: int, boy: int) -> Image.Image:
    """Kaynağı hedef orana ortadan kırpar, sonra hedef boyuta ölçekler."""
    hedef = en / boy
    kaynak = im.width / im.height

    if kaynak > hedef:
        yeni_en = round(im.height * hedef)
        sol = (im.width - yeni_en) // 2
        im = im.crop((sol, 0, sol + yeni_en, im.height))
    elif kaynak < hedef:
        yeni_boy = round(im.width / hedef)
        ust = (im.height - yeni_boy) // 2
        im = im.crop((0, ust, im.width, ust + yeni_boy))

    return im.resize((en, boy), Image.LANCZOS)


def isle(kaynak: Path, sira: int) -> list[Path]:
    foto = Image.open(kaynak)
    if foto.mode != "RGB":
        foto = foto.convert("RGB")

    en_oran, boy_oran = AYAR["oran"]
    yazilan = []
    for genislik in AYAR["boyutlar"]:
        boy = round(genislik * boy_oran / en_oran)
        cikti = CIKTI / f"okur-nakliyat-galeri-{sira:02d}-{genislik}.webp"
        kirp_oranla(foto, genislik, boy).save(
            cikti, "WEBP", quality=AYAR["kalite"], method=6
        )
        yazilan.append(cikti)
    return yazilan


def eski_ciktilari_temizle(korunacak: set[int]) -> int:
    """Listede olmayan galeri numaralarına ait eski WebP çıktıları siler."""
    silinen = 0
    if not CIKTI.exists():
        return silinen

    for eski in CIKTI.glob("okur-nakliyat-galeri-*.webp"):
        eslesme = CIKTI_DESENI.match(eski.name)
        if not eslesme:
            continue
        no = int(eslesme.group(1))
        if no not in korunacak:
            eski.unlink()
            silinen += 1

    return silinen


def ciktilari_dogrula(numaralar: set[int]) -> list[str]:
    """Listelenen her fotoğraf için beklenen responsive çıktıları doğrular."""
    eksik = []
    for no in sorted(numaralar):
        for genislik in AYAR["boyutlar"]:
            yol = CIKTI / f"okur-nakliyat-galeri-{no:02d}-{genislik}.webp"
            if not yol.is_file() or yol.stat().st_size == 0:
                eksik.append(str(yol.relative_to(KOK)))
    return eksik


def main() -> int:
    argumanlar = [a for a in sys.argv[1:] if not a.startswith("--")]
    temiz = "--temiz" in sys.argv
    numaralar = liste_numaralari()

    if temiz:
        silinen = eski_ciktilari_temizle(numaralar)
        print(
            f"listede olmayan eski çıktılar silindi: {silinen} "
            f"({CIKTI.relative_to(KOK)})"
        )

    CIKTI.mkdir(parents=True, exist_ok=True)

    if argumanlar:
        dosyalar = [Path(a) for a in argumanlar]
    else:
        if not KAYNAK.exists():
            print(f"kaynak klasör yok: {KAYNAK}")
            return 1
        dosyalar = sorted(
            (p for p in KAYNAK.iterdir() if p.suffix in UZANTILAR),
            key=lambda p: (kaynak_numarasi(p), p.name.lower()),
        )

    toplam = 0
    for yol in dosyalar:
        sira = kaynak_numarasi(yol)
        yazilan = isle(yol, sira)
        toplam += len(yazilan)
        boyutlar = "  ".join(f"{p.stat().st_size // 1024}K" for p in yazilan)
        print(f"{sira:02d}  {yol.name:<40} -> {len(yazilan)} dosya  {boyutlar}")

    eksik = ciktilari_dogrula(numaralar)
    if eksik:
        print("\nHATA: liste.json içinde kayıtlı bazı galeri çıktıları eksik:", file=sys.stderr)
        for yol in eksik:
            print(f"  - {yol}", file=sys.stderr)
        return 1

    print(
        f"\n{len(dosyalar)} kaynak işlendi, {toplam} dosya yazıldı; "
        f"{len(numaralar)} galeri kaydı doğrulandı -> {CIKTI}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

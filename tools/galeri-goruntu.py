#!/usr/bin/env python3
"""
Galeri fotoğraflarını siteye uygun boyutlara indirger.

    galeri-kaynak/*.jpg      -> assets/images/gallery/okur-nakliyat-galeri-NN-{600,900,1400}.webp
    galeri-kaynak/*.png.b64  -> assets/images/gallery/okur-nakliyat-galeri-NN-{600,900,1400}.webp

Kaynak klasör yayına kopyalanmaz (bkz. deploy.yml); yalnızca çıktılar siteye
gider. `.b64` dosyaları, GitHub metin dosyası yükleme kanalından aktarılan
PNG/JPEG/WebP görsellerinin saf Base64 içeriğini taşır ve işlem sırasında
bellekte çözülür.

Fotoğrafın altına marka bandı (logo, telefon, adres) basan bir sürümü vardı;
bant istenmediği için kaldırıldı. Bu araç artık yalnızca kırpma, ölçekleme ve
WebP'ye çevirme yapıyor.

Oran çıktının tamamı için geçerlidir: galeri kartı CSS'te 4:3 ve
`object-fit: cover` kullanıyor, kaynak ne olursa olsun 4:3'e getirilir.

Kullanım:
    python3 tools/galeri-goruntu.py                 # galeri-kaynak/ içindeki her şey
    python3 tools/galeri-goruntu.py foto.jpg        # tek dosya
    python3 tools/galeri-goruntu.py --temiz         # önce eski çıktıları siler
"""

import base64
import io
import json
import sys
from pathlib import Path

from PIL import Image

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "galeri-kaynak"
CIKTI = KOK / "assets" / "images" / "gallery"
AYAR = json.loads((KOK / "tools" / "galeri-goruntu.json").read_text(encoding="utf-8"))

UZANTILAR = {".jpg", ".jpeg", ".png", ".webp"}
BASE64_UZANTISI = ".b64"


def kaynak_mi(yol: Path) -> bool:
    """Desteklenen normal görselleri ve Base64 kaynaklarını seçer."""
    if yol.suffix.lower() in UZANTILAR:
        return True
    if yol.suffix.lower() != BASE64_UZANTISI:
        return False
    return Path(yol.stem).suffix.lower() in UZANTILAR


def fotograf_ac(kaynak: Path) -> Image.Image:
    """Normal görseli veya saf Base64 metnini Pillow ile açar."""
    if kaynak.suffix.lower() != BASE64_UZANTISI:
        return Image.open(kaynak)

    kodlanmis = kaynak.read_text(encoding="ascii").strip()
    try:
        ham = base64.b64decode(kodlanmis, validate=True)
    except ValueError as hata:
        raise ValueError(f"geçersiz Base64 galeri kaynağı: {kaynak}") from hata
    return Image.open(io.BytesIO(ham))


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
    foto = fotograf_ac(kaynak)
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


def main() -> int:
    argumanlar = [a for a in sys.argv[1:] if not a.startswith("--")]
    temiz = "--temiz" in sys.argv

    if temiz and CIKTI.exists():
        for eski in CIKTI.glob("okur-nakliyat-galeri-*.webp"):
            eski.unlink()
        print(f"eski çıktılar silindi ({CIKTI.relative_to(KOK)})")

    CIKTI.mkdir(parents=True, exist_ok=True)

    if argumanlar:
        dosyalar = [Path(a) for a in argumanlar]
    else:
        if not KAYNAK.exists():
            print(f"kaynak klasör yok: {KAYNAK}")
            return 1
        dosyalar = sorted(p for p in KAYNAK.iterdir() if kaynak_mi(p))

    if not dosyalar:
        print(f"kaynak klasörde fotoğraf yok ({KAYNAK}) — yapılacak iş yok")
        return 0

    toplam = 0
    for sira, yol in enumerate(dosyalar, start=1):
        yazilan = isle(yol, sira)
        toplam += len(yazilan)
        boyutlar = "  ".join(f"{p.stat().st_size // 1024}K" for p in yazilan)
        print(f"{sira:02d}  {yol.name:<40} -> {len(yazilan)} dosya  {boyutlar}")

    print(f"\n{len(dosyalar)} fotoğraf, {toplam} dosya yazıldı -> {CIKTI}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

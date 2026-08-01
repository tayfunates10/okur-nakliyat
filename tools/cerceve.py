#!/usr/bin/env python3
"""
Galeri fotoğraflarına marka çerçevesi uygular.

    galeri-kaynak/*.jpg  ->  assets/images/gallery/okur-nakliyat-galeri-NN-{600,900,1400}.webp

Kaynak klasör yayına kopyalanmaz (bkz. deploy.yml); yalnızca çıktılar siteye gider.

Çerçeve: fotoğrafın altında siyah bir şerit, üst kenarında marka sarısı çizgi.
Şeritte marka işareti, ad, telefon ve (doluysa) e-posta / adres / site yer alır.
İçerik tools/cerceve.json dosyasından okunur; boş alan hiç yazılmaz.

Ölçüler çıktı genişliğine oranlanır, yani 600 px ile 1400 px çıktı birebir aynı
düzene sahiptir. Çerçeve her boyut için ayrıca çizilir — 1400'ü küçültmek yazıyı
bulanıklaştırırdı.

Kullanım:
    python3 tools/cerceve.py                 # galeri-kaynak/ içindeki her şeyi işler
    python3 tools/cerceve.py foto.jpg        # tek dosya
    python3 tools/cerceve.py --temiz         # önce eski çıktıları siler
"""

import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "galeri-kaynak"
CIKTI = KOK / "assets" / "images" / "gallery"
AYAR = json.loads((KOK / "tools" / "cerceve.json").read_text(encoding="utf-8"))
ISARET = KOK / "tools" / "marka-isaret.png"

SARI = (245, 196, 0)
SIYAH = (11, 11, 11)
BEYAZ = (255, 255, 255)
GRI = (176, 176, 176)

# ubuntu-latest ve bu ortamda garanti bulunan tek Türkçe destekli aile.
# Sitenin Manrope'u yerel değil; çerçeve metni sonuçtaki dosyaya gömüldüğü
# için ağdan gelen bir yazı tipine bağlamak çıktıyı belirsiz yapardı.
YAZI_KALIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
YAZI_NORMAL = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

UZANTILAR = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"}


def font(yol: str, boyut: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(yol, max(boyut, 6))


def dolu(anahtar: str) -> str:
    return str(AYAR.get(anahtar, "")).strip()


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


def cerceve_ciz(foto: Image.Image, genislik: int) -> Image.Image:
    """Fotoğrafın altına marka şeridi ekler ve tamamını döndürür."""
    en_oran, boy_oran = AYAR["oran"]
    foto_boy = round(genislik * boy_oran / en_oran)
    foto = kirp_oranla(foto, genislik, foto_boy)

    serit = round(genislik * 0.145)
    cizgi = max(round(genislik * 0.0045), 2)
    bosluk = round(genislik * 0.033)
    ara = round(genislik * 0.025)  # sol ve sağ blok arasında bırakılacak en az boşluk

    tuval = Image.new("RGB", (genislik, foto_boy + serit), SIYAH)
    tuval.paste(foto.convert("RGB"), (0, 0))

    ciz = ImageDraw.Draw(tuval)
    ciz.rectangle([0, foto_boy, genislik, foto_boy + cizgi], fill=SARI)

    serit_ust = foto_boy + cizgi
    serit_ic = serit - cizgi
    orta = serit_ust + serit_ic / 2

    def genisligi(metin: str, f: ImageFont.FreeTypeFont) -> float:
        return ciz.textlength(metin, font=f)

    # --- Sol blok: marka işareti + ad. Önce ölçülür, çizim sonra. ---
    sol_x = bosluk
    isaret_im = None
    isaret_kutu = (0, 0)
    if ISARET.exists():
        isaret_im = Image.open(ISARET).convert("RGBA")
        h = round(serit_ic * 0.40)
        w = round(h * isaret_im.width / isaret_im.height)
        isaret_im = isaret_im.resize((w, h), Image.LANCZOS)
        isaret_kutu = (w, h)

    marka = dolu("marka")
    f_marka = font(YAZI_KALIN, round(serit_ic * 0.24))
    marka_genislik = genisligi(marka, f_marka) if marka else 0
    isaret_ara = round(bosluk * 0.5) if (isaret_im is not None and marka) else 0
    sol_genislik = isaret_kutu[0] + isaret_ara + marka_genislik

    # --- Sağ blok: telefon üstte, ikincil bilgiler altta ---
    sag = genislik - bosluk
    telefon = dolu("telefon")
    parcalar = [p for p in (dolu("eposta"), dolu("adres"), dolu("site")) if p]

    kullanilabilir = genislik - 2 * bosluk - sol_genislik - ara

    f_tel = font(YAZI_KALIN, round(serit_ic * 0.30))
    tel_genislik = genisligi(telefon, f_tel) if telefon else 0

    # İkincil satır sol bloğa çarpmasın: önce küçült, yetmezse baştan parça at.
    # Eskiden sabit punto kullanılıyordu ve uzun adres marka adının üstüne
    # biniyordu.
    f_alt = font(YAZI_NORMAL, round(serit_ic * 0.19))
    ikincil = " · ".join(parcalar)
    while ikincil:
        punto = round(serit_ic * 0.19)
        f_alt = font(YAZI_NORMAL, punto)
        while genisligi(ikincil, f_alt) > kullanilabilir and punto > round(serit_ic * 0.13):
            punto -= 1
            f_alt = font(YAZI_NORMAL, punto)
        if genisligi(ikincil, f_alt) <= kullanilabilir or len(parcalar) <= 1:
            break
        parcalar.pop()  # en az öncelikli bilgiden başlayarak çıkar
        ikincil = " · ".join(parcalar)

    if tel_genislik > kullanilabilir:
        punto = round(serit_ic * 0.30)
        while tel_genislik > kullanilabilir and punto > round(serit_ic * 0.18):
            punto -= 1
            f_tel = font(YAZI_KALIN, punto)
            tel_genislik = genisligi(telefon, f_tel)

    # --- Çizim ---
    if isaret_im is not None:
        tuval.paste(isaret_im, (sol_x, round(orta - isaret_kutu[1] / 2)), isaret_im)
        sol_x += isaret_kutu[0] + isaret_ara
    if marka:
        ciz.text((sol_x, orta), marka, font=f_marka, fill=BEYAZ, anchor="lm")

    if telefon and ikincil:
        ciz.text((sag, orta - serit_ic * 0.19), telefon, font=f_tel, fill=SARI, anchor="rm")
        ciz.text((sag, orta + serit_ic * 0.21), ikincil, font=f_alt, fill=GRI, anchor="rm")
    elif telefon:
        ciz.text((sag, orta), telefon, font=f_tel, fill=SARI, anchor="rm")
    elif ikincil:
        ciz.text((sag, orta), ikincil, font=f_alt, fill=GRI, anchor="rm")

    return tuval


def isle(kaynak: Path, sira: int) -> list[Path]:
    foto = Image.open(kaynak)
    if foto.mode not in ("RGB", "RGBA"):
        foto = foto.convert("RGB")

    yazilan = []
    for genislik in AYAR["boyutlar"]:
        cikti = CIKTI / f"okur-nakliyat-galeri-{sira:02d}-{genislik}.webp"
        cerceve_ciz(foto, genislik).save(
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
        print("eski çıktılar silindi")

    CIKTI.mkdir(parents=True, exist_ok=True)

    if argumanlar:
        dosyalar = [Path(a) for a in argumanlar]
    else:
        if not KAYNAK.exists():
            print(f"kaynak klasör yok: {KAYNAK}")
            print("fotoğrafları galeri-kaynak/ altına koyun")
            return 1
        dosyalar = sorted(p for p in KAYNAK.iterdir() if p.suffix in UZANTILAR)

    if not dosyalar:
        # Boş kaynak klasörü hata değil, normal bir durum: fotoğraflar henüz
        # eklenmemiş olabilir. Hata döndürülünce iş akışı her seferinde
        # kırmızıya düşüyordu. Klasörün kendisi yoksa yukarıda 1 dönülür.
        print(f"kaynak klasörde fotoğraf yok ({KAYNAK}) — yapılacak iş yok")
        return 0

    eksik = [d for d in dosyalar if not d.exists()]
    if eksik:
        print("bulunamayan dosyalar: " + ", ".join(str(d) for d in eksik))
        return 1

    toplam = 0
    for sira, kaynak in enumerate(dosyalar, start=1):
        yazilan = isle(kaynak, sira)
        boyutlar = " ".join(f"{p.stat().st_size / 1024:.0f}K" for p in yazilan)
        print(f"{sira:02d}  {kaynak.name:<40} -> {len(yazilan)} dosya  {boyutlar}")
        toplam += len(yazilan)

    print(f"\n{len(dosyalar)} fotoğraf, {toplam} dosya yazıldı -> {CIKTI}")
    if not dolu("eposta"):
        print("not: tools/cerceve.json içinde 'eposta' boş, çerçeveye yazılmadı")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

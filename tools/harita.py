#!/usr/bin/env python3
"""
Hizmet bölgesi haritasındaki Edremit işaretini ve güzergâh çizgilerini çizer.

    tools/harita-taban.webp  ->  assets/images/coverage/okur-nakliyat-hizmet-bolgesi-{900,1300}.webp

Taban dosyada kara parçası ve şehir noktaları var; Edremit halkası ile ona
bağlı kesikli güzergâhlar yok. Bu betik onları her seferinde yeniden çizer,
yani konum değişince görsel elle rötuşlanmaz — sayı değiştirilip betik
yeniden çalıştırılır.

Neden gerekti: özgün görselde halka Edremit'in ~216 px doğusunda, ~50 px
güneyinde duruyordu (yaklaşık Afyon/Kütahya). Konum, Türkiye'nin gerçek uç
koordinatları taban görselin kara sınırına oturtularak hesaplandı.

Kullanım:
    python3 tools/harita.py
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw

KOK = Path(__file__).resolve().parent.parent
TABAN = KOK / "tools" / "harita-taban.webp"
CIKTI = KOK / "assets" / "images" / "coverage"

SARI = (243, 197, 3, 255)
KARA = (16, 16, 16, 255)

# Türkiye anakarasının yaklaşık uç koordinatları. Taban görselin kara sınırı
# bu dikdörtgene karşılık gelir; ara konumlar doğrusal ölçeklenir. Silüet
# stilize olduğu için bu bir yaklaşım, ama görsel yerleştirmeden çok daha
# tutarlı.
LON_BATI, LON_DOGU = 26.0, 44.8
LAT_KUZEY, LAT_GUNEY = 42.1, 35.8

EDREMIT = (27.024, 39.596)

# Güzergâh varış noktaları: taban görseldeki şehir noktalarının merkezleri.
VARISLAR = [(1108, 187), (1020, 303), (884, 387)]

# Halka ölçüleri (1300 px genişlikteki taban için, px)
MERKEZ_R = 22
IC_HALKA_R, IC_HALKA_KALINLIK = 45, 7
DIS_HALKA_R, DIS_HALKA_KALINLIK = 61, 7

# Kesikli çizgi
CIZGI_KALINLIK = 9
CIZIK = 22
BOSLUK = 14


def kara_siniri(im: Image.Image) -> tuple[int, int, int, int]:
    """Taban görseldeki çizili alanın sınır kutusu."""
    alfa = im.getchannel("A").point(lambda v: 255 if v > 180 else 0)
    return alfa.getbbox()


def edremit_konumu(im: Image.Image) -> tuple[float, float]:
    x0, y0, x1, y1 = kara_siniri(im)
    lon, lat = EDREMIT
    fx = (lon - LON_BATI) / (LON_DOGU - LON_BATI)
    fy = (LAT_KUZEY - lat) / (LAT_KUZEY - LAT_GUNEY)
    return x0 + fx * (x1 - x0 - 1), y0 + fy * (y1 - y0 - 1)


def halka(ciz: ImageDraw.ImageDraw, cx: float, cy: float) -> None:
    # Edremit kıyıda olduğu için işaretin bir kısmı denize (sarı zemine)
    # taşıyor; sarı halka orada kaybolurdu. Altına kara rengiyle aynı koyu
    # disk konur: karada görünmez, denizin üstünde rozet gibi okunur.
    zemin = DIS_HALKA_R + 7
    ciz.ellipse([cx - zemin, cy - zemin, cx + zemin, cy + zemin], fill=KARA)

    for r, k in ((DIS_HALKA_R, DIS_HALKA_KALINLIK), (IC_HALKA_R, IC_HALKA_KALINLIK)):
        ciz.ellipse([cx - r, cy - r, cx + r, cy + r], outline=SARI, width=k)
    ciz.ellipse(
        [cx - MERKEZ_R, cy - MERKEZ_R, cx + MERKEZ_R, cy + MERKEZ_R], fill=SARI
    )


def kesikli_egri(ciz, p0, p1, bukum: float) -> None:
    """p0'dan p1'e, ortası `bukum` kadar yukarı bombeli kesikli yay."""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    # kontrol noktası, kirişe dik yönde kaydırılır
    dx, dy = x1 - x0, y1 - y0
    uzunluk = math.hypot(dx, dy) or 1
    kx, ky = mx - dy / uzunluk * bukum, my + dx / uzunluk * bukum

    def nokta(t):
        u = 1 - t
        return (u * u * x0 + 2 * u * t * kx + t * t * x1,
                u * u * y0 + 2 * u * t * ky + t * t * y1)

    # Yay boyunca eşit aralıklı yürü; çizik/boşluk sırayla uygulanır.
    ornek = [nokta(i / 600) for i in range(601)]
    toplam = 0.0
    mesafeler = [0.0]
    for i in range(1, len(ornek)):
        toplam += math.dist(ornek[i - 1], ornek[i])
        mesafeler.append(toplam)

    def konum(s):
        for i in range(1, len(mesafeler)):
            if mesafeler[i] >= s:
                onceki = mesafeler[i - 1]
                t = (s - onceki) / (mesafeler[i] - onceki or 1)
                ax, ay = ornek[i - 1]
                bx, by = ornek[i]
                return (ax + (bx - ax) * t, ay + (by - ay) * t)
        return ornek[-1]

    s = DIS_HALKA_R + 24  # halkanın (ve koyu zemininin) dışından başla
    son = toplam - 26      # varış noktasının biraz öncesinde bitir
    while s < son:
        bitis = min(s + CIZIK, son)
        ciz.line([konum(s), konum(bitis)], fill=SARI, width=CIZGI_KALINLIK)
        s = bitis + BOSLUK


def main() -> int:
    if not TABAN.exists():
        print(f"taban görsel yok: {TABAN}")
        return 1

    taban = Image.open(TABAN).convert("RGBA")
    cx, cy = edremit_konumu(taban)

    katman = Image.new("RGBA", taban.size, (0, 0, 0, 0))
    ciz = ImageDraw.Draw(katman)

    for i, varis in enumerate(VARISLAR):
        # Üstteki güzergâh daha çok, alttaki daha az bombeli — özgün çizimdeki
        # yelpaze görünümü böyle korunuyor.
        kesikli_egri(ciz, (cx, cy), varis, bukum=(78, 30, -34)[i])

    halka(ciz, cx, cy)

    sonuc = Image.alpha_composite(taban, katman)
    CIKTI.mkdir(parents=True, exist_ok=True)

    for genislik in (1300, 900):
        boy = round(sonuc.height * genislik / sonuc.width)
        yol = CIKTI / f"okur-nakliyat-hizmet-bolgesi-{genislik}.webp"
        sonuc.resize((genislik, boy), Image.LANCZOS).save(
            yol, "WEBP", quality=88, method=6
        )
        print(f"{yol.name}  {genislik}x{boy}  {yol.stat().st_size / 1024:.0f} KB")

    x0, y0, x1, y1 = kara_siniri(taban)
    print(
        f"\nEdremit işareti: ({cx:.0f}, {cy:.0f}) "
        f"= %{100 * cx / taban.width:.1f} soldan, %{100 * cy / taban.height:.1f} üstten"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

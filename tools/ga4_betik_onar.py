#!/usr/bin/env python3
"""Geçici GA4 üretici betiğindeki f-string kaçışını çalıştırmadan önce düzeltir."""

from pathlib import Path

YOL = Path(__file__).with_name("ga4_kurulum.py")
metin = YOL.read_text(encoding="utf-8")

eski_satir = '    window.OKUR_ANALYTICS_ID = \\"{OLCUM_KIMLIGI\\";'
yeni_satir = '    window.OKUR_ANALYTICS_ID = \\"{OLCUM_KIMLIGI}\\";'
if eski_satir not in metin:
    raise SystemExit("Ölçüm kimliği satırı beklenen biçimde bulunamadı")
metin = metin.replace(eski_satir, yeni_satir, 1)

eski_blok = '''    # Yukarıdaki f-string içinde kimlik kapanışını açıkça kur; yanlış süslü
    # parantezlerin Python tarafından yorumlanmasını önle.
    baslangic = baslangic.replace(f'\\"{OLCUM_KIMLIGI\\";', f'\\"{OLCUM_KIMLIGI}\\";')
'''
if eski_blok not in metin:
    raise SystemExit("Geçici f-string düzeltme bloğu bulunamadı")
metin = metin.replace(eski_blok, "", 1)

YOL.write_text(metin, encoding="utf-8")

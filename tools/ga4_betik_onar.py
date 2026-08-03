#!/usr/bin/env python3
"""Geçici GA4 üretici betiğindeki f-string satırını çalıştırmadan önce düzeltir."""

from pathlib import Path

YOL = Path(__file__).with_name("ga4_kurulum.py")
metin = YOL.read_text(encoding="utf-8")

eski = '    window.OKUR_ANALYTICS_ID = "{OLCUM_KIMLIGI";'
yeni = '    window.OKUR_ANALYTICS_ID = "{OLCUM_KIMLIGI}";'
if eski not in metin:
    raise SystemExit("Ölçüm kimliği satırı beklenen biçimde bulunamadı")
metin = metin.replace(eski, yeni, 1)

satirlar = []
atlanan = 0
for satir in metin.splitlines():
    if "Yukarıdaki f-string içinde kimlik kapanışını" in satir:
        atlanan += 1
        continue
    if "parantezlerin Python tarafından yorumlanmasını önle" in satir:
        atlanan += 1
        continue
    if "baslangic = baslangic.replace" in satir:
        atlanan += 1
        continue
    satirlar.append(satir)

if atlanan != 3:
    raise SystemExit(f"Geçici düzeltme bloğunda {atlanan} satır bulundu; 3 olmalı")

YOL.write_text("\n".join(satirlar) + "\n", encoding="utf-8")

# Galeri fotoğrafları için alt bant — ChatGPT komutları

## Önce şunu bilin

Bu depo alt bandı **zaten kendi başına** ekliyor. Ham fotoğrafı
`galeri-kaynak/` klasörüne koyup `main` dalına gönderdiğinizde
`tools/cerceve.py` her fotoğrafın altına logo, marka adı, telefon ve adres
içeren siyah-sarı bandı basıyor; bilgiler `tools/cerceve.json` içinden
geliyor ve tek yerden değiştiriliyor.

Yani ChatGPT'ye ihtiyaç yok. Aşağıdaki komutlar, bandı **elle** ya da
başka bir araçla üretmek istediğinizde işinize yarar; örneğin bandın
görünümünü değiştirmeden önce alternatif tasarımlar görmek isterseniz.

Bir uyarı: dil modelleri görsel üretirken metni sık sık bozuyor. Telefon
numarasının bir rakamı değişirse fark etmek zor, sonucu da müşteri
kaybettirir. ChatGPT'den gelen her bandı **rakam rakam** kontrol edin.

---

## 1. komut — bandı tasarlatmak

> Bir nakliyat firması için fotoğrafların altına konacak bir marka bandı
> tasarla. Bandın kendisini istiyorum, fotoğrafı değil.
>
> **Firma bilgileri (birebir bu şekilde yazılacak, değiştirme):**
> - Marka: OKUR NAKLİYAT
> - Telefon: 0537 226 50 43
> - Adres: Atatürk Mah. Kalkım Cad. No: 4, Edremit / Balıkesir
> - Site: okurnakliyatedremit.com
>
> **Ölçü ve biçim:**
> - Bant 1400 × 203 piksel (fotoğrafın altına eklenecek, tam genişlik).
> - Üst kenarında 6 piksel kalınlığında sarı bir çizgi olsun.
> - Zemin düz koyu siyah (#0B0B0B). Doku, gradyan, parlama yok.
> - Vurgu rengi sarı (#F5C400). Üçüncü bir renk kullanma.
>
> **Yerleşim:**
> - Solda marka adı "OKUR NAKLİYAT", kalın ve büyük harf.
> - Sağda telefon numarası, sarı ve en büyük ikinci öğe — banttaki en
>   dikkat çeken bilgi telefon olmalı.
> - Telefonun hemen altında, daha küçük ve gri: adres ve site adresi,
>   aralarında ince bir ayraç.
> - Sol ve sağ blok arasında en az 35 piksel boşluk kalsın; hiçbir yazı
>   kenara 45 pikselden fazla yaklaşmasın.
>
> **Tipografi:** Tek bir gruptan sans-serif kullan (Inter, Manrope veya
> benzeri). Harf aralığı marka adında hafif açık, telefonda normal.
> Süslü, el yazısı ya da gölgeli yazı tipi kullanma.
>
> **İstemediklerim:** ikon kalabalığı, sosyal medya logoları, çerçeve
> içinde çerçeve, 3B efekt, filigran, stok fotoğraf öğesi.
>
> Bandı PNG olarak, arka planı saydam olmayacak biçimde ver. Yazıların
> hepsinin okunur ve tam olduğundan emin ol.

---

## 2. komut — bandı fotoğrafa eklemek

Birinci komutla bandı beğendikten sonra, her fotoğraf için bunu kullanın.
Fotoğrafı ve bandı birlikte yükleyin.

> Yüklediğim fotoğrafın altına, yine yüklediğim marka bandını ekle.
>
> **Kurallar:**
> - Çıktının tamamı (fotoğraf + bant) **4:3** oranında olsun. Bandı
>   eklemek için fotoğrafı alttan değil, gerekirse üstten ve alttan
>   dengeli biçimde kırp; insanların başı ve taşınan eşya kadraj dışında
>   kalmasın.
> - Bant fotoğrafın **üzerine binmesin**, altına eklensin.
> - Bandın yüksekliği toplam yüksekliğin %14,5'i olsun.
> - Bandı yeniden çizme, yeniden yazma, rengini ya da yazılarını
>   değiştirme. Verdiğim bandı olduğu gibi, yalnızca genişliğe göre
>   ölçekleyerek kullan.
> - Fotoğrafın rengine, kontrastına, netliğine dokunma. Filtre uygulama.
> - Çıktıyı 1400 piksel genişliğinde ver.
>
> Sonucu vermeden önce şunu kontrol et: bandın içindeki telefon numarası
> **0537 226 50 43** olarak, rakamları eksiksiz ve doğru sırada görünüyor
> mu? Görünmüyorsa baştan üret.

---

## Sonuç dosyalarını siteye koyarken

ChatGPT'den gelen fotoğrafları **`galeri-kaynak/` klasörüne koymayın** —
o klasördeki dosyalara `tools/cerceve.py` bandı bir kez daha ekler, iki
bant üst üste gelir.

Bandı dışarıda eklediyseniz dosyaları doğrudan
`assets/images/gallery/` altına, şu adlarla koyun:

    okur-nakliyat-galeri-08-600.webp
    okur-nakliyat-galeri-08-900.webp
    okur-nakliyat-galeri-08-1400.webp

Sonra `galeri-kaynak/liste.json` içindeki `fotograflar` dizisinin sonuna
kaydı ekleyin:

    { "no": 8, "aciklama": "Edremit'te yükleme öncesi hazırlanan araç" }

`no` numarası büyük olan fotoğraf sitede en başta görünür.

# ChatGPT Görsel Üretim Promptları

Bu dosya, Okur Nakliyat sitesinde **raster (fotoğraf/illüstrasyon) görsel gereken**
alanlar için hazırlanmış promptları içerir.

## Entegrasyon durumu

Bu ortamda **ChatGPT görsel üretim aracı veya API entegrasyonu bulunmamaktadır.**
Bu nedenle aşağıdaki promptlar hazırlanmış, ancak **görseller üretilmemiştir.**
İnternetten telifi belirsiz görsel indirilmemiş, sahte görsel oluşturulmamıştır.

Görseller üretildikten sonra izlenecek yol her promptun altında yazılıdır.

## Mevcut görsel envanteri

| Dosya | Tür | Ölçü | Boyut | Durum |
| --- | --- | --- | --- | --- |
| `assets/images/hero/okur-nakliyat-hero-background.webp` | Raster (WebP) | 1672 × 941 | 71,882 B | ✅ Uygun, kullanımda |
| `assets/images/hero/okur-nakliyat-hero.svg` | SVG illüstrasyon | 960 × 720 | 4,840 B | ⚠️ Raster ile değiştirilmeli (Prompt 1) |
| `assets/images/og/okur-nakliyat-og.svg` | SVG paylaşım görseli | 1200 × 630 | 2,549 B | ⚠️ Raster ile değiştirilmeli (Prompt 2) |
| `assets/images/logo/favicon.svg` | Logo / ikon | 64 × 64 | 331 B | ✅ Kural gereği SVG kalabilir |

> **SVG kuralı:** Bu denetim sırasında **yeni SVG illüstrasyon üretilmemiştir.**
> Yukarıdaki iki SVG, bu kural yürürlüğe girmeden önce oluşturulmuştu. Siteyi
> çalışır durumda tutmak için silinmediler; raster karşılıkları üretildiğinde
> değiştirilecekler. Arayüz ikonları (telefon, WhatsApp, konum, menü, onay)
> kural gereği inline SVG olarak kalmaya devam eder.

---

## Prompt 1 — Hero ön plan aracı

| Alan | Değer |
| --- | --- |
| Sayfa | Ana sayfa (`index.html`) |
| Bölüm | Hero (`#anasayfa`), sağ sütun `.hero-visual` |
| Önerilen dosya adı | `okur-nakliyat-hero-arac.webp` |
| Piksel ölçüsü | 1600 × 1200 |
| En-boy oranı | 4:3 (CSS'te `aspect-ratio: 4 / 3` ile kullanılıyor) |
| Kullanım | Masaüstünde sağ sütun, mobilde metnin altında tam genişlik |
| Şeffaflık | **Gerekli** — arka plan görselinin üzerine bineceği için PNG üretilip WebP'ye çevrilmeli |
| Mobil varyasyon | Gerekmiyor; aynı görsel `object-fit: contain` ile ölçekleniyor |
| Üretildi mi? | ❌ Hayır (entegrasyon yok) |
| WebP'ye çevrildi mi? | ❌ Hayır |
| Projeye entegre edildi mi? | ❌ Hayır |

**Prompt:**

> Create a high-quality, stylized 3/4 side-view illustration of a modern box truck
> (moving/removals truck) for a Turkish moving company website hero section.
>
> Purpose: foreground hero visual placed over a dark abstract background; it must
> read instantly as "professional home moving service".
>
> Composition: the truck occupies the lower-right two thirds of the frame, facing
> right, slightly angled three-quarter view. Leave the upper-left third visually
> empty and transparent for layout breathing room. Ground shadow soft and subtle,
> no ground plane or road drawn.
>
> Aspect ratio: 4:3, 1600 × 1200 pixels. Transparent background (alpha channel).
>
> Style: clean flat-vector look with soft shading and gentle gradients. Not
> photorealistic, not cartoonish, no outlines thicker than necessary. Premium and
> corporate, similar to modern SaaS product illustrations.
>
> Colors: cargo box in off-white (#F7F7F4) with a single yellow accent stripe
> (#F5C400); cab in yellow (#F5C400 to #FFD94A gradient); wheels, chassis and
> bumper in near-black (#0B0B0B / #151515); glass in dark blue-grey. No other hues.
>
> Must NOT include: any text, lettering, numbers, license plates, watermarks,
> logos, brand marks, people, buildings, trees, road markings, speed lines,
> sky, or background scenery. No drop shadows on a solid background.
>
> Safe area: keep the truck fully inside the middle 90% of the frame so that
> cropping on small screens never cuts the cab or wheels.

**Üretildikten sonra yapılacaklar:**

1. PNG olarak indir (şeffaflık korunmalı).
2. WebP'ye çevir: `python3 -c "from PIL import Image; im=Image.open('kaynak.png'); im.save('assets/images/hero/okur-nakliyat-hero-arac.webp','WEBP',quality=90,method=6,lossless=False)"`
   (şeffaflık için `im.convert('RGBA')` kullan, `RGB`'ye çevirme).
3. `index.html` içindeki `.hero-visual-image` `src` değerini yeni dosyaya çevir.
4. `width` / `height` değerlerini `1600` / `1200` yap.
5. `assets/images/hero/okur-nakliyat-hero.svg` dosyasını sil.
6. `Site kontrolü` iş akışını çalıştırıp 200 döndüğünü doğrula.

---

## Prompt 2 — Sosyal medya paylaşım görseli (Open Graph)

| Alan | Değer |
| --- | --- |
| Sayfa | Ana sayfa (`index.html`) `<head>` |
| Bölüm | `og:image` / `twitter:image` |
| Önerilen dosya adı | `okur-nakliyat-og.jpg` |
| Piksel ölçüsü | 1200 × 630 |
| En-boy oranı | 1.91:1 |
| Kullanım | WhatsApp, Facebook, X, LinkedIn önizlemesi |
| Şeffaflık | Gerekmiyor |
| Mobil varyasyon | Gerekmiyor |
| Üretildi mi? | ❌ Hayır (entegrasyon yok) |
| WebP'ye çevrildi mi? | ❌ Hayır — **bu görsel WebP olmamalı** |
| Projeye entegre edildi mi? | ❌ Hayır |

> **Önemli:** Open Graph görselleri için **JPG veya PNG kullanılmalıdır.** Birçok
> sosyal platform WebP ve SVG önizlemelerini desteklemez. Bu tek istisnadır;
> sitenin geri kalanında WebP tercih edilir.

**Prompt:**

> Create a social sharing preview image for a Turkish moving company called
> "Okur Nakliyat", based in Edremit, serving all of Türkiye.
>
> Purpose: link preview card shown in WhatsApp, Facebook and X when the website
> is shared. It must look professional and trustworthy at small sizes.
>
> Aspect ratio: 1.91:1, exactly 1200 × 630 pixels.
>
> Composition: dark, premium background. A stylized yellow moving truck on the
> right third, seen from a three-quarter side angle. The left two thirds stay
> visually calm and dark so that text can be overlaid later by the designer.
> A very subtle abstract route line arcs from lower-left to the truck.
>
> Style: modern, corporate, clean. Soft lighting, no heavy gradients, no neon
> glow, no lens flare.
>
> Colors: background near-black (#0B0B0B) to dark anthracite (#151515); truck in
> brand yellow (#F5C400) with off-white cargo box; accents in the same yellow at
> low opacity. No other hues.
>
> Must NOT include: any text, lettering, numbers, watermarks, logos, brand marks,
> people, or photographic elements.
>
> Safe area: keep all meaningful content inside the central 85% of the frame,
> because some platforms crop the edges.

**Üretildikten sonra yapılacaklar:**

1. JPG olarak `assets/images/og/okur-nakliyat-og.jpg` yoluna kaydet (kalite ~85).
2. `index.html` içindeki `og:image` ve `twitter:image` değerlerini güncelle
   (mutlak URL: `https://okurnakliyatedremit.com/assets/images/og/okur-nakliyat-og.jpg`).
3. JSON-LD içindeki `image` alanını da güncelle.
4. `assets/images/og/okur-nakliyat-og.svg` dosyasını sil.
5. Önizlemeyi doğrula: WhatsApp'ta linki kendine gönder veya
   `https://www.opengraph.xyz` üzerinden kontrol et.

---

## Sonraki bölümler için not

Hizmetler, hakkımızda, süreç, SSS ve iletişim bölümleri **henüz oluşturulmadı.**
Bu bölümler yazıldığında görsel ihtiyaçları netleşecek ve bu dosyaya yeni promptlar
eklenecek. Şu an var olmayan bölümler için önden prompt üretilmemiştir; çünkü
görselin en-boy oranı ve kırpma davranışı ancak bölümün düzeni belirlendikten
sonra doğru tanımlanabilir.

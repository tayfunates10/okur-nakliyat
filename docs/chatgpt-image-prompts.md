# ChatGPT Görsel Üretim Promptları

Bu dosya, Okur Nakliyat sitesinde **raster (fotoğraf/illüstrasyon) görsel gereken**
alanlar için hazırlanmış promptları içerir.

## Entegrasyon durumu

Bu ortamda **ChatGPT görsel üretim aracı veya API entegrasyonu bulunmamaktadır.**
Bu nedenle aşağıdaki promptlar hazırlanmış, ancak **görseller üretilmemiştir.**
İnternetten telifi belirsiz görsel indirilmemiş, sahte görsel oluşturulmamıştır.

Görseller üretildikten sonra izlenecek yol her promptun altında yazılıdır.

## Mevcut görsel envanteri

**Dosya olarak duran görseller**

| Dosya | Tür | Ölçü | Boyut | Durum |
| --- | --- | --- | --- | --- |
| `assets/images/hero/okur-nakliyat-hero-background.webp` | Raster (WebP) | 1672 × 941 | 71.882 B | ✅ Uygun, kullanımda (hero arka planı) |
| `assets/images/hero/okur-nakliyat-hero.svg` | SVG illüstrasyon | 960 × 720 | 4.840 B | ⚠️ Raster ile değiştirilmeli (Prompt 1) |
| `assets/images/og/okur-nakliyat-og.svg` | SVG paylaşım görseli | 1200 × 630 | 2.549 B | ⚠️ Raster ile değiştirilmeli (Prompt 2) |
| `assets/images/logo/favicon.svg` | Logo / ikon | 64 × 64 | 331 B | ✅ Kural gereği SVG kalabilir |

**`index.html` içine gömülü (inline) illüstrasyonlar**

| Konum | viewBox | Rol | Durum |
| --- | --- | --- | --- |
| `.about-scene` (`#hakkimizda`) | 640 × 680 | Taşıma sahnesi illüstrasyonu | ⚠️ Raster ile değiştirilebilir (Prompt 3) |
| `.coverage-map` (hizmet bölgesi) | 820 × 390 | Dekoratif Türkiye haritası + güzergâh noktaları | ℹ️ Vektör kalması tercih edildi — gerekçe aşağıda |
| Arayüz ikonları (telefon, WhatsApp, konum, menü, ok, onay, hizmet kartı ikonları) | çeşitli | İkon | ✅ Kural gereği inline SVG kalır |

> **SVG kuralına uyum — dürüst durum bildirimi:** Bu denetim çalışmasında
> **yeni SVG illüstrasyon, arka plan veya dekorasyon üretilmemiştir.** Yukarıda
> listelenen SVG'lerin tamamı bu kural yürürlüğe girmeden önce, sayfanın
> tasarım aşamasında oluşturulmuştu. Siteyi çalışır durumda tutmak için
> silinmediler; raster karşılıkları için aşağıya prompt hazırlanmıştır.
>
> `.coverage-map` için raster prompt hazırlanmadı: bu öğe bir *harita*dır,
> illüstrasyon değildir. Rasterleştirilirse 2560 px'lik ekranlarda kenarları
> bozulur ve `aria-hidden` dekoratif rolüne kıyasla gereksiz ağırlık getirir.
> Bu, bilinçli bir tercihtir; kullanıcı aksini isterse prompt eklenebilir.

---

## Prompt 1 — Hero ön plan aracı

| Alan | Değer |
| --- | --- |
| Sayfa | Ana sayfa (`index.html`) |
| Bölüm | Hero (`#anasayfa`), sağ sütun `.hero-visual` |
| Önerilen dosya adı | `okur-nakliyat-hero-arac.webp` |
| Piksel ölçüsü | 1600 × 1200 |
| En-boy oranı | 4:3 — mevcut `okur-nakliyat-hero.svg` dosyasının `960 × 720` oranıyla aynı; `index.html` içindeki `width`/`height` bu orana göre yazılı |
| Kullanım | Masaüstünde sağ sütun, 960 px altında metnin altında ortalanmış; `width: min(780px, 126%)` ile ölçekleniyor |
| Şeffaflık | **Gerekli** — hero arka plan görselinin üzerine bineceği için PNG üretilip WebP'ye çevrilmeli |
| Mobil varyasyon | Gerekmiyor; aynı görsel genişlik kuralıyla ölçekleniyor |
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

## Prompt 3 — Hakkımızda bölümü görseli

| Alan | Değer |
| --- | --- |
| Sayfa | Ana sayfa (`index.html`) |
| Bölüm | Hakkımızda (`#hakkimizda`), sol sütun `.about-visual` → `.about-scene` |
| Önerilen dosya adı | `okur-nakliyat-hakkimizda.webp` |
| Piksel ölçüsü | 1280 × 1360 |
| En-boy oranı | 32:34 (mevcut inline SVG'nin `viewBox` oranı: 640 × 680) |
| Kullanım | Masaüstünde sol sütun, 960 px altında metnin üstünde ortalanmış, `width: min(100%, 670px)` |
| Şeffaflık | Gerekmiyor — kendi koyu zemini olabilir, köşeler CSS'te `border-radius` ile yuvarlanıyor |
| Mobil varyasyon | Gerekmiyor |
| Üretildi mi? | ❌ Hayır (entegrasyon yok) |
| WebP'ye çevrildi mi? | ❌ Hayır |
| Projeye entegre edildi mi? | ❌ Hayır |

**Prompt:**

> Create a portrait-orientation illustration for the "About us" section of a
> Turkish moving company website.
>
> Purpose: it must communicate careful, planned household moving — two movers
> carrying a packed box together, calm and professional, not rushed.
>
> Aspect ratio: portrait, exactly 1280 × 1360 pixels.
>
> Composition: two stylized figures seen from the front, standing on either side
> of a single cardboard moving box they carry between them at waist height. The
> pair is centered horizontally and sits in the lower two thirds of the frame.
> The upper third stays calm and uncluttered. Background is a soft dark panel
> with generous padding around the figures.
>
> Style: clean flat-vector look with soft shading and gentle gradients. Not
> photorealistic, not cartoonish. Faces simplified with no detailed features.
> Premium and corporate, similar to modern SaaS product illustrations.
>
> Colors: background near-black (#181818) with a slightly lighter inner panel
> (#222222); one figure in brand yellow (#F5C400), the other in off-white
> (#E8E8E3); the box in brand yellow with near-black (#0B0B0B) strapping lines.
> Small yellow accent marks in the corners. No other hues.
>
> Must NOT include: any text, lettering, numbers, watermarks, logos, brand marks,
> furniture, trucks, rooms, windows, floors, or photographic elements.
>
> Safe area: keep both figures and the box fully inside the middle 85% of the
> frame; the section crops the edges on narrow screens.

**Üretildikten sonra yapılacaklar:**

1. PNG olarak indir.
2. WebP'ye çevir:
   `python3 -c "from PIL import Image; im=Image.open('kaynak.png'); im.save('assets/images/hero/okur-nakliyat-hakkimizda.webp','WEBP',quality=88,method=6)"`
3. `index.html` içindeki `.about-scene` `<div>`'inin **tamamını** (içindeki inline
   `<svg>` dahil) şu satırla değiştir:
   `<img class="about-scene-image" src="assets/images/hero/okur-nakliyat-hakkimizda.webp" width="1280" height="1360" alt="" loading="lazy" decoding="async">`
4. `assets/css/style.css` içinde `.about-scene` kuralına karşılık gelen
   `.about-scene-image { width: 100%; height: auto; border-radius: var(--radius-lg); }`
   kuralını ekle.
5. `npm run test:responsive` çalıştırıp oran bozulması (`dist`) sayısının 0
   kaldığını doğrula.

---

## Not

Ana sayfanın bütün bölümleri (hizmetler, hakkımızda, süreç, hizmet bölgesi, SSS,
teklif formu, CTA, footer) tamamlanmış durumdadır. Bu bölümlerin görsel
ihtiyaçları yukarıdaki üç promptla karşılanmaktadır; geri kalan görsel öğeler
arayüz ikonu olduğu için kural gereği inline SVG kalmaya devam eder.

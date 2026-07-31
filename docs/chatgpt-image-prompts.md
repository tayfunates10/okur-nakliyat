# ChatGPT Görsel Üretim Promptları

Bu dosya, Okur Nakliyat sitesinde **raster (fotoğraf/illüstrasyon) görsel gereken**
alanlar için hazırlanmış promptları içerir.

## Entegrasyon durumu

Bu ortamda ChatGPT görsel üretim aracı veya API entegrasyonu **bulunmamaktadır**;
görseller Claude tarafından üretilmemiştir. Aşağıdaki promptlar hazırlanmış,
**kullanıcı bunları kendi ChatGPT hesabında çalıştırıp üretilen üç görseli
projeye sağlamıştır.** Claude bu görselleri dönüştürüp entegre etmiş ve
ölçümle doğrulamıştır.

İnternetten telifi belirsiz görsel indirilmemiş, sahte görsel oluşturulmamıştır.

| Prompt | Üretildi mi? | Dönüştürüldü mü? | Entegre edildi mi? |
| --- | --- | --- | --- |
| 1 — Hero ön plan aracı | ✅ Kullanıcı üretti | ✅ WebP (şeffaflık korundu) + 900px varyant | ✅ `srcset` ile |
| 2 — Open Graph görseli | ✅ Kullanıcı üretti | ✅ 1200×630 JPG | ✅ `og:image`, `twitter:image`, JSON-LD |
| 3 — Hakkımızda görseli | ✅ Kullanıcı üretti | ✅ WebP | ✅ inline SVG'nin yerine |
| 4 — Hizmet bölgesi haritası | ✅ Kullanıcı üretti | ✅ Kırpma + renk düzeltmesi + WebP, 2 varyant | ✅ `srcset` ile, inline SVG'nin yerine |

## Mevcut görsel envanteri

**Dosya olarak duran görseller**

| Dosya | Tür | Ölçü | Boyut | Durum |
| --- | --- | --- | --- | --- |
| `assets/images/hero/okur-nakliyat-hero-background.webp` | Raster (WebP) | 1672 × 941 | 71,9 KB | ✅ Hero arka planı |
| `assets/images/hero/okur-nakliyat-hero-arac.webp` | Raster (WebP, şeffaf) | 1536 × 1024 | 117,8 KB | ✅ Hero ön planı (retina) |
| `assets/images/hero/okur-nakliyat-hero-arac-900.webp` | Raster (WebP, şeffaf) | 900 × 600 | 44,5 KB | ✅ `srcset` mobil varyantı |
| `assets/images/about/okur-nakliyat-hakkimizda.webp` | Raster (WebP) | 1217 × 1293 | 34,4 KB | ✅ Hakkımızda bölümü |
| `assets/images/og/okur-nakliyat-og.jpg` | Raster (JPG) | 1200 × 630 | 57,5 KB | ✅ Paylaşım görseli |
| `assets/images/coverage/okur-nakliyat-hizmet-bolgesi-1300.webp` | Raster (WebP, şeffaf) | 1300 × 618 | 137,3 KB | ✅ Hizmet bölgesi (masaüstü) |
| `assets/images/coverage/okur-nakliyat-hizmet-bolgesi-900.webp` | Raster (WebP, şeffaf) | 900 × 428 | 71,9 KB | ✅ `srcset` mobil varyantı |
| `assets/images/logo/favicon.svg` | Logo / ikon | 64 × 64 | 331 B | ✅ Kural gereği SVG kalabilir |

Prompt 1 ve 2 ile değiştirilen `okur-nakliyat-hero.svg` ve `okur-nakliyat-og.svg`
dosyaları **silinmiştir**.

**`index.html` içine gömülü (inline) illüstrasyonlar**

| Konum | viewBox | Rol | Durum |
| --- | --- | --- | --- |
| `.about-scene` (`#hakkimizda`) | — | Taşıma sahnesi illüstrasyonu | ✅ **Raster ile değiştirildi** (Prompt 3) |
| `.coverage-map` (hizmet bölgesi) | — | Türkiye haritası + güzergâh noktaları | ✅ **Raster ile değiştirildi** (Prompt 4) |
| Arayüz ikonları (telefon, WhatsApp, konum, menü, ok, onay, hizmet kartı ikonları) | çeşitli | İkon | ✅ Kural gereği inline SVG kalır |

> **SVG kuralına uyum — dürüst durum bildirimi:** Bu denetim çalışmasında
> **yeni SVG illüstrasyon, arka plan veya dekorasyon üretilmemiştir.** Yukarıda
> listelenen SVG'lerin tamamı bu kural yürürlüğe girmeden önce, sayfanın
> tasarım aşamasında oluşturulmuştu. Siteyi çalışır durumda tutmak için
> silinmediler; raster karşılıkları için aşağıya prompt hazırlanmıştır.
>
> `.coverage-map` için başlangıçta prompt hazırlanmamıştı — bu öğe bir
> *harita*dır ve rasterleştirilmesi büyük ekranlarda kenar kalitesi açısından
> risklidir. Kullanıcı talebi üzerine **Prompt 4** eklendi; oradaki uyarı
> notu bu riski ayrıntılandırıyor.

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
| Üretildi mi? | ✅ Evet — kullanıcı ChatGPT'de üretti |
| WebP'ye çevrildi mi? | ✅ Evet |
| Projeye entegre edildi mi? | ✅ Evet |

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
| Üretildi mi? | ✅ Evet — kullanıcı ChatGPT'de üretti |
| WebP'ye çevrildi mi? | ✅ JPG'ye çevrildi (bu görsel WebP olmamalı) |
| Projeye entegre edildi mi? | ✅ Evet |

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
| Üretildi mi? | ✅ Evet — kullanıcı ChatGPT'de üretti |
| WebP'ye çevrildi mi? | ✅ Evet |
| Projeye entegre edildi mi? | ✅ Evet |

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

## Prompt 4 — Hizmet bölgesi haritası

| Alan | Değer |
| --- | --- |
| Sayfa | Ana sayfa (`index.html`) |
| Bölüm | Hizmet bölgemiz — sağ sütun `.coverage-map` |
| Önerilen dosya adı | `okur-nakliyat-hizmet-bolgesi.webp` |
| Piksel ölçüsü | **1640 × 780** (2:1 çıktı da kabul edilir, uyarlanır) |
| En-boy oranı | 2,103:1 — mevcut `viewBox 820 × 390` ile aynı |
| Kullanım | Masaüstünde sağ sütun (821 × 391 CSS px), 1080 px altında tam genişlik, 720 px altında iki kenardan 16 px taşacak şekilde |
| Zemin | **Bölümün zemini marka sarısı `#F5C400`** — görsel şeffaf olmalı |
| Şeffaflık | **Zorunlu** — PNG olarak üretilip WebP'ye çevrilecek |
| Mobil varyasyon | Gerekmiyor |

> **Bu prompt diğerlerinden riskli.** Görsel üretim modelleri ülke sınırlarını
> güvenilir biçimde çizemez; Türkiye'nin kıyı şeridi çoğu zaman bozuk çıkar.
> Nakliyat sitesinde yanlış görünen bir Türkiye haritası, mevcut soyut
> silüetten daha kötüdür. Bu yüzden prompt **coğrafi doğruluk değil, stilize
> silüet** istiyor. Gelen görsel Türkiye gibi durmuyorsa entegre edilmemeli;
> o durumda doğru kaynak görsel üretimi değil, kamuya açık coğrafi veridir.

**Prompt:**

> Create a stylized, minimal map illustration for the "service area" section of
> a Turkish moving company website.
>
> Aspect ratio: 2.1:1, 1640 x 780 pixels. **Transparent background (alpha
> channel) — the artwork will be placed on a solid yellow section, so no
> background fill of any kind.**
>
> Subject: a single simplified silhouette of Turkiye, drawn as one solid shape.
> Smooth, softened coastline — a clean graphic abstraction, not a precise
> cartographic outline. No neighbouring countries, no borders, no water, no
> grid, no compass, no legend.
>
> On the silhouette: nine small filled circles marking cities, and three
> gently curved dashed connection lines that all radiate from one point in the
> left third of the shape toward points to the right. Around that same origin
> point, two thin concentric rings.
>
> Critical: every circle, dashed line and ring must sit **entirely inside** the
> dark silhouette. Nothing may extend past its edge, because outside the
> silhouette the background is transparent and yellow marks would disappear
> against the yellow section.
>
> Colors: silhouette in near-black (#101010). Circles, dashed lines and rings
> in brand yellow (#F5C400); the rings at low opacity. No other colors, no
> gradients, no glow, no drop shadow.
>
> Style: flat vector look, clean edges, generous negative space. Calm and
> corporate.
>
> Must NOT include: any text, letters, city names, numbers, watermarks, logos,
> brand marks, pins with tails, photographic elements, 3D effects, or a
> background rectangle.
>
> Safe area: keep the silhouette within the central 92% of the frame.

**Sonuç — yapılanlar:**

Gelen görsel 1536 × 1024 şeffaf PNG idi. Üzerinde üç işlem yapıldı:

1. **Kırpma.** Silüetin gerçek sınırı `alfa > 128` maskesiyle bulundu
   (1045 × 395, oran 2,646). Slotun oranı 2,103 olduğu için silüet merkezine
   göre %6 pay bırakılarak 2,101 oranında kırpıldı.
2. **Renk düzeltmesi.** Üretilen görselin karası `#303030`, sarısı `#F0D010`
   idi; hedef `#101010` ve `#F5C400`. Her piksel koyu→sarı ekseni üzerine
   izdüşürülüp iki hedef renk arasında harmanlandı — böylece kenar yumuşatması
   korundu. İç alanlar tam düz renge sabitlendi (t < 0,15 → koyu, t > 0,85 →
   sarı); bu, kayıpsız WebP boyutunu 355 → 198 KB'a indirdi.
3. **Çözünürlük seçimi.** 1640 px (2×) sürüm 196 KB idi. 1640 · 1300 · 1100 ·
   900 px sürümleri gerçek görüntüleme boyutunda (821 CSS px, 2× ekran) render
   edilip 1640 ile piksel piksel karşılaştırıldı: 900 px'te bile ortalama fark
   yalnızca **1,10/255**, farkın tamamı kıyı çizgisi kenarlarında. Bu yüzden
   `srcset` ile 900w + 1300w sunuluyor.

Ayrıca **"EDREMİT" etiketi görselin içinde değil, HTML'de.** Görsele gömülü
yazı ölçeklenince bozulur ve ekran okuyucu okuyamaz. Etiket kendi koyu zeminini
taşıyor (`#101010`): harita üzerinde görünmez, bir şehir noktasının veya sarı
zeminin üstüne denk gelirse okunurluğu korur.

**Genel yönerge — bir sonraki görsel için:**

1. **Şeffaflığı koruyarak** PNG indir.
2. Claude'a gönder; dönüşüm ve entegrasyon Claude tarafından yapılacak:
   - WebP'ye çevrilir (alfa korunur), 2× retina için 1640 px genişlikte kalır.
   - `index.html` içindeki inline `<svg>` bloğu `<img>` ile değiştirilir.
   - `.coverage-map svg` kuralları `.coverage-map img` olarak güncellenir;
     `width: 112%` ve `transform: translateX(-2%)` bleed davranışı korunur.
   - Mevcut SVG'deki **"EDREMİT" yazısı** görselin içinde olmayacağı için
     HTML'e taşınır — bu erişilebilirlik açısından da doğrusudur.
   - 19 senaryoda oran bozulması ve taşma yeniden ölçülür.

---

## Not

Ana sayfanın bütün bölümleri (hizmetler, hakkımızda, süreç, hizmet bölgesi, SSS,
teklif formu, CTA, footer) tamamlanmış durumdadır. Bu bölümlerin görsel
ihtiyaçları yukarıdaki üç promptla karşılanmaktadır; geri kalan görsel öğeler
arayüz ikonu olduğu için kural gereği inline SVG kalmaya devam eder.

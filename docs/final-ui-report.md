# Final UI Raporu — Okur Nakliyat

**Tarih:** 30 Temmuz 2026
**Kapsam:** `index.html` ve `404.html` üzerinde responsive/UI denetimi,
düzeltmeler ve ölçümle doğrulama

---

## 1. Genel sonuç

Proje **saf statik bir sitedir**: HTML5 + CSS3 + vanilla JavaScript. Framework,
derleme adımı veya TypeScript yoktur. Depoya bu çalışmada eklenen `package.json`
**yalnızca geliştirme/test aracı** içindir (Playwright); site çalışma zamanında
hiçbir pakete bağlı değildir ve sunucuya yalnızca statik dosyalar gönderilir.

| | |
| --- | --- |
| Görevin genel durumu | Uygulanabilir tüm aşamalar tamamlandı |
| İncelenen sayfa sayısı | 2 (`index.html`, `404.html` — sitedeki tüm sayfalar) |
| İncelenen bölüm sayısı | 9 (hero, hizmetler, hakkımızda, süreç, hizmet bölgesi, SSS, teklif formu, CTA, footer) |
| Test edilen viewport | 16 cihaz ölçüsü + 3 yatay senaryo + 29 ara genişlik + 5 çentik simülasyonu; `404.html` için ayrıca 13 ölçü |
| Değiştirilen dosya sayısı | 5 (`style.css`, `variables.css`, `components.css`, `index.html`, `404.html`) |
| Oluşturulan dosya sayısı | 4 (`tests/responsive-audit.js`, `package.json`, `docs/` altındaki 3 rapor) |
| Düzeltilen ölçülmüş kusur | 11 |
| Uygulanan iyileştirme | 2 |

---

## 2. Yapılan değişiklikler

### Yerleşim ve taşma düzeltmeleri

- **Grid izlerinin taşma koruması:** Dar ekranda tek sütuna inen bütün grid'ler
  `1fr` yerine `minmax(0, 1fr)` kullanıyor (9 kural). `1.35fr 1fr 1fr` ve
  `1.45fr repeat(3, …)` izleri de `minmax(0, …)` ile sarıldı. Bu, bir alt öğenin
  min-content genişliğiyle kapsayıcıyı patlatmasını yapısal olarak engelliyor.
- **Düğme metni:** `@media (max-width: 440px)` içinde `.btn { white-space: normal }`
  ve `.btn-lg { padding-inline: 1.25rem }`. 320 px'de teklif formunu 39 px
  taşıran kök neden buydu.
- **Hero şerit payı:** `.hero-inner` alt boşluğu 72 px'lik `.hero-service-rail`
  payını kalıcı olarak taşıyor; şerit artık hero içeriğinin üzerine binmiyor.

### Güvenli alan (safe area) desteği

Projede tek bir `env(safe-area-inset-*)` kullanımı yoktu. Her iki sayfanın
viewport etiketine `viewport-fit=cover` eklendi ve kenara oturan yedi bileşene
güvenli alan payı verildi: `.container` (yatay), `.site-header` (üst),
`.mobile-menu`, `.mobile-contact-bar` (dört kenar), `.skip-link`, mobil
`.site-footer` (alt) ve `scroll-padding-top`. Tasarım payı ile cihaz payından
büyüğü seçildiği için (`max(...)`) çentiksiz cihazlarda hiçbir değer değişmez —
19 senaryoluk denetim değişiklikten önce ve sonra birebir aynı sonucu verdi.

### Yükseklik ve viewport davranışı

- **Yatay ekran kuralı eklendi:**
  `@media (orientation: landscape) and (max-height: 560px) and (min-width: 640px)`
  — iki sütunlu düzene dönüş, sıkılaştırılmış dikey ritim, 260 px görsel
  yüksekliği, `clamp(1.6rem, 4vw, 2.35rem)` başlık ölçeği.
- **Footer alt boşluğu** sabit mobil iletişim çubuğunun görünmediği
  genişliklerde `clamp(2.5rem, 4vw, 3.5rem)`'e indirildi.
- **`404.html`** yatay tutulan telefonda dikey taşıyordu (844×390'da 465 px
  içerik). "404" rakamı ve başlık artık yüksekliği de hesaba katıyor
  (`min(24vw, 26vh)` / `min(7vw, 9vh)`), dikey boşluklar kısa ekranlarda
  daralıyor. 13 ölçünün tamamında kaydırma kalmadı.

### Container ve tipografi

- `--container-gutter` → `clamp(32px, 4.5vw, 48px)`; 767 px'deki 32→40 px
  sıçraması kaldırıldı. Sağ-sol boşluk 320–2560 px arasında simetrik ve kademesiz.
- `--fs-display` → `clamp(2.125rem, 8.5vw, 3.75rem)`. **Dürüst not:** 720 px
  altında `.hero-title` kendi kuralını (`clamp(2.85rem, 13vw, 4.3rem)`)
  kullandığı için bu değişken o aralıkta devrede değildir.
- `.hero-title-line` kırpma kutusu `padding-bottom: 0.16em` +
  `margin-bottom: -0.16em` ile büyütüldü; **ğ, y, ı** harflerinin ve virgülün
  kesilmesi giderildi. Maske büyüdüğü için `heroTitleReveal` başlangıcı
  `104% → 122%` yapıldı.

### Bileşen düzeltmeleri

- **SSS akordeonu:** `.faq-answer p` alt boşluğu `padding` yerine
  `::after { height }` ile akışa alındı; kapalı durumda satır başına 21,6 px'lik
  ölü şerit kalktı.
- **Hero hizmet şeridi:** 720 px altında kaydırılabilir olduğunu gösteren sağ
  kenar geçişi (`.hero-service-rail::after`) eklendi.

### Buton düzenlemeleri

`.btn` ailesi zaten `min-height: var(--tap-target)` (44 px) kullanıyordu ve
normal / hover / `focus-visible` / active / disabled durumları tanımlıydı.
Yalnızca 440 px altındaki `white-space` ve `padding-inline` değerleri
değiştirildi; renk, yarıçap veya gölge değerlerine dokunulmadı.

### Form denetimi

Teklif formu (`#quoteForm`) incelendi:

- Her alanın `<label>` bağlantısı var; `required`, `type`, `inputmode`,
  `autocomplete` ve `pattern` değerleri tanımlı.
- `input`, `select`, `textarea` yükseklikleri 44 px eşiğinin üzerinde
  (ölçüldü: 0 küçük hedef).
- Gönderim `checkValidity()` ile doğrulanıp `reportValidity()` ile geri
  bildiriliyor; JavaScript kapalıyken form varsayılan davranışına düşer.
- Tarih alanının `min` değeri bugüne ayarlanıyor.
- 320 px'de alanların taşması **1. maddedeki düzeltmeyle** giderildi.

Düzeltme gerektiren başka bulgu çıkmadı.

### Erişilebilirlik düzenlemeleri

- 44 px altındaki **20 dokunma hedefi** (masaüstü) / **19** (mobil) düzeltildi:
  `.header-phone`, `.service-link` ×6, `.text-action` ×2, footer bağlantıları ×11.
- Alt çizgili bağlantılarda ek yükseklik `align-items: flex-end` ile metnin
  üstüne verildi; böylece alt çizgi metne yapışık ve **tek parça** kaldı.
  (İlk denemede `text-decoration` kullanıldı, ancak flex öğeleri arasında
  çizgiyi parçaladığı için geri alındı — ekran görüntüsüyle doğrulandı.)
- Önceki adımda eklenen `.skip-link`, `.brand`, `.nav-link` 44 px kuralları
  yürürlükte.
- **İsimsiz klavye durağı giderildi:** dar ekranda kaydırılabilir olan hizmet
  şeridini Chrome kendiliğinden sekme durağı yapıyordu, ancak öğe isimsizdi ve
  odak halkası yoktu. `aria-label` rolsüz dış `div`'den kaydırma yapan iç öğeye
  taşındı, `role="group"` ve `:focus-visible` çerçevesi eklendi.
- Teklif formundaki adres alanlarına `autocomplete="address-level2"` eklendi.

### Animasyon düzenlemeleri

- `prefers-reduced-motion` desteği doğrulandı: sonsuz animasyonlar ve parallax
  devre dışı kalıyor, içerik son konumunda görünür kalıyor.
- Tüm animasyonlar `transform` ve `opacity` üzerinden çalışıyor; layout
  özelliği animasyonu yok.
- `heroTitleReveal` başlangıç konumu maske değişikliğine göre güncellendi.

### JavaScript incelemesi

`assets/js/main.js` içindeki dokuz fonksiyon okundu. **Düzeltme gerektiren
sorun bulunmadı:**

- Scroll dinleyicisi `requestAnimationFrame` ile sınırlandırılmış ve `passive: true`.
- `resize` dinleyicisi yok; yerine `matchMedia` change dinleyicisi kullanılmış.
- Yumuşak kaydırma tek bir delege dinleyiciyle çalışıyor (dinleyici çoğalması yok).
- Parallax yalnızca `pointer: fine` ve hareket izni varken bağlanıyor.
- Mobil menüde odak tuzağı, ESC, overlay tıklaması ve gövde kaydırma kilidi var.
- SSS akordeonu `<details>` üzerine kurulu — JavaScript kapalıyken de çalışır.
- `console.log` veya kullanılmayan kod yok.

### Performans

- **İlk boyamayı bloklayan Google Fonts stil sayfası düzeltildi.** Ölçüm:
  FCP ve LCP **mobilde 13.016 ms, masaüstünde 12.776 ms** iken `domInteractive`
  yalnızca 15–72 ms idi — DOM anında hazırdı, ancak tarayıcı bloklayan stil
  sayfası çözülene kadar tek piksel boyamıyordu. `display=swap` yalnızca yazı
  tipi *dosyasını* ilgilendirir; *stil sayfası* bloklayıcıdır. Bloklamayan
  yüklemeye geçildi (`preload as=style` + `media="print"` / `onload` +
  `<noscript>` yedeği). Sonuç: **FCP/LCP mobilde 152 ms, masaüstünde 240 ms** —
  aynı koşulda yaklaşık **85 kat** iyileşme. Düzen değişmedi (ekran
  görüntüsüyle doğrulandı), CLS 0 / 0,001 seviyesinde kaldı.
- Hero arka planı `<link rel="preload" as="image" fetchpriority="high">` ile
  önceden yükleniyor (LCP kaynağı).
- `.htaccess` üzerinden gzip/brotli; statik dosyalar için 1 yıllık `immutable`
  önbellek, HTML için `no-cache` — canlıda yanıt başlıklarıyla doğrulanmıştı.
- CSS ve JavaScript sürgüsü `?v=3 → ?v=7` yapıldı; yayına alındığında eski
  CSS önbellekten servis edilmeyecek.

---

## 3. Test sonuçları

| Test | Sonuç | Not |
| --- | --- | --- |
| Build | **Çalıştırılamadı** | Projede derleme sistemi yok (saf statik site) |
| Lint | **Çalıştırılamadı** | Lint yapılandırması yok |
| Typecheck | **Çalıştırılamadı** | TypeScript kullanılmıyor |
| Unit test | **Çalıştırılamadı** | Birim test altyapısı yok |
| E2E / responsive denetimi | **Başarılı** | `npm run test:responsive` — 16 viewport + 3 landscape + 29 ara genişlik |
| `404.html` responsive testi | **Başarılı** | 13 ölçü; kaydırma, taşma, kesilme yok |
| Güvenli alan (çentik) testi | **Başarılı** | 5 senaryo, `env()` gerçek iPhone paylarıyla değiştirilerek |
| Kırık çapa / bağlantı testi | **Başarılı** | 34 iç çapanın tamamının hedefi mevcut |
| Başlık hiyerarşisi | **Başarılı** | Tek `h1`, 26 başlıkta seviye atlaması yok |
| Klavye odak testi | **Başarılı** | Skip-link, sekme sırası, mobil menü odak tuzağı ve ESC, SSS klavye ile açılış |
| iOS Safari zoom eşiği | **Başarılı** | Yedi form denetiminin tamamı 16 px |
| Yatay taşma testi | **Başarılı** | 320–2560 px arası hiçbir noktada taşma yok |
| Dokunma hedefi testi | **Başarılı** | 19 senaryonun tamamında 0 |
| Metin kesilme testi | **Başarılı** | Gerçek kesilme 0; kalan uyarılar dekoratif öğelerden |
| Öğe çakışması testi | **Başarılı** | 0 |
| Görsel oran testi | **Başarılı** | `naturalWidth > 0`, oran bozulması 0 |
| Console error testi | **Başarılı\*** | Site kaynaklı hata yok |
| Kırık asset testi | **Başarılı** | 404 yok |
| Landscape görünüm | **Başarılı** | 844×390, 932×430, 667×375 |
| Formlar | **Başarılı** | Teklif formu 320 px dahil tüm ölçülerde kapsayıcı içinde |
| Mobil menü | **Başarılı** | Açılma, ESC, overlay, kaydırma kilidi, odak panele giriş ve düğmeye dönüş |
| Lighthouse | **Çalıştırılamadı** | Ortamda Lighthouse CLI yok, dış ağ erişimi beyaz listeyle sınırlı |
| Core Web Vitals (doğrudan ölçüm) | **Başarılı** | `PerformanceObserver` ile LCP ve CLS ölçüldü — aşağıdaki tablo |
| Kullanılmayan CSS taraması | **Başarılı** | 380 kural tarandı; gerçekten ölü kural 2 (bkz. bölüm 8) |
| Otomatik a11y taraması (axe) | **Çalıştırılamadı** | Paket ortamda kurulu değil, dış ağ erişimi sınırlı |
| Erişilebilirlik (elle) | **Kısmen başarılı** | Dokunma hedefi, başlık sırası, ARIA, odak yönetimi kontrol edildi |
| Gerçek cihaz testi | **Çalıştırılamadı** | Ortamda fiziksel cihaz yok — çentik davranışı simülasyonla doğrulandı |

\* Yerel testte Google Fonts isteği **ortamın ağ politikası** nedeniyle düşüyor
(16 adet `net::ERR_CONNECTION_RESET`). Bu bir ortam kısıtıdır, site kusuru
değildir; yayındaki sitede fontlar yükleniyor.

---

## 4. Viewport matrisi

Sayfa: `index.html` (tüm satırlar). "Taşma" sütunu gerçek içerik taşmasını
gösterir; dekoratif kenar taşmaları denetim raporunun ilgili bölümünde
ayrıca listelenmiştir.

| Ölçü | Yatay kaydırma | Taşan içerik | Kesilen içerik | Üst üste binme | Küçük dokunma hedefi | Sonuç |
| --- | --- | --- | --- | --- | --- | --- |
| 320×568 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 360×640 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 375×667 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 390×844 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 412×915 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 430×932 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 540×720 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 768×1024 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 820×1180 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 1024×768 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 1280×720 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 1366×768 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 1440×900 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 1536×864 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 1920×1080 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 2560×1440 | Yok | Yok | Yok | Yok | 0 | ✅ |
| 844×390 (yatay) | Yok | Yok | Yok | Yok | 0 | ✅ |
| 932×430 (yatay) | Yok | Yok | Yok | Yok | 0 | ✅ |
| 667×375 (yatay) | Yok | Yok | Yok | Yok | 0 | ✅ |

**Ara genişlik taraması:** 320 → 2560 px, 80 px adım (29 nokta) — taşma yok.

### `404.html`

| Ölçü | Yatay kaydırma | Dikey kaydırma | Taşan içerik | Kesilen içerik | Sonuç |
| --- | --- | --- | --- | --- | --- |
| 320×568 · 360×640 · 390×844 · 430×932 | Yok | Yok | Yok | Yok | ✅ |
| 540×720 · 768×1024 · 1024×768 | Yok | Yok | Yok | Yok | ✅ |
| 1280×720 · 1440×900 · 1920×1080 · 2560×1440 | Yok | Yok | Yok | Yok | ✅ |
| 844×390 (yatay) · 667×375 (yatay) | Yok | Yok | Yok | Yok | ✅ |

Ana sayfaya dönüş bağlantısı her ölçüde 52×196 px (44 px eşiğinin üzerinde).
Konsol hatası yok.

### Çentik simülasyonu

`env(safe-area-inset-*)` değerleri gerçek iPhone 14 Pro paylarıyla değiştirilmiş
bir kopya üzerinde ölçüldü.

| Senaryo | Container yatay boşluk | Header üst konumu | İletişim çubuğu alt boşluk | Yatay kaydırma |
| --- | --- | --- | --- | --- |
| Portre 390×844 / 430×932 / 320×568 (üst 59, alt 34) | 16 px | **59 px** | **44 px** | Yok |
| Yatay 844×390 / 932×430 (yanlar 59, alt 21) | **59 px** | 0 px | (gizli) | Yok |
| Çentiksiz (`env() = 0`) | 16–24 px | 0 px | 10 px | Yok |

### Core Web Vitals (Playwright + `PerformanceObserver`, yerel sunucu)

Lighthouse çalıştırılamadığı için metrikler doğrudan tarayıcı API'siyle ölçüldü.

| Metrik | Mobil 390×844 | Masaüstü 1440×900 | Eşik | Durum |
| --- | --- | --- | --- | --- |
| FCP — **önce** | 13.016 ms | 12.776 ms | < 1.800 ms | ❌ |
| FCP — **sonra** | **132 ms** | **168 ms** | < 1.800 ms | ✅ |
| LCP — **sonra** | **132 ms** | **168 ms** | < 2.500 ms | ✅ |
| CLS | **0** | **0,001** | < 0,1 | ✅ |
| `domInteractive` | 23 ms | 21 ms | — | ✅ |
| Toplam aktarım | 263,2 KB | 263,2 KB | — | ✅ |
| Kaynak sayısı | 9 | 9 | — | ✅ |

LCP kaynağı masaüstünde `div.hero-background` (önceden yüklenen WebP).
Aktarımın dağılımı: HTML 39,4 KB · CSS 63,3 KB · görsel 149,4 KB · JS 11,2 KB.
Görsel payı gerçek fotoğraf/illüstrasyonların eklenmesiyle 75,2 → 149,4 KB'a
çıktı; `srcset` sayesinde mobilde bu artış sınırlı kaldı ve LCP düşmedi.

**Ölçümün sınırı:** Denetim ortamı Google Fonts'a erişemiyor. Bu, "font servisi
erişilemez" senaryosunu gerçekçi biçimde test etmemizi sağladı ve düzeltilen
kusuru ortaya çıkardı. Gerçek kullanıcıların çoğunda font servisi ~100 ms'de
yanıt verir; bu nedenle **önce** sütunundaki değerler tipik değil, en kötü
durum değerleridir. Düzeltmeden sonra ilk boyama artık font servisine hiç
bağlı değildir.

---

## 5. WebP dönüşüm raporu

Kullanıcının ChatGPT'de ürettiği üç görsel dönüştürülüp entegre edildi.

| Kaynak | Yeni dosya | Önceki boyut | Yeni boyut | Tasarruf | Kullanıldığı bölüm | Kalite kontrolü |
| --- | --- | --- | --- | --- | --- | --- |
| Kullanıcının yüklediği PNG | `assets/images/hero/okur-nakliyat-hero-background.webp` | 1.429.670 B | 71,9 KB | **%95,0** | Hero arka planı (CSS) | Kanal başına ortalama fark ~1/255; görünür kayıp yok |
| `9e01fec0…png` (şeffaf) | `assets/images/hero/okur-nakliyat-hero-arac.webp` | 2.133 KB | 117,8 KB | **%94,5** | Hero ön planı (retina) | Opak bölgede ortalama fark **1,68/255**, en yüksek 29. Alfa kanalı korundu (%83,5 tamamen şeffaf) |
| ↳ mobil varyant | `assets/images/hero/okur-nakliyat-hero-arac-900.webp` | — | 44,5 KB | — | `srcset` 900w | 900×600'e LANCZOS ile küçültüldü |
| `309b3759…png` | `assets/images/about/okur-nakliyat-hakkimizda.webp` | 1.221 KB | 34,4 KB | **%97,2** | Hakkımızda bölümü | Görünür kayıp yok |
| `98071a90…png` | `assets/images/og/okur-nakliyat-og.jpg` | 1.447 KB | 57,5 KB | **%96,0** | `og:image` / `twitter:image` | 1200×630'a LANCZOS; **JPG** seçildi çünkü sosyal platformlar WebP önizlemeyi desteklemiyor |

**Silinen dosyalar:** `okur-nakliyat-hero.svg`, `okur-nakliyat-og.svg` — yerlerini
raster karşılıkları aldı. `.about-scene` içindeki inline SVG de kaldırıldı.

Kalan SVG'ler:

| Öğe | Tür | Durum |
| --- | --- | --- |
| `assets/images/logo/favicon.svg` | Logo / ikon | ✅ Kural gereği SVG kalır |
| `.coverage-map` (inline) | Dekoratif harita | ℹ️ Vektör bırakıldı — gerekçe prompt dosyasında |
| Arayüz ikonları (inline) | İkon | ✅ Kural gereği SVG kalır |

### Responsive görsel (`srcset`) doğrulaması

| Senaryo | Seçilen dosya | İndirilen | Oran bozulması |
| --- | --- | --- | --- |
| Mobil 390 @2x | `…-900.webp` | **44,5 KB** | 0,0000 |
| Mobil 390 @1x | `…-900.webp` | 44,5 KB | 0,0000 |
| Masaüstü 1440 @1x | `…-900.webp` | 44,5 KB | 0,0000 |
| Masaüstü 1440 @2x | `…-arac.webp` | 117,8 KB | 0,0000 |

Mobilde tek boyutlu sunuma göre **%62 daha az** veri iniyor.

---

## 6. ChatGPT görsel promptları

| | |
| --- | --- |
| Hazırlanan prompt sayısı | 3 |
| Üretilen görsel sayısı | **3** — kullanıcı kendi ChatGPT hesabında üretti |
| Claude tarafından üretilen görsel | **0** — bu ortamda görsel üretim entegrasyonu yok |
| Entegrasyon durumu | ✅ Üçü de dönüştürülüp siteye yerleştirildi ve ölçümle doğrulandı |
| Eksik kullanıcı işlemi | Yok |

Sahte görsel üretilmedi, internetten telif durumu belirsiz görsel indirilmedi,
base64 görsel kaynak koda gömülmedi.

**SVG kuralına uyum:** Bu denetim çalışmasında **yeni SVG illüstrasyon, arka
plan veya dekorasyon üretilmedi.** Mevcut SVG'lerin tamamı kural yürürlüğe
girmeden önce, sayfanın tasarım aşamasında oluşturulmuştu; siteyi kırmamak için
silinmediler ve raster karşılıkları için prompt hazırlandı. Arayüz ikonları
kural kapsamında inline SVG olarak kalmaya devam ediyor.

---

## 7. Yapılamayan işlemler

| İşlem | Neden | Alınan hata | Denenen çözüm | Kullanıcının yapması gereken | İlgili komut |
| --- | --- | --- | --- | --- | --- |
| Lighthouse analizi | Ortamda Lighthouse CLI yok, dış ağ erişimi beyaz listeyle sınırlı | — | Yerel Chromium ile manuel ölçüm (LCP kaynağı, önbellek başlıkları, sıkıştırma) | Chrome DevTools → Lighthouse sekmesinden canlı sitede çalıştırmak | `npx lighthouse https://okurnakliyatedremit.com` |
| Otomatik a11y taraması | `@axe-core/playwright` kurulu değil, paket indirme kısıtlı | — | Dokunma hedefi, başlık sırası, ARIA ve odak yönetimi elle kontrol edildi | Yerelde kurup denetimi tekrarlamak | `npm i -D @axe-core/playwright` |
| Build / Lint / Typecheck | Projede derleme sistemi, lint yapılandırması ve TypeScript yok | — | Proje yapısı incelendi | Gerekirse bir lint kurulumu istemek | — |
| Görsel üretimi | ChatGPT görsel entegrasyonu yok | — | 3 prompt eksiksiz hazırlandı | Promptları ChatGPT'ye vermek | `docs/chatgpt-image-prompts.md` |
| Gerçek cihaz testi | Ortamda fiziksel cihaz yok | — | Chromium'da 16 viewport + 3 yatay senaryo + 5 çentik senaryosu simüle edildi | iOS Safari ve Android Chrome'da gözle kontrol | — |
| Görsel regresyon karşılaştırması | Başlangıç ekran görüntüleri sistematik arşivlenmedi | — | Ölçüm tabanlı karşılaştırma yapıldı (yükseklik, taşma, hedef boyutu, örtüşme — hepsi sayısal raporlandı) | — | `npm run test:responsive:shot` |

---

## 8. Bilinen kalan riskler

- **Google Fonts bağımlılığı:** Fontlar hâlâ dış servisten geliyor. İlk boyama
  artık bu servise bağlı değil (bloklamayan yüklemeye geçildi), ancak servis
  yavaşladığında yazı tipi geç oturur ve kısa bir yedek-font aşaması görünür.
  Tam bağımsızlık isteniyorsa `.woff2` dosyaları `assets/fonts/` altına alınıp
  `@font-face` ile yerelden servis edilmelidir.
- **Kullanılmayan CSS:** `.btn-secondary.btn-on-light` (2 kural, ~0,2 KB) hiçbir
  HTML'de kullanılmıyor. Tasarım sisteminin belgelenmiş bir varyantı olduğu ve
  ileride açık zeminli bir bölümde gerekebileceği için silinmedi. Taranan diğer
  380 kuralın tamamı ya kullanılıyor ya da durum bağımlı.
- **Gerçek cihaz testi yapılmadı:** Özellikle iOS Safari'de dinamik adres çubuğu
  davranışı fiziksel cihazda doğrulanmalı.
- **Mobilde başlık 4 satır:** 540 px ve altında hero başlığı 4 satıra düşüyor.
  Taşma veya kesilme üretmiyor; ortalanmış büyük mobil başlık bilinçli bir
  tasarım tercihi olduğu için **kullanıcıya sormadan değiştirilmedi.**
- **Yatay ekranda hero hâlâ tek ekrandan uzun:** 1,41×–1,83× aralığında. Tek
  ekrana sığdırmak için başlık veya açıklama metnini kısaltmak gerekir; bu
  içerik kararı olduğu için yapılmadı.
- **Kaydırılabilir şerit ve klavye:** Hizmet şeridi 720 px altında yatay
  kaydırılabilir. Chrome kaydırılabilir kutuları kendiliğinden klavye durağı
  yapar; **Firefox ve Safari yapmaz.** Bu tarayıcılarda şeridin görünmeyen
  kısmına yalnızca dokunma/fare ile ulaşılır. Şeritteki dört hizmet adı
  hizmetler bölümünde ve footer'da bağlantı olarak da bulunduğu için bilgi
  kaybı yoktur; bu nedenle yapay bir `tabindex` eklenmedi.
- **`viewport-fit=cover` gerçek cihazda doğrulanmadı:** Güvenli alan payları
  `env()` değerleri gerçek iPhone ölçüleriyle değiştirilerek simüle edildi ve
  beş senaryoda doğru sonuç verdi. Fiziksel bir iPhone'da göz kontrolü yine de
  önerilir.
- **`body { overflow-x: hidden }`:** Depoda önceden var olan güvenlik ağı.
  Dekoratif kenar taşmalarını örtüyor; bu denetimde hiçbir gerçek kusuru
  gizlemek için kullanılmadı, ancak ileride eklenecek yeni bölümlerde bir taşma
  olursa çıplak gözle fark edilmeyebilir. Bu yüzden `npm run test:responsive`
  her değişiklikten sonra çalıştırılmalıdır.

---

## 9. Son doğrulama

Yalnızca gerçekten ölçülüp doğrulanan kutular işaretlenmiştir.

- [x] Yatay taşma yok (19 senaryo + 29 ara genişlik, ölçümle doğrulandı)
- [x] Gerçek içerik taşması yok (320 px'de 32 taşan öğe → 0)
- [x] Mobil görünüm doğrulandı (320–430 px, 6 ölçü)
- [x] Tablet görünümü doğrulandı (540, 768, 820, 1024 px)
- [x] Masaüstü görünümü doğrulandı (1280, 1366, 1440, 1536 px)
- [x] Büyük ekran görünümü doğrulandı (1920, 2560 px)
- [x] Landscape görünümü doğrulandı (844×390, 932×430, 667×375)
- [x] Dokunma hedefleri 44 px eşiğinin üzerinde (19 senaryoda 0 ihlal)
- [x] Metin kesilmesi giderildi (hero başlık satırları: `scrollHeight === clientHeight`)
- [x] Öğe çakışması giderildi (1024×768 ve 1280×720)
- [x] Form 320 px dahil tüm ölçülerde kapsayıcı içinde
- [x] Görseller optimize edildi (4 raster görsel, %94,5–%97,2 tasarruf)
- [x] `srcset` responsive görsel eklendi ve 4 senaryoda doğrulandı (mobilde %62 tasarruf)
- [x] Open Graph görseli SVG'den JPG'ye çevrildi (sosyal önizleme sorunu giderildi)
- [x] SVG kuralına uyuldu (yeni SVG illüstrasyon üretilmedi)
- [x] ChatGPT promptları hazırlandı (3 adet) ve üçü de entegre edildi
- [x] Console error yok (site kaynaklı)
- [x] Kırık asset yok (404 yok)
- [x] Ekran görüntüsüyle görsel doğrulama yapıldı (hero, hizmetler, SSS, footer × 3 ölçü)
- [x] `404.html` 13 ölçüde doğrulandı (kaydırma, taşma, kesilme yok)
- [x] Güvenli alan (`env()`) desteği eklendi ve 5 senaryoda simülasyonla doğrulandı
- [x] Klavye erişimi doğrulandı (skip-link, sekme sırası, mobil menü odak tuzağı + ESC, SSS)
- [x] Kırık çapa / bağlantı yok (34 iç çapanın tamamı geçerli)
- [x] Başlık hiyerarşisi doğrulandı (tek `h1`, seviye atlaması yok)
- [x] Form denetimleri iOS Safari zoom eşiğinin üzerinde (16 px)
- [x] Yinelenen CSS seçicisi yok; `!important` kullanımlarının tamamı gerekçeli
- [x] Core Web Vitals ölçüldü (LCP 152/240 ms, CLS 0/0,001 — ikisi de eşiğin altında)
- [x] Render'ı bloklayan kaynak kaldırıldı (FCP 13.016 ms → 152 ms)
- [x] Kullanılmayan CSS tarandı (380 kural; gerçekten ölü olan 2 kural raporlandı)
- [x] Final raporu oluşturuldu
- [ ] Build başarılı — *derleme sistemi yok, çalıştırılamadı*
- [ ] Lighthouse skorları — *ortamda çalıştırılamadı, bölüm 7*
- [ ] Otomatik a11y taraması — *ortamda çalıştırılamadı, bölüm 7*
- [ ] Gerçek cihaz testi — *ortamda fiziksel cihaz yok*

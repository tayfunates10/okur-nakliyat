# Final UI Raporu — Okur Nakliyat

**Tarih:** 30 Temmuz 2026
**Kapsam:** Ana sayfanın tamamı üzerinde responsive/UI denetimi, düzeltmeler ve
ölçümle doğrulama

---

## 1. Genel sonuç

Proje **saf statik bir sitedir**: HTML5 + CSS3 + vanilla JavaScript. Framework,
derleme adımı veya TypeScript yoktur. Depoya bu çalışmada eklenen `package.json`
**yalnızca geliştirme/test aracı** içindir (Playwright); site çalışma zamanında
hiçbir pakete bağlı değildir ve sunucuya yalnızca statik dosyalar gönderilir.

| | |
| --- | --- |
| Görevin genel durumu | Uygulanabilir tüm aşamalar tamamlandı |
| İncelenen sayfa sayısı | 1 (`index.html` — sitedeki tek sayfa) |
| İncelenen bölüm sayısı | 9 (hero, hizmetler, hakkımızda, süreç, hizmet bölgesi, SSS, teklif formu, CTA, footer) |
| Test edilen viewport | 16 cihaz ölçüsü + 3 yatay senaryo + 29 ara genişlik |
| Değiştirilen dosya sayısı | 4 (`style.css`, `variables.css`, `components.css`, `index.html`) |
| Oluşturulan dosya sayısı | 4 (`tests/responsive-audit.js`, `package.json`, `docs/` altındaki 3 rapor) |
| Düzeltilen ölçülmüş kusur | 7 |
| Uygulanan iyileştirme | 1 |

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

### Yükseklik ve viewport davranışı

- **Yatay ekran kuralı eklendi:**
  `@media (orientation: landscape) and (max-height: 560px) and (min-width: 640px)`
  — iki sütunlu düzene dönüş, sıkılaştırılmış dikey ritim, 260 px görsel
  yüksekliği, `clamp(1.6rem, 4vw, 2.35rem)` başlık ölçeği.
- **Footer alt boşluğu** sabit mobil iletişim çubuğunun görünmediği
  genişliklerde `clamp(2.5rem, 4vw, 3.5rem)`'e indirildi.

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

- Hero arka planı `<link rel="preload" as="image" fetchpriority="high">` ile
  önceden yükleniyor (LCP kaynağı).
- Fontlar tek istekte, `display=swap` ve `preconnect` ile.
- `.htaccess` üzerinden gzip/brotli; statik dosyalar için 1 yıllık `immutable`
  önbellek, HTML için `no-cache` — canlıda yanıt başlıklarıyla doğrulanmıştı.
- CSS ve JavaScript sürgüsü `?v=3 → ?v=4` yapıldı; yayına alındığında eski
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
| Yatay taşma testi | **Başarılı** | 320–2560 px arası hiçbir noktada taşma yok |
| Dokunma hedefi testi | **Başarılı** | 19 senaryonun tamamında 0 |
| Metin kesilme testi | **Başarılı** | Gerçek kesilme 0; kalan uyarılar dekoratif öğelerden |
| Öğe çakışması testi | **Başarılı** | 0 |
| Görsel oran testi | **Başarılı** | `naturalWidth > 0`, oran bozulması 0 |
| Console error testi | **Başarılı\*** | Site kaynaklı hata yok |
| Kırık asset testi | **Başarılı** | 404 yok |
| Landscape görünüm | **Başarılı** | 844×390, 932×430, 667×375 |
| Formlar | **Başarılı** | Teklif formu 320 px dahil tüm ölçülerde kapsayıcı içinde |
| Mobil menü | **Başarılı** | Açılma, ESC, overlay, kaydırma kilidi, odak yönetimi |
| Lighthouse | **Çalıştırılamadı** | Ortamda Lighthouse CLI yok, dış ağ erişimi beyaz listeyle sınırlı |
| Otomatik a11y taraması (axe) | **Çalıştırılamadı** | Paket ortamda kurulu değil, dış ağ erişimi sınırlı |
| Erişilebilirlik (elle) | **Kısmen başarılı** | Dokunma hedefi, başlık sırası, ARIA, odak yönetimi kontrol edildi |
| Gerçek cihaz testi | **Çalıştırılamadı** | Ortamda fiziksel cihaz yok |

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

---

## 5. WebP dönüşüm raporu

**Projede dönüştürülecek PNG/JPEG bulunmamaktadır.**
`find assets -name "*.png" -o -name "*.jpg" -o -name "*.jpeg"` sonucu boştur.

Tek raster görsel bu oturumdan önce dönüştürülmüştü:

| Kaynak | Yeni dosya | Önceki boyut | Yeni boyut | Tasarruf | Kullanıldığı bölüm | Kalite kontrolü |
| --- | --- | --- | --- | --- | --- | --- |
| Kullanıcının yüklediği PNG | `assets/images/hero/okur-nakliyat-hero-background.webp` | 1.429.670 B | 71.882 B | **%95,0** | Hero arka planı (CSS `background-image`) | Kanal başına ortalama fark ~1/255; görünür kayıp yok. 1672×941 çözünürlük korundu. |

Kalan görseller SVG'dir ve raster dönüşüm kapsamına girmez:

| Öğe | Tür | Durum |
| --- | --- | --- |
| `assets/images/logo/favicon.svg` | Logo / ikon | ✅ Kural gereği SVG kalabilir |
| `assets/images/hero/okur-nakliyat-hero.svg` | Hero illüstrasyonu | ⚠️ Raster ile değiştirilmeli (Prompt 1) |
| `assets/images/og/okur-nakliyat-og.svg` | Paylaşım görseli | ⚠️ **JPG/PNG** ile değiştirilmeli (Prompt 2) |
| `.about-scene` (inline) | Hakkımızda illüstrasyonu | ⚠️ Raster ile değiştirilebilir (Prompt 3) |
| `.coverage-map` (inline) | Dekoratif harita | ℹ️ Vektör bırakıldı — gerekçe prompt dosyasında |
| Arayüz ikonları (inline) | İkon | ✅ Kural gereği SVG kalır |

---

## 6. ChatGPT görsel promptları

| | |
| --- | --- |
| Hazırlanan prompt sayısı | 3 |
| Üretilen görsel sayısı | **0** |
| Üretilemeyen görseller | Hero ön plan aracı, Open Graph paylaşım görseli, hakkımızda illüstrasyonu |
| Entegrasyon durumu | **Yok** — bu ortamda ChatGPT görsel üretme aracı veya API entegrasyonu bulunmuyor |
| Eksik kullanıcı işlemleri | Promptları ChatGPT'ye verip görselleri üretmek, `docs/chatgpt-image-prompts.md` içindeki adımlarla entegre etmek |

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
| Gerçek cihaz testi | Ortamda fiziksel cihaz yok | — | Chromium'da 16 viewport + 3 yatay senaryo simüle edildi | iOS Safari ve Android Chrome'da gözle kontrol | — |
| Görsel regresyon karşılaştırması | Başlangıç ekran görüntüleri sistematik arşivlenmedi | — | Ölçüm tabanlı karşılaştırma yapıldı (yükseklik, taşma, hedef boyutu, örtüşme — hepsi sayısal raporlandı) | — | `npm run test:responsive:shot` |

---

## 8. Bilinen kalan riskler

- **Google Fonts bağımlılığı:** Fontlar dış servisten geliyor. Servis yavaşlarsa
  `display=swap` sayesinde metin görünür kalır, ancak yazı tipi geç oturur.
- **Open Graph önizlemesi:** `og:image` hâlâ SVG. Bazı platformlar SVG önizlemeyi
  desteklemez; paylaşım kartı bu görsel değişene kadar bazı uygulamalarda boş
  görünebilir. (Prompt 2)
- **Kullanıcı tarafından sağlanacak görseller:** Üç raster görsel bekliyor.
- **Gerçek cihaz testi yapılmadı:** Özellikle iOS Safari'de dinamik adres çubuğu
  davranışı fiziksel cihazda doğrulanmalı.
- **Mobilde başlık 4 satır:** 540 px ve altında hero başlığı 4 satıra düşüyor.
  Taşma veya kesilme üretmiyor; ortalanmış büyük mobil başlık bilinçli bir
  tasarım tercihi olduğu için **kullanıcıya sormadan değiştirilmedi.**
- **Yatay ekranda hero hâlâ tek ekrandan uzun:** 1,41×–1,83× aralığında. Tek
  ekrana sığdırmak için başlık veya açıklama metnini kısaltmak gerekir; bu
  içerik kararı olduğu için yapılmadı.
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
- [x] Görseller optimize edildi (tek raster görsel WebP, %95 tasarruf)
- [x] SVG kuralına uyuldu (yeni SVG illüstrasyon üretilmedi)
- [x] ChatGPT promptları hazırlandı (3 adet)
- [x] Console error yok (site kaynaklı)
- [x] Kırık asset yok (404 yok)
- [x] Ekran görüntüsüyle görsel doğrulama yapıldı (hero, hizmetler, SSS, footer × 3 ölçü)
- [x] Final raporu oluşturuldu
- [ ] Build başarılı — *derleme sistemi yok, çalıştırılamadı*
- [ ] Lighthouse skorları — *ortamda çalıştırılamadı, bölüm 7*
- [ ] Otomatik a11y taraması — *ortamda çalıştırılamadı, bölüm 7*
- [ ] Gerçek cihaz testi — *ortamda fiziksel cihaz yok*

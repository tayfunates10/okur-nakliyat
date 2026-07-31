# Responsive / UI Denetim Raporu

**Tarih:** 30 Temmuz 2026
**Kapsam:** `index.html` (bölümler: hero `#anasayfa`, hizmetler `#hizmetler`,
hakkımızda `#hakkimizda`, süreç `#surec`, hizmet bölgesi, SSS `#sss`,
teklif formu `#teklif`, CTA, footer) ve `404.html`.
**Yöntem:** Playwright + Chromium; 16 cihaz ölçüsü, 3 yatay (landscape) senaryo,
320–2560 px arası 80 px adımlı 29 ara genişlik. Bütün tespitler DOM ölçümüyle
(`getBoundingClientRect`, `scrollWidth/clientWidth`, `scrollHeight/clientHeight`)
alınmıştır; hiçbiri gözle tahmin değildir.

> **Not:** Bu rapor, ana sayfanın tüm bölümleri tamamlandıktan sonra yapılan
> denetimi anlatır. Daha önceki (yalnızca hero'nun bulunduğu) sürüme ait
> ölçümler geçersizdir ve buraya taşınmamıştır.

---

## Tespit edilen sorunlar ve uygulanan çözümler

### 1. Teklif formu 320 px'de kapsayıcısından taşıyordu

| | |
| --- | --- |
| Bileşen | `.quote-grid`, `.quote-content`, `#quoteForm`, `.quote-submit` |
| Ekranlar | 320×568 |
| Ölçüm | Kapsayıcı `.quote-grid` **288 px**, içindeki `.quote-content` ve `#quoteForm` **343,31 px**. Sağ kenar `x = 359`, viewport ise 320 px. Form alanları, etiketler ve gönder düğmesi dahil **32 öğe** görünür alanın dışına taşıyordu. |
| Neden | İki bağımsız etken üst üste bindi: **(a)** `.btn` üzerindeki `white-space: nowrap` yüzünden "WhatsApp'tan Teklif İste" düğmesinin min-content genişliği 305 px'e çıkıyordu; **(b)** dar ekranda tek sütuna inen grid'ler `grid-template-columns: 1fr` kullanıyordu — bu `minmax(auto, 1fr)` demektir ve izin otomatik alt sınırı (min-content) kapsayıcıyı aşmasına izin verir. |
| Gizlenme sebebi | Taşma `body { overflow-x: hidden }` tarafından örtülüyordu; bu yüzden yatay kaydırma çubuğu görünmüyor, sorun ilk bakışta fark edilmiyordu. **Sorun `overflow-x: hidden` eklenerek gizlenmedi; kök neden bulunup düzeltildi.** |
| Çözüm | Dokuz yerdeki `grid-template-columns: 1fr` → `minmax(0, 1fr)`; `1.35fr 1fr 1fr` ve `1.45fr repeat(3, …)` izleri de `minmax(0, …)` ile sarıldı. `@media (max-width: 440px)` içine `.btn { white-space: normal }` ve `.btn-lg { padding-inline: 1.25rem }` eklendi. |
| Son durum | ✅ 320 px'de `.quote-content` ve `#quoteForm` **16 → 304 px** (viewport içinde, iki yanda simetrik 16 px). Taşan öğe sayısı **42 → 10**; kalan 10'u aşağıdaki "bilinçli dekoratif taşma" listesindedir. |

### 2. 44 px altında dokunma hedefleri

| | |
| --- | --- |
| Bileşenler | `a.header-phone`, `a.service-link` (×6), `a.text-action` (×2), `.footer-column a` / `span` (×10), `.footer-bottom a` |
| Ekranlar | Tümü |
| Ölçüm | 1440×900'de **20 hedef**, 390×844'te **19 hedef** eşiğin altındaydı. Yükseklikler: `header-phone` 41 px, `service-link` 26 px, `text-action` 31 px, footer bağlantıları 18–21 px. |
| Çözüm | İlgilere `min-height: var(--tap-target)` (44 px) eklendi. Alt çizgili bağlantılarda (`.service-link`, `.text-action`) ek yükseklik `align-items: flex-end` ile **metnin üstüne** verildi; böylece alt çizgi metne yapışık ve tek parça kalır — kutuyu büyütmenin çizgiyi metinden koparması engellendi. `.footer-column` boşluğu `0.65rem → 0`, çünkü bağlantılar artık kendi 44 px'ini taşıyor. |
| Son durum | ✅ 16 viewport + 3 landscape senaryonun **tamamında 0**. |

### 3. Hero başlığında alt uzantıların kırpılması

| | |
| --- | --- |
| Bileşen | `.hero-title-line` |
| Ekranlar | Tümü |
| Ölçüm | 1440×900'de `scrollHeight = 66`, `clientHeight = 62` (satır 1) ve `128 / 125` (satır 2). Yani her satırda 3–4 px içerik kırpılıyordu. |
| Neden | `.hero-title-line` üzerinde giriş animasyonunu maskelemek için `overflow: hidden` var; `line-height: 1.04` ise satır kutusunu font'un iniş (descender) alanından küçük yapıyor. Türkçe metindeki **ğ, y, ı** harfleri ve virgül maskenin dışında kalıp kesiliyordu. |
| Çözüm | `.hero-title-line`'a `padding-bottom: 0.16em` + `margin-bottom: -0.16em` (kırpma kutusu büyür, yerleşim aynı kalır). Maske büyüdüğü için `heroTitleReveal` başlangıcı `translateY(104%) → translateY(122%)` yapıldı; aksi hâlde animasyonun başında metnin üst kenarı görünecekti. |
| Son durum | ✅ 320 / 390 / 768 / 1440'ta `scrollHeight === clientHeight`. Denetim çıktısındaki kesilme listesinden tamamen çıktı. |

### 4. SSS kapalıyken her satırın altında 22 px boş şerit

| | |
| --- | --- |
| Bileşen | `.faq-answer p` |
| Ekranlar | Tümü |
| Ölçüm | Kapalı `<details>` içindeki `p` yüksekliği **21,6 px** (masaüstü), item yüksekliği 109 px. |
| Neden | Akordeon `grid-template-rows: 0fr → 1fr` tekniğiyle çalışıyor, ancak `p` üzerindeki `padding: 0 1.35rem 1.35rem` iz yüksekliğine bağlı değildir — 0fr'de bile alt padding yüksekliği üretmeye devam eder. |
| Çözüm | Alt padding akışa alındı: `padding: 0 1.35rem` + `.faq-answer p::after { display: block; height: 1.35rem }`. `::after` içerik akışında olduğu için 0fr'de birlikte kapanır. `@media (max-width: 720px)` içinde 1rem karşılığı da güncellendi. |
| Son durum | ✅ Kapalı `p` yüksekliği **21,6 → 0 px**; item yüksekliği **109 → 87 px** (mobil) / **78 px** (masaüstü). Açıldığında boşluk aynen korunuyor. |

### 5. Hero hizmet şeridi içeriğin üzerine biniyordu

| | |
| --- | --- |
| Bileşenler | `.hero-inner`, `.hero-service-rail` |
| Ekranlar | 1024×768, 1280×720 |
| Ölçüm | `.hero-content` alt kenarı 706 px, şeridin üst kenarı 687 px → **19 px örtüşme** (1024×768). 1280×720'de **23 px**. Şeridin `z-index: 3` ve opak sarı zemini olduğu için içeriğin alt kısmını fiilen kapatıyordu. |
| Neden | Şerit `position: absolute; inset: auto 0 0` ile hero'nun altına sabitlenmiş. `.hero-inner` 72 px'lik şerit payını yalnızca `min-height` hesabından düşüyordu; içerik bu asgari yüksekliği aştığında pay yok oluyordu. |
| Çözüm | Pay `min-height`'tan alınıp kalıcı alt boşluğa taşındı: `min-height: calc(clamp(720px, 92vh, 980px) - var(--header-height))` ve `padding-block: clamp(3rem, 7vh, 6rem) calc(clamp(3rem, 7vh, 6rem) + 72px)`. |
| Son durum | ✅ 1024×768'de **19 px örtüşme → 53 px boşluk**; 1280×720'de **23 px → 49 px**. Denetimde çakışma sayısı bütün ölçülerde 0. |

### 6. Yatay tutulan telefonlarda hero, ekran yüksekliğinin üç katı

| | |
| --- | --- |
| Bileşenler | `.hero`, `.hero-inner`, `.hero-visual` |
| Ekranlar | 844×390, 932×430, 667×375 |
| Ölçüm | Hero yüksekliği **1277 px (3,27×)**, **1285 px (2,99×)**, **1291 px (3,44×)**. |
| Neden | Düzen yalnızca genişliğe bakıyordu: 960 px altında hero tek sütuna iniyor ve `.hero-visual` 530 px asgari yükseklik alıyordu. Yatay tutulan bir telefon "dar" değil "alçak" olduğu için bu kural yanlış tarafa çalışıyordu. |
| Çözüm | Yeni blok: `@media (orientation: landscape) and (max-height: 560px) and (min-width: 640px)` — iki sütunlu düzene dönülür (içerik 1/7, görsel 8/-1), metin sola hizalanır, başlık `clamp(1.6rem, 4vw, 2.35rem)`'e iner, dikey boşluklar ve görsel yüksekliği (260 px) sıkılaştırılır, şerit 60 px olur. |
| Son durum | ✅ **1277 → 666 px (1,71×)**, **1285 → 608 px (1,41×)**, **1291 → 687 px (1,83×)**. Başlık ve açıklama artık ilk ekranda görünüyor. Kesilme veya taşma yok. |

### 7. Masaüstünde footer altında 104 px ölü alan

| | |
| --- | --- |
| Bileşen | `.site-footer` |
| Ekranlar | 721 px ve üzeri tüm ölçüler |
| Ölçüm | Telif satırının altında **104 px** boş zemin. |
| Neden | Taban kuralda `padding-bottom: 6.5rem` vardı; bu pay, yalnızca 720 px altında görünen sabit `.mobile-contact-bar` için ayrılmıştı. Çubuğun görünmediği genişliklerde pay boşuna duruyordu. |
| Çözüm | Taban değer `clamp(2.5rem, 4vw, 3.5rem)`'e indirildi; `@media (max-width: 720px)` içindeki `padding-bottom: 8.5rem` olduğu gibi bırakıldı. |
| Son durum | ✅ Masaüstünde alt boşluk **104 → 56 px**; mobilde sabit çubuk payı korunuyor. |

### 8. Kaydırılabilir hero şeridinde gösterge yokluğu (iyileştirme)

| | |
| --- | --- |
| Bileşen | `.hero-service-rail-inner` |
| Ekranlar | 720 px ve altı |
| Ölçüm | 390 px genişlikte şeridin **405 px'i** görünür alanın dışında; kaydırma çubuğu `scrollbar-width: none` ile gizli olduğu için devamı olduğu belli olmuyordu. |
| Çözüm | `.hero-service-rail::after` ile sağ kenara 42 px'lik sarıdan şeffafa geçiş eklendi; `pointer-events: none`. |
| Son durum | ✅ Şeridin devam ettiği görsel olarak belli oluyor. İçerik kaybı yok — şerit yatay kaydırılabilir kalmaya devam ediyor. |

### 9. Çentikli cihazlarda güvenli alan (safe area) desteği yoktu

| | |
| --- | --- |
| Bileşenler | `.container`, `.site-header`, `.mobile-menu`, `.mobile-contact-bar`, `.skip-link`, `.site-footer`, `404.html` gövdesi |
| Ekranlar | Çentik / ev göstergesi olan cihazlar (iPhone X ve sonrası) |
| Neden | Projede tek bir `env(safe-area-inset-*)` kullanımı yoktu. `viewport-fit` tanımsız olduğu için tarayıcı sayfayı güvenli alana sıkıştırıyor, çentikli telefonlarda yatay yönde iki yanda siyah şerit bırakıyor ve tam genişlik hero arka planı kenara ulaşamıyordu. |
| Çözüm | `index.html` ve `404.html` viewport etiketine `viewport-fit=cover` eklendi; ardından kenara oturan her öğeye güvenli alan payı verildi: `.container` yatay boşluğu `max(tasarım payı, env(...))`, `.site-header` üst boşluğu `env(safe-area-inset-top)`, sabit `.mobile-contact-bar` dört kenarı, `.mobile-menu` iç boşluğu, `.skip-link` konumu, mobil `.site-footer` alt boşluğu ve `scroll-padding-top`. |
| Doğrulama | `env()` çağrıları gerçek iPhone 14 Pro paylarıyla (portre 59/34, yatay 59/59/21) metinsel olarak değiştirilmiş bir kopya üretilip aynı denetim çalıştırıldı. Sonuç: **portrede header içeriği çentiğin 59 px altında**, **yatayda container yatay boşluğu 16 px → 59 px**, **iletişim çubuğu alt boşluğu 10 px → 44 px**, beş senaryonun hiçbirinde yatay kaydırma yok. Çentiksiz durumda (`env() = 0`) 19 senaryonun ölçümleri değişiklikten **önceki değerlerle birebir aynı** çıktı. |
| Son durum | ✅ Güvenli alan payları uygulanıyor, çentiksiz cihazlarda hiçbir davranış değişikliği yok. |

### 10. `404.html` yatay ekranda taşıyordu

| | |
| --- | --- |
| Bileşen | `404.html` — `.code`, `h1`, `a` |
| Ekranlar | 844×390, 667×375 |
| Ölçüm | İçerik yüksekliği 844×390'da **465 px**, 667×375'te **423 px**; her ikisinde de sayfa dikey kaydırma üretiyordu. Sebep: "404" rakamı `clamp(6rem, 24vw, 13rem)` ile yalnızca genişliğe bağlıydı, 844 px genişlikte 202 px'e çıkıyordu. |
| Çözüm | Rakam `clamp(4rem, min(24vw, 26vh), 13rem)`, başlık `clamp(1.75rem, min(7vw, 9vh), 4rem)`; başlık ve düğme dikey boşlukları `clamp(..., vh, ...)` ile kısa ekranlarda daralıyor. |
| Son durum | ✅ Test edilen **13 ölçünün tamamında** dikey ve yatay kaydırma yok, taşma yok, kesilme yok. Bağlantı 52×196 px. |

### 11. Kaydırılabilir şerit klavye odağında isimsizdi

| | |
| --- | --- |
| Bileşen | `.hero-service-rail-inner` |
| Neden | Şerit dar ekranda `overflow-x: auto` olduğu için Chrome onu kendiliğinden klavye durağı yapıyor. Ancak öğe isimsiz bir `div` idi ve odak halkası tanımlı değildi; `aria-label` ise erişilebilirlik ağacında yok sayılan, rolsüz dış `div` üzerindeydi. |
| Ölçüm | Sekme sırasında 6. durak: `div.container`, erişilebilir ad **yok**, görünür odak göstergesi **yok**. |
| Çözüm | `aria-label` kaydırma yapan iç öğeye taşındı, `role="group"` eklendi ve `:focus-visible` için görünür bir çerçeve tanımlandı. `tabindex` eklenmedi; böylece durak yalnızca şerit gerçekten kaydırılabilir olduğunda oluşur. |
| Son durum | ✅ Durak isimli (`role=group`, "Öne çıkan hizmetler") ve görünür. Sınırlama: Firefox ve Safari kaydırılabilir kutuları kendiliğinden odaklanabilir yapmaz — bkz. kalan riskler. |

### 12. Bu daldaki önceki düzeltmeler (yürürlükte)

| Değişiklik | Dosya | Durum |
| --- | --- | --- |
| `--container-gutter` → `clamp(32px, 4.5vw, 48px)`; 767 px'deki 32→40 px sıçraması kaldırıldı | `variables.css` | ✅ Yürürlükte |
| `.skip-link`, `.brand`, `.nav-link` → `min-height: var(--tap-target)`; nav dikey iç boşluk 0.5 → 0.625rem | `components.css` | ✅ Yürürlükte |
| `--fs-display` → `clamp(2.125rem, 8.5vw, 3.75rem)` | `variables.css` | ⚠️ Yalnızca 720 px üstünde etkili — aşağıdaki nota bakınız |

---

## İncelenip **sorun sayılmayan** durumlar

Aşağıdakiler otomatik denetimde "taşan" veya "kesik" olarak işaretlenir. Her biri
tek tek incelenmiş, kasıtlı tasarım kararı olduğu doğrulanmış ve **değiştirilmemiştir.**

| Öğe | Ölçüm | Neden sorun değil |
| --- | --- | --- |
| `div.hero-background` | 1440×900'de −10 → 1448 | 20 sn'lik drift animasyonu için `scale(1.01)`–`1.035` aralığında; kenar boşluğu görünmesin diye kutusundan büyük. `.hero { overflow: hidden }` kırpıyor. |
| `img.hero-visual-image` | 390 px'de −13 → 403 | Hero görselinin bilinçli kenar taşması; `.hero` kırpıyor, anlamlı içerik kaybı yok. |
| `div.coverage-map` + `svg` + `path` | 390 px'de −16 → 406 | `aria-hidden="true"` dekoratif Türkiye haritası; 720 px altında `width: 118%; margin-left: -9%` ile bilinçli olarak iki kenardan simetrik taşırılmış. `.coverage-section { overflow: hidden }` kırpıyor. |
| `.hero-service-rail-inner` içindeki `span` / `i` | 320 px'de 235 → 779 | Yatay kaydırılabilir şerit (`overflow-x: auto`); içerik erişilebilir, kaybolmuyor. 8. maddedeki gösterge eklendi. |
| `article.service-card` (kesik) | `scrollHeight 535` / `clientHeight 367` | Kartın sağ-alt köşesindeki dekoratif `::after` çemberi (`inset: auto -26% -46% auto`). Kart içeriği kesilmiyor; kesilen yalnızca çemberin kart dışında kalan yayı. |
| `.faq-answer p` (kesik) | `scrollHeight 71` / `clientHeight 0` | Akordeon kapalıyken beklenen davranış. `clientHeight = 0` olması 4. maddedeki düzeltmenin doğru çalıştığının kanıtıdır. |

### Yatay kaydırmanın gerçekten olmadığının doğrulaması

`documentElement.scrollWidth === documentElement.clientWidth` koşulu 16 viewport,
3 landscape senaryo ve 320–2560 px arası 29 ara genişliğin **tamamında** sağlandı.

`body { overflow-x: hidden }` kuralı depoda önceden vardı ve dekoratif taşmalar
için güvenlik ağı olarak bırakıldı. Bu denetimde **hiçbir sorun bu kuralla
gizlenmedi**; 1. maddedeki gerçek taşmanın kök nedeni bulunup giderildi.

### Başlık satır sayısı hakkında dürüst not

| Genişlik | Başlık punto | Görünen satır |
| --- | --- | --- |
| 320–540 px | 46–69 px | **4 satır** |
| 768 px | 60 px | 2 satır |
| 1024–2560 px | 60 px | 3 satır |

720 px altında `.hero-title` kendi kuralını kullanıyor
(`clamp(2.85rem, 13vw, 4.3rem)`), yani `--fs-display` bu aralıkta devrede
değildir. Mobilde başlığın 4 satıra düşmesi **taşma veya kesilme üretmiyor**;
ortalanmış, büyük puntolu mobil başlık bilinçli bir tasarım tercihidir ve
kullanıcıya sormadan değiştirilmemiştir.

---

## İncelenip **kusur bulunmayan** alanlar

Aşağıdakiler ölçülerek kontrol edildi; düzeltme gerektiren bulgu çıkmadı.

| Alan | Ölçüm / sonuç |
| --- | --- |
| Form denetimlerinde iOS Safari otomatik yakınlaştırma | Yedi alanın tamamı **16 px** (eşik 16 px), `box-sizing: border-box`, yükseklik 52–133 px. Zoom tetiklenmez. |
| Çapa bağlantıları | 34 iç bağlantının **tamamının** hedefi mevcut, kırık yok. Üç dış bağlantı WhatsApp'a gidiyor. |
| Başlık hiyerarşisi | Tek `h1`; 26 başlıkta seviye atlaması **yok**. |
| Erişilebilir ad | İsimsiz `<button>` veya `<a>` **yok** (0). |
| Form etiketleri | Yedi alanın tamamı `<label>` içinde; `required`, `inputmode`, `autocomplete` tanımlı. |
| Skip-link | Sekmede ilk durak, `:focus-visible` ile görünür oluyor (8, 8 konumunda, 44 px). |
| Mobil menü | Açılışta odak panele giriyor, gövde kaydırma kilitleniyor, panel sağ kenarı = viewport genişliği (taşma yok), ESC kapatıyor, odak açan düğmeye dönüyor, kilit kalkıyor. |
| SSS akordeonu | Fare ve klavye (Enter) ile açılıyor; ikinci öğe açıldığında birinci kapanıyor. Kapalı satır yüksekliği 78 px (yalnızca özet + kenarlık). |
| Görseller | Tek `<img>`; yükleniyor (`naturalWidth 960`), açıklayıcı `alt` metni ve `width`/`height` öznitelikleri var (layout shift üretmez). |
| `prefers-reduced-motion` | `reset.css` içinde `scroll-behavior: auto !important` dahil global azaltma; `style.css` içinde hero animasyonları ve parallax kapatılıyor. |
| Yinelenen CSS | Aynı medya bağlamında iki kez tanımlanmış seçici **yok** (0). |
| `!important` kullanımı | Toplam 8; **tamamı gerekçeli**: 5'i `prefers-reduced-motion` bloklarında, 3'ü `<noscript>` içinde ana stil sayfasını geçersiz kılmak için. |

## Test edilen ekran ölçüleri

**Cihaz matrisi (16):** 320×568, 360×640, 375×667, 390×844, 412×915, 430×932,
540×720, 768×1024, 820×1180, 1024×768, 1280×720, 1366×768, 1440×900, 1536×864,
1920×1080, 2560×1440

**Yatay yön (3):** 844×390, 932×430, 667×375

**Ara genişlik taraması (29):** 320'den 2560'a 80 px adım — hepsinde yatay
kaydırma yok.

**`404.html`:** 13 ölçü (320×568 – 2560×1440 ve 844×390, 667×375).

**Çentik simülasyonu (5):** portre 390×844, 430×932, 320×568; yatay 844×390,
932×430 — `env(safe-area-inset-*)` değerleri gerçek iPhone paylarıyla
değiştirilerek.

---

## Son durum özeti

| Kontrol | Başlangıç | Son |
| --- | --- | --- |
| Yatay kaydırma (19 senaryo) | 0 | **0** |
| Yatay kaydırma (29 ara genişlik) | 0 | **0** |
| Gerçek içerik taşması (320 px) | 32 öğe | **0** |
| Dokunma hedefi < 44 px (masaüstü) | 20 | **0** |
| Dokunma hedefi < 44 px (mobil) | 19 | **0** |
| Gerçek metin kesilmesi | 2 (hero başlık satırı) | **0** |
| Öğe çakışması | 2 ekranda (19 px, 23 px) | **0** |
| Görsel oran bozulması | 0 | **0** |
| Yatay ekranda hero / viewport oranı | 2,99× – 3,44× | **1,41× – 1,83×** |
| SSS kapalı satır altı boşluk | 21,6 px | **0** |
| Masaüstü footer ölü alanı | 104 px | **56 px** |
| `404.html` yatay ekranda dikey taşma | 2 ölçüde var | **yok** |
| Güvenli alan (`env()`) desteği | yok | **7 bileşende var** |
| İsimsiz klavye durağı | 1 | **0** |
| Konsol hatası (site kaynaklı) | 0 | **0** |
| Kırık asset / kırık çapa | 0 | **0** |

Denetim ortamının ağ politikası Google Fonts'u engellediği için yerel testte
16 adet `net::ERR_CONNECTION_RESET` görülür. Bu **ortam kısıtıdır**, site kusuru
değildir; yayındaki sitede fontlar yükleniyor.

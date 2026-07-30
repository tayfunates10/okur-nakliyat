# Responsive / UI Denetim Raporu

**Tarih:** 30 Temmuz 2026
**Kapsam:** `index.html` (sitedeki tek sayfa — diğer bölümler henüz oluşturulmadı)
**Yöntem:** Playwright + Chromium ile 19 viewport, 320–2560 px arası 29 noktalık
ara genişlik taraması, DOM ölçümüyle otomatik taşma/kesilme/dokunma hedefi analizi.

---

## Tespit edilen sorunlar ve uygulanan çözümler

### 1. Hero altında boş şerit (büyük ve kısa ekranlar)

| | |
| --- | --- |
| Sayfa | `index.html` |
| Bileşen | `.hero` |
| Ekranlar | 1280×720, 1440×900, 1920×1080, 2560×1440 |
| Neden | `min-height: clamp(680px, 88vh, 920px)` üst sınırı 920px'de kalıyordu. 1440px yüksekliğinde ekranda hero 920px'de bitiyor, altında 520px kırık beyaz sayfa zemini görünüyordu. 1280×720'de de 116px boşluk oluşuyordu. |
| Ölçüm | 2560×1440 → hero 920px, altında 520px boşluk. 1280×720 → hero 604px, altında 116px boşluk. |
| Çözüm | `min-height: max(clamp(680px, 88vh, 920px), 100svh)` — tasarım yüksekliği ile ekran yüksekliğinin büyüğü alınır. İçerik daha uzunsa doğal olarak büyümeye devam eder. |
| Son durum | ✅ Her ekranda hero en az görünür alanı doldurur, boş şerit kalmaz. 2560×1440'ta boşluk **520px → 0**, 1280×720'de **116px → 0**. |

### 2. Yatay ekranlarda aşırı uzun hero

| | |
| --- | --- |
| Bileşen | `.hero`, `.hero-inner` |
| Ekranlar | 844×390, 932×430, 667×375 (telefon yatay), 1024×768 (tablet yatay) |
| Neden | İki sütunlu düzen yalnızca `min-width: 1025px` altında açılıyordu. Yatay tutulan telefon ve tabletlerde içerik tek sütunda yığılıyor, hero 1095–1192px yüksekliğe ulaşıyordu. 390px yüksekliğindeki bir ekranda bu, hero'yu görmek için üç ekran boyu kaydırma demekti. |
| Ölçüm | 844×390 → hero 1095px (viewport'un 2,8 katı). 1024×768 → hero 1192px, başlık 3 satır. |
| Çözüm | Yeni kural: `@media (orientation: landscape) and (max-height: 820px) and (min-width: 700px)` — hero `min-height: 100svh` alır (tasarımın 680px alt sınırı burada dayatılmaz), iki sütuna geçer, başlık ölçeği ve dikey boşluklar küçülür, görsel 420px ile sınırlanır. Ayrıca `max-height: 480px` için ek sadeleştirme: arka plan animasyonu kapatılır. |
| Son durum | ✅ 844×390'da hero **1095px → 611px**. 1024×768'de **1192px → 768px** (tam ekran, boşluksuz). Kesilme yok. |

### 3. Küçük ekranlarda başlığın dört satıra düşmesi

| | |
| --- | --- |
| Bileşen | `.hero-title` / `--fs-display` |
| Ekranlar | 320, 360, 375, 390, 412 px |
| Neden | Taban ölçek `clamp(2.5rem, 6vw, 5.75rem)` idi; 430px altında alt sınır olan 40px devreye giriyor, Türkçe metnin uzunluğu nedeniyle başlık dört satıra düşüyordu. Tasarım şartnamesi en fazla üç satır öngörüyordu. |
| Ölçüm | Dört aday değer 320/360/390/430/540/768/899 px'de ölçüldü. |
| Çözüm | `clamp(2.125rem, 8.5vw, 3.75rem)` — 360px'den itibaren üç satır. |
| Son durum | ⚠️ 360px ve üzerinde ✅ üç satır. **320px'de hâlâ dört satır.** Üç satıra indirmek için fontu 30px'e çekmek gerekiyordu; bu, gerçek kullanımdaki telefonlarda (360–430px) başlığı gereksiz zayıflatacağı için bilinçli olarak tercih edilmedi. 320px'de taşma veya kesilme **yok**, yalnızca satır sayısı fazla. |

### 4. Erişilebilir olmayan dokunma hedefleri

| | |
| --- | --- |
| Bileşenler | `.skip-link`, `.brand`, `.nav-link` (×6), `.header-phone` |
| Ekranlar | Tümü (nav ve telefon yalnızca masaüstünde) |
| Neden | Yükseklikler 41–42px idi; 44×44px eşiğinin altında. |
| Ölçüm | Başlangıç: mobilde 2, masaüstünde 9 hedef eşiğin altında. |
| Çözüm | İlgili bileşenlere `min-height: var(--tap-target)` (44px) eklendi; `.nav-link` dikey iç boşluğu 0.5rem → 0.625rem. |
| Son durum | ✅ 19 viewport'un tamamında eşiğin altında hedef kalmadı. |

### 5. Container yatay boşluğunda sıçrama

| | |
| --- | --- |
| Bileşen | `.container` / `--container-gutter` |
| Neden | 767px'de 32px'ten 40px'e ani geçiş yapıyordu; ara genişliklerde sağ-sol boşluk oranı düzensizdi. |
| Çözüm | Tek akışkan değer: `clamp(32px, 4.5vw, 48px)`; medya sorgusundaki override kaldırıldı. |
| Son durum | ✅ 320–2560 px arasında sağ ve sol boşluk simetrik ve kademesiz. |

---

## İncelenip sorun bulunmayan / bilinçli bırakılan durumlar

### Dekoratif arka plan taşması (`.hero-background`)

Otomatik tarayıcı bu öğeyi her viewport'ta "taşan" olarak işaretliyor. İnceleme sonucu:

- Öğe `transform: scale(1.01)` ile başlar ve 20 saniyelik `heroBackgroundDrift`
  animasyonunda 1.035'e kadar büyür. Kenar boşluğu görünmesin diye **kasıtlı** olarak
  kutusundan büyüktür.
- Kapsayıcı `.hero` üzerinde `overflow: hidden` vardır.
- Doğrulama (1440×900): `documentElement.scrollWidth === clientWidth === body.scrollWidth === 1440`.
- 320–2560 px arası 29 noktada yatay kaydırma **oluşmuyor**.

**Sonuç:** Layout'a ve yatay kaydırmaya etkisi yok. Şartnamenin izin verdiği
"bilinçli dekoratif taşma" kapsamındadır, değiştirilmedi.

### Metin kesilmesi

`.hero-title`, `.hero-description`, `.badge`, `.trust-item`, `.btn`, `.nav-link`,
`.floating-card-*` öğeleri tek tek `scrollWidth/clientWidth` ve
`scrollHeight/clientHeight` ile karşılaştırıldı: **hiçbirinde kesilme yok.**
Denetim çıktısındaki "KESİK" uyarıları yalnızca yukarıdaki dekoratif arka plandan
kaynaklanıyordu.

### Görsel oranı

Tek `<img>` öğesi (`.hero-visual-image`) `object-fit: contain` kullanıyor ve
kapsayıcısında `aspect-ratio: 4 / 3` tanımlı. 19 viewport'un hiçbirinde oran
bozulması ölçülmedi.

### Header / içerik çakışması

`.site-header` alt kenarı ile `.hero-content` üst kenarı her viewport'ta
karşılaştırıldı; çakışma yok. `scroll-padding-top` tanımlı olduğu için çapa
bağlantıları da header altında kalmıyor.

---

## Test edilen ekran ölçüleri

**Cihaz matrisi (19 nokta):**
320×568, 360×640, 375×667, 390×844, 412×915, 430×932, 540×720, 768×1024,
820×1180, 1024×768, 1280×720, 1366×768, 1440×900, 1536×864, 1920×1080, 2560×1440
ve yatay yön: 844×390, 932×430, 667×375.

**Ara genişlik taraması:** 320'den 2560'a 80px adımlarla 29 nokta — hepsinde
yatay kaydırma yok.

---

## Son durum özeti

| Kontrol | Başlangıç | Son |
| --- | --- | --- |
| Yatay kaydırma (19 viewport) | 0 | **0** |
| Yatay kaydırma (29 ara genişlik) | 0 | **0** |
| Gerçek metin kesilmesi | 0 | **0** |
| Dokunma hedefi < 44px (mobil) | 2 | **0** |
| Dokunma hedefi < 44px (masaüstü) | 9 | **0** |
| Görsel oran bozulması | 0 | **0** |
| Öğe çakışması | 0 | **0** |
| Konsol hatası (yerel) | 0* | **0*** |
| Kırık asset / 404 | 0 | **0** |
| Hero altında boş şerit | 4 ekranda var | **yok** |
| Başlık > 3 satır | 5 ekranda | **1 ekranda (320px)** |

\* Test ortamının ağ politikası Google Fonts'u engellediği için yerel testte
`ERR_CONNECTION_RESET` görülüyor. Bu, ortam kısıtıdır; yayındaki sitede fontlar
sorunsuz yükleniyor (canlı denetimle doğrulandı). Site kaynaklı konsol hatası yok.

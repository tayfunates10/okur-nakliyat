# Okur Nakliyat

Edremit merkezli **Okur Nakliyat** için geliştirilen kurumsal, mobil uyumlu ve
dönüşüm odaklı statik web sitesi.

- **Alan adı:** https://okurnakliyatedremit.com
- **Telefon / WhatsApp:** +90 537 226 50 43
- **Hizmet alanı:** Edremit, Balıkesir ve Türkiye geneli
- **Ana hizmetler:** evden eve, şehirler arası, ofis ve parça eşya taşıma
- **Ek destek:** ücretsiz kurulum ve montaj

## Teknoloji

Derleme adımı veya sunucu tarafı uygulama gerekmez.

- Semantic HTML5
- Modern CSS3
- Vanilla JavaScript
- GitHub Actions ile FTPS dağıtımı
- Apache / cPanel `.htaccess` üretim ayarları
- Bootstrap, Tailwind, React, jQuery ve PHP yok


## Responsive denetim

Projede Playwright tabanlı bir denetim koşucusu bulunur. 16 cihaz ölçüsü, üç
yatay (landscape) senaryo ve 320–2560 px arası 80 px adımlı 29 ara genişlikte
yatay taşma, metin kesilmesi, 44px altı
dokunma hedefi, görsel oran bozulması, öğe çakışması, konsol hatası ve kırık
asset kontrolü yapar.

```bash
npm install                      # yalnızca ilk kullanımda (playwright)
npx playwright install chromium  # tarayıcı ikilisi
npm run serve                    # ayrı terminalde: http://localhost:8099
npm run test:responsive          # ekran görüntüsü için: npm run test:responsive:shot
```

`package.json` yalnızca geliştirme araçları içindir; sitede çalışma zamanı
bağımlılığı yoktur ve sunucuya yalnızca statik dosyalar gönderilir.

Sonuçlar: `docs/responsive-ui-audit.md` ve `docs/final-ui-report.md`.

## Tasarım yaklaşımı

Tasarım; sarı, siyah ve antrasit marka paleti üzerinde kuruludur.

- 12 kolonlu ana yerleşim
- 8 px tabanlı boşluk ritmi
- Akışkan `clamp()` tipografi ölçeği
- Eşit kart yükseklikleri ve tutarlı köşe yarıçapları
- Sarının yalnızca vurgu, yönlendirme ve CTA için kullanılması
- Masaüstü, tablet ve mobil için ayrı yerleşim kırılımları
- Hareket azaltma tercihi için `prefers-reduced-motion`

Tasarım tokenleri `assets/css/variables.css`, ortak bileşenler
`assets/css/components.css`, bölüm yerleşimleri ise `assets/css/style.css`
içindedir.

## Ana sayfa bölümleri

1. Sabit header ve erişilebilir mobil menü
2. Hero ve güven göstergeleri
3. Altı hizmet kartı
4. Hakkımızda / neden biz
5. Dört adımlı taşıma süreci
6. Türkiye geneli hizmet haritası
7. Sık sorulan sorular
8. WhatsApp teklif formu
9. Telefon / WhatsApp CTA bandı
10. Kurumsal footer ve mobil hızlı iletişim çubuğu

## Etkileşimler

`assets/js/main.js` aşağıdaki davranışları yönetir:

- Header scroll durumu
- Mobil menü, ESC ile kapatma ve focus trap
- Bölüm bağlantılarında yumuşak kaydırma
- Görünen bölüme göre aktif menü bağlantısı
- Düşük yoğunluklu hero parallax
- Scroll reveal animasyonları
- Tek açık öğeli SSS
- Form verilerinden WhatsApp teklif mesajı oluşturma
- Otomatik telif yılı

Form verileri sunucuya gönderilmez veya depolanmaz.

## SEO ve üretim dosyaları

- Canonical URL
- Open Graph ve Twitter Card etiketleri
- `MovingCompany` Schema.org verisi
- `robots.txt`
- `sitemap.xml`
- Özel `404.html`
- HTTP → HTTPS ve `www` → kanonik alan adı yönlendirmesi
- Gzip / Brotli sıkıştırma
- Statik varlık önbelleği
- Temel güvenlik başlıkları

## Klasör yapısı

```text
/
├── index.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── .htaccess
├── assets/
│   ├── css/
│   │   ├── reset.css
│   │   ├── variables.css
│   │   ├── components.css
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── gallery/
│       ├── hero/
│       ├── logo/
│       └── og/
├── galeri-kaynak/
│   └── liste.json
├── tools/
│   ├── galeri-goruntu.py
│   └── sayfa.py
├── .github/workflows/
│   ├── deploy.yml
│   ├── site-check.yml
│   └── htaccess-test.yml
├── DEPLOY.md
└── README.md
```

## Yerel geliştirme

```bash
python3 -m http.server 8000
```

Ardından:

```text
http://localhost:8000
```

Statik dosya sürümleri `index.html` içinde sorgu etiketiyle yönetilir:

```html
<link rel="stylesheet" href="assets/css/style.css?v=3">
<script defer src="assets/js/main.js?v=3"></script>
```

CSS veya JavaScript değiştiğinde sürüm numarası artırılmalıdır.

## Yayına alma — standart prosedür

**GitHub `main` dalı üretim için tek kaynak kabul edilir. Normal yayın sırasında
cPanel File Manager veya ayrı bir FTP istemcisiyle elle dosya yüklenmez.**

1. Site değişikliği bir branch/PR üzerinde hazırlanır veya GitHub üzerinden
   doğrudan doğru dosyalar güncellenir.
2. Değişiklik `main` dalına geldiğinde `.github/workflows/deploy.yml`
   otomatik olarak **Yayına al (FTP)** iş akışını başlatır.
3. İş akışı `python3 tools/sayfa.py` ile bütün site sayfalarını yeniden üretir.
   `index.html` veya `galeri/index.html` gibi üretilen sayfaları yalnızca yayın
   almak için elle düzenlemeye gerek yoktur.
4. Yayın paketi `dist/` altında hazırlanır ve FTPS ile cPanel
   `public_html/` dizinine aktarılır.
5. Ardından sunucudaki dosyalar ve canlı HTTP yanıtları doğrulanır.
6. Yayın ancak GitHub Actions'taki **Yayına al (FTP)** işi yeşil ve ilgili
   commit üzerindeki **`deploy/ftp-live` = `success`** olduğunda tamamlanmış
   kabul edilir.

### Yayın başlamazsa

Normal bir `main` push/merge işleminden sonra iş akışı başlamadıysa **boş
`noop`, deploy-trigger veya zaman damgası commit'i oluşturmayın.** Bunun yerine:

```text
GitHub → Actions → Yayına al (FTP) → Run workflow
Branch: main
→ Run workflow
```

Bu manuel çalıştırma da aynı üretim + FTPS + sunucu doğrulama adımlarını uygular.

### Yayın sırasında yapılmaması gerekenler

- `public_html/` içine elle aynı site dosyalarını kopyalamayın.
- Sadece yayını tetiklemek için sahte/değişiklik içermeyen commit oluşturmayın.
- `index.html` veya `galeri/index.html` dosyasını yalnızca çıktı almak için elle
  düzenlemeyin; bunları `tools/sayfa.py` üretir.
- Actions kırmızıysa canlı sitenin güncellendiğini varsaymayın; önce hata
  adımını çözün ve yeniden çalıştırın.

Hosting yapısı ve ayrıntılı teşhis adımları için [`DEPLOY.md`](DEPLOY.md)
dosyasına bakın.

## Galeriye yeni fotoğraf ekleme

Galeride iki parça birlikte güncellenmelidir:

1. Görsel dosyaları
2. `galeri-kaynak/liste.json` içindeki fotoğraf kaydı

**Yalnızca WebP dosyalarını yüklemek yeterli değildir.** `liste.json` içinde
aynı `no` değeriyle kayıt bulunmazsa `tools/sayfa.py` o görseli ana sayfa ve
`/galeri/` HTML'ine eklemez.

### Yöntem A — ham fotoğraftan üretim (tercih edilen)

Yeni fotoğrafın başına sıra numarası koyun. Örnek:

```text
galeri-kaynak/07-yukleme.jpg
```

Ardından `galeri-kaynak/liste.json` içindeki `fotograflar` dizisine aynı
numarayla açıklama ve alt metin ekleyin:

```json
{
  "no": 7,
  "aciklama": "Fotoğrafın kısa ve doğal açıklaması",
  "alt": "Görseli erişilebilir biçimde tarif eden alt metin"
}
```

Responsive WebP çıktıları yerelde üretilir:

```bash
python3 tools/galeri-goruntu.py --temiz
```

Araç her fotoğraf için 4:3 oranında şu üç dosyayı üretir:

```text
assets/images/gallery/okur-nakliyat-galeri-07-600.webp   # 600×450
assets/images/gallery/okur-nakliyat-galeri-07-900.webp   # 900×675
assets/images/gallery/okur-nakliyat-galeri-07-1400.webp  # 1400×1050
```

Kaynak fotoğraf, `liste.json` ve üretilen üç WebP birlikte commit edilmelidir.

### Yöntem B — hazır WebP dosyalarını doğrudan ekleme

Fotoğraflar önceden hazırlanmışsa ham kaynak zorunlu değildir. Ancak aynı
numara için **600, 900 ve 1400** genişliklerinin üçü de şu adlarla eklenmelidir:

```text
assets/images/gallery/okur-nakliyat-galeri-NN-600.webp
assets/images/gallery/okur-nakliyat-galeri-NN-900.webp
assets/images/gallery/okur-nakliyat-galeri-NN-1400.webp
```

Sonra mutlaka `galeri-kaynak/liste.json` içine aynı `NN` numarası eklenmelidir.
`tools/galeri-goruntu.py --temiz`, `liste.json` içinde kayıtlı numaralara ait
hazır WebP dosyalarını korur; sadece listeden çıkarılmış eski numaraların
çıktılarını temizler.

### Galeri yayın kontrol listesi

Yeni galeri fotoğrafı için `main`e göndermeden önce:

- `liste.json` içinde benzersiz bir `no` var.
- `aciklama` ve `alt` alanları boş değil.
- Aynı numara için `-600.webp`, `-900.webp` ve `-1400.webp` mevcut.
- Dosya adındaki numara ile `liste.json` içindeki `no` aynı.
- Yeni numarası daha büyük olan görselin galeride daha önce görüneceği biliniyor.
- `main`e push/merge sonrası **Yayına al (FTP)** yeşil.
- Son committe **`deploy/ftp-live` = `success`**.

Bu adımlar tamamlandığında `tools/sayfa.py` ana sayfa galeri önizlemesini ve
`/galeri/` sayfasını otomatik olarak yeniden oluşturur ve deploy iş akışı bunları
cPanel'e yayınlar.

## Kontrol

GitHub Actions içindeki **Site kontrolü** işi aşağıdakileri doğrular:

- DNS ve SSL
- HTTP → HTTPS yönlendirmesi
- Kritik varlıkların HTTP 200 yanıtı
- Özel 404 davranışı
- Güvenlik ve önbellek başlıkları
- Tüm ana sayfa bölümlerinin canlı HTML içinde bulunması
- Telefon, WhatsApp ve teklif formu bağlantıları

## Erişilebilirlik

- Tek `h1`
- Semantic `header`, `nav`, `main`, `section`, `footer`
- İçeriğe geç bağlantısı
- Klavye odak göstergeleri
- Mobil menüde odak yönetimi
- SSS için doğal `details / summary` yapısı
- Dekoratif SVG'lerde `aria-hidden`
- Hareket azaltma desteği

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
│       ├── hero/
│       ├── logo/
│       └── og/
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

## Yayına alma

`main` dalına gelen her push `.github/workflows/deploy.yml` iş akışını tetikler.
Yayın yalnızca gerekli site dosyalarını GoDaddy cPanel üzerindeki doğrulanmış
belge köküne FTPS ile aktarır.

Hosting yapısı ve teşhis adımları için [`DEPLOY.md`](DEPLOY.md) dosyasına bakın.

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

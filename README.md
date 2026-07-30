# Okur Nakliyat

Edremit merkezli nakliyat firması **Okur Nakliyat** için kurumsal web sitesi.
Şehir içi, şehirler arası ve Türkiye geneli evden eve nakliyat; ücretsiz kurulum ve montaj desteği.

- **Alan adı:** okurnakliyatedremit.com
- **Telefon / WhatsApp:** +90 537 226 50 43

## Teknoloji

Harici bir CSS veya JS framework'ü kullanılmaz.

- Semantic HTML5
- Modern CSS3 (custom properties, CSS Grid, `clamp()`, `svh`)
- Vanilla JavaScript (defer ile yüklenir)
- Bootstrap / Tailwind / React / jQuery **yok**

## Klasör yapısı

```
/
├── index.html
├── assets/
│   ├── css/
│   │   ├── reset.css        # Tarayıcı sıfırlama + reduced-motion
│   │   ├── variables.css    # Tüm tasarım tokenleri (renk, ölçü, geçiş)
│   │   ├── components.css   # Yeniden kullanılabilir bileşenler
│   │   └── style.css        # Bölüm yerleşimleri, animasyonlar, responsive
│   ├── js/
│   │   └── main.js          # Header scroll, mobil menü, smooth scroll, parallax
│   ├── images/
│   │   ├── logo/            # favicon.svg
│   │   ├── hero/            # arka plan (.webp) + araç illüstrasyonu (.svg)
│   │   ├── icons/           # (boş — ikonlar inline SVG)
│   │   └── og/              # Sosyal medya paylaşım görseli
│   └── fonts/               # (boş — fontlar Google Fonts'tan)
├── tests/
│   └── responsive-audit.js  # Playwright tabanlı responsive/UI denetimi
├── docs/                    # Denetim ve görsel prompt raporları
└── README.md
```

## Responsive denetim

Projede Playwright tabanlı bir denetim koşucusu bulunur. 19 cihaz ölçüsü ve
320–2560 px arası ara genişliklerde yatay taşma, metin kesilmesi, 44px altı
dokunma hedefi, görsel oran bozulması, öğe çakışması, konsol hatası ve kırık
asset kontrolü yapar.

```bash
python3 -m http.server 8099      # proje kökünde
npx playwright install chromium  # ilk kullanımda
node tests/responsive-audit.js   # SHOT=1 ile ekran görüntüsü de alır
```

Sonuçlar: `docs/responsive-ui-audit.md` ve `docs/final-ui-report.md`.

## Geliştirme

Statik bir site olduğu için derleme adımı yoktur. Yerel olarak çalıştırmak için:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Tasarım sistemi

Tüm ortak değerler `assets/css/variables.css` içinde tanımlıdır; bileşen
dosyalarında sabit renk veya ölçü kullanılmaz.

| Token grubu | Örnek |
| --- | --- |
| Renkler | `--color-yellow: #F5C400`, `--color-black: #0B0B0B` |
| Anlamsal renkler | `--surface-dark`, `--text-on-dark-muted`, `--accent-line` |
| Tipografi | `--font-heading: Manrope`, `--font-body: Inter`, `--fs-display` |
| Boşluk | `--space-3xs` … `--space-3xl` |
| Köşe | `--radius-sm` … `--radius-pill` |
| Gölge | `--shadow-xs` … `--shadow-lg`, `--shadow-accent` |
| Geçiş | `--transition-fast/normal/slow`, `--duration-*` |
| Katman | `--z-header`, `--z-overlay`, `--z-panel` |

Sarı renk yalnızca vurgu için kullanılır: logo detayı, birincil CTA, aktif
navigasyon, güven rozetleri, rota çizgileri.

### Buton sınıfları

`.btn` + `.btn-primary` / `.btn-secondary` / `.btn-icon`, boyut için
`.btn-sm` / `.btn-lg`. Tüm butonlarda normal, hover, focus-visible, active ve
disabled durumları tanımlıdır; minimum dokunma alanı 44 × 44 px'dir.

## Bu aşamada tamamlananlar

- Proje altyapısı ve tasarım sistemi
- Header / masaüstü navigasyon + scroll durumu
- Sağdan açılan mobil menü (focus trap, ESC, overlay, scroll kilidi)
- Ana sayfa hero bölümü (`#anasayfa`) — katmanlı arka plan görseli + okunabilirlik gradyanı
- Header ve hero animasyonları
- Masaüstü / tablet / mobil uyumluluk

Sonraki aşamalarda eklenecek bölümler için bağlantılar hazırdır:
`#hizmetler`, `#hakkimizda`, `#surec`, `#sss`, `#iletisim`.

## Görseller

| Dosya | Durum |
| --- | --- |
| `assets/images/hero/okur-nakliyat-hero-background.webp` | Hero arka planı: soyut Türkiye haritası, rota ağı ve yol kompozisyonu. PNG kaynaktan WebP'ye dönüştürüldü (1.43 MB → 72 KB, 1672 × 941). CSS `background-image` olarak kullanılır, `<link rel="preload">` ile öncelikli yüklenir. |
| `assets/images/hero/okur-nakliyat-hero.svg` | Proje için çizilmiş stilize araç illüstrasyonu. Marka görseli (`.webp`) hazırlandığında `index.html` içindeki `src` değeri değiştirilir. |
| `assets/images/logo/favicon.svg` | Geçici marka işareti (sarı halka + rota noktası). |
| `assets/images/og/okur-nakliyat-og.svg` | Sosyal paylaşım görseli. Yayına çıkmadan önce 1200 × 630 JPG/PNG sürümüyle değiştirilmesi önerilir; bazı platformlar SVG `og:image` desteklemez. |

Logo yazı tabanlıdır ve `index.html` içinde `.brand` bloğunda inline SVG olarak
durur; görsel logo dosyası geldiğinde yalnızca `.brand-mark` içeriği değiştirilir.

## Erişilebilirlik

- Tek `h1`, semantic `header` / `nav` / `main` / `section`
- `aria-label`, `aria-expanded`, `aria-controls`, `aria-current`
- Mobil menüde `role="dialog"`, `aria-modal`, focus trap ve odak iadesi
- Dekoratif SVG'lerde `aria-hidden="true"`
- Belirgin `:focus-visible` halkası, "İçeriğe geç" bağlantısı
- `prefers-reduced-motion` desteği (animasyonlar ve parallax devre dışı kalır)
- JavaScript kapalıyken `noscript` stili ile menü bağlantıları erişilebilir kalır

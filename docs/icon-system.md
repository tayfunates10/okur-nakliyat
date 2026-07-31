# İkon Sistemi

Bu belge, sitedeki bütün ikonların uyduğu kuralları tanımlar. Yeni bir ikon
eklenirken buradaki ölçüler kullanılmalıdır.

## Izgara

| | |
| --- | --- |
| viewBox | `0 0 24 24` |
| Canlı alan | 20 × 20 birim (her kenardan 2 birim iç boşluk) |
| Keyline'lar | Kare 20×20 · Daire ⌀20 · Dikey 18×20 · Yatay 20×18 |
| Köşe yarıçapı | Kutular için 1 birim, kalkan/rozet için 0,8–0,9 birim |
| Ortalama | Çizgi kalınlığı dahil sınır kutusunun merkezi (12, 12) olmalı |

### Ortalama kontrolü

İkonlar elle çizildiği için gözle "ortalı görünen" bir ikon aslında kaymış
olabilir. Doğrulama tarayıcıda `getBBox({ stroke: true })` ile yapılır —
`stroke: true` önemlidir, çünkü çizgi kalınlığı sınır kutusunu büyütür ve
yalnızca geometriye bakmak yanıltır.

```js
const bb = g.getBBox({ stroke: true });
const sapmaX = (bb.x + bb.width  / 2) - 12;
const sapmaY = (bb.y + bb.height / 2) - 12;
// |sapma| > 0,3 birim ise ikon kaydırılmalı
```

Bu ölçüm ilk sette 16 ikonun 8'inin kaymış olduğunu ortaya çıkardı; en kötüsü
`wrench` idi (Y ekseninde 1,89 birim, yani üstte 1,8 altta 5,58 boşluk).

Tek ızgara kullanılmasının sebebi: aynı sistemde 24 ve 48 birimlik iki ayrı
ızgara olduğunda ikonların iç oranları, köşe yarıçapları ve çizgi uçları
birbirini tutmuyordu.

## Çizim dili

Bütün ikonlar **stroke tabanlıdır**; dolgu kullanılmaz.

```html
<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">…</svg>
```

```css
.icon {
  flex: none;
  fill: none;
  stroke: currentColor;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
```

Renk `currentColor` üzerinden gelir; ikonun bulunduğu kapsayıcının `color`
değeri neyse ikon onu alır. Bu sayede aynı ikon koyu ve açık zeminde ayrı
dosya gerektirmez.

## Çizgi kalınlığı — optik denge

Çizgi kalınlığı **CSS'te, bağlama göre** verilir; SVG içine yazılmaz.

Tek bir sabit değer kullanılamaz: 24 birimlik ızgara farklı piksel
boyutlarında render edildiğinde çizgi de aynı oranda ölçeklenir. 17 px'lik bir
onay işaretiyle 36 px'lik bir süreç ikonu aynı `stroke-width` değerini
kullanırsa aradaki görünen kalınlık iki katına çıkar.

Uygulanan kural: render boyutu büyüdükçe çizgi **göreli olarak incelir**,
mutlak olarak hafifçe kalınlaşır.

| Bağlam | Render | `stroke-width` | Ekranda |
| --- | --- | --- | --- |
| `.trust-item` | 17 px | 2.12 | 1,50 px |
| `.header-phone`, `.btn`, `.floating-card-icon`, `.mobile-contact-bar` | 18 px | 2.03 | 1,52 px |
| `.btn-icon`, `.mobile-menu-phone` | 20 px | 1.87 | 1,56 px |
| `.contact-card-icon` | 23 px | 1.69 | 1,62 px |
| `.service-icon` | 31 px | 1.38 | 1,78 px |
| `.process-icon` | 36 px | 1.25 | 1,88 px |

Ekrandaki kalınlık **1,50 – 1,88 px** bandında kalıyor. Önceki durumda bu bant
1,05 – 1,70 px idi, yani %61 fark vardı ve iletişim kartı ikonları gözle
görülür biçimde soluk kalıyordu.

Yeni bir bağlam eklenirken formül:

```
stroke-width = hedefKalınlık × 24 / renderBoyutu
hedefKalınlık ≈ 1,50 + 0,02 × (renderBoyutu − 17)
```

## Set

| Ad | Kullanım |
| --- | --- |
| `phone` | Header telefonu, mobil menü, iletişim kartı, mobil çubuk |
| `whatsapp` | İletişim kartı, mobil çubuk |
| `arrowRight` | Birincil buton okları |
| `check` | Hero güven satırı |
| `close` | Mobil menü kapatma |
| `mapPin` | Hero yüzen kartı |
| `wrench` | Hero yüzen kartı, "Ücretsiz Kurulum ve Montaj" |
| `home` | "Evden Eve Nakliyat" |
| `truck` | "Şehirler Arası Taşıma" |
| `building` | "Ofis ve İş Yeri Taşıma" |
| `package` | "Parça Eşya Taşıma" |
| `shieldBox` | "Paketleme ve Koruma" |
| `phoneCall` | Süreç 1 — "İlk Görüşme" |
| `planning` | Süreç 2 — "Planlama" |
| `boxes` | Süreç 3 — "Paketleme ve Taşıma" |
| `delivered` | Süreç 4 — "Teslim ve Kurulum" |

`package` (tek izometrik kutu) ile `boxes` (istiflenmiş üç kutu) bilinçli
olarak farklı formlardır; ikisi de aynı sayfada göründüğü için birbirine
benzemeleri istenmedi.

## Marka işareti

Logo bu sistemin parçası değildir; kendi kuralları vardır.

| | |
| --- | --- |
| viewBox | `0 0 66 36` (oran 11:6) |
| Yükseklik | Header 38 px · ≤720 px'de 32 px · mobil menü ve footer 38 px |
| Halka | Her zaman `#F5C400` — zemin ne olursa olsun sabit |
| Kamyon | `currentColor` — koyu zeminde beyaz, açık zeminde siyah |
| Ayraç | OKUR ile NAKLİYAT arasında 2 px sarı çizgi |

Kamyonun `currentColor` alması bilinçlidir: sağlanan logonun açık ve koyu zemin
(knockout) olmak üzere iki sürümü var. Renk kapsayıcıdan geldiği için tek
işaret her iki zeminde de doğru görünür, ikinci bir dosya gerekmez.

### Animasyon

- **Açılış** (yalnızca header): halka `scale(0.55) → 1` + opaklık, kamyon
  `translateX(-7px) → 0`, 100 ms gecikmeyle. Süre 0,62 sn.
- **Hover / odak** (her yerde): halka `scale(1.07)`, kamyon `translateX(2.4px)`.
  Halka ve kamyon ayrı hareket eder; tek parça döndürmek kamyonu yatırıyordu.
- `animation-fill-mode: backwards` kullanılır — animasyon bitince öğe normal
  stiline döner, böylece hover geçişleri çalışmaya devam eder.
- `prefers-reduced-motion: reduce` altında animasyon ve dönüşümlerin tamamı
  kapanır. Kuralın özgüllüğü `.site-header .brand-ring` ile eşleşecek şekilde
  yazılmıştır; aksi hâlde devreye girmiyordu.

### Favicon

`assets/images/logo/favicon.svg` yalnızca **sarı halkayı** koyu yuvarlatılmış
kare üzerinde kullanır. 16 px'te kamyon okunmuyor; koyu zemin ise açık renkli
sekmelerde halkanın kaybolmasını engelliyor.

## Kapsam dışı
- **Hizmet bölgesi haritası** (`.coverage-map`) — ikon değil, dekoratif
  haritadır; kendi `viewBox`'ını korur.

## Erişilebilirlik

Bütün ikonlar dekoratiftir ve `aria-hidden="true"` taşır; anlam her zaman
yanlarındaki metinden gelir. Tek başına anlam taşıyan bir ikon eklenirse
`aria-hidden` kaldırılıp `<title>` veya kapsayıcıya `aria-label` verilmelidir.

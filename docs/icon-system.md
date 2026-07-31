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

## Kapsam dışı

- **Marka işareti** (`.brand-mark`, 64×24 ızgara) — logo olduğu için bu sistemin
  parçası değildir.
- **Hizmet bölgesi haritası** (`.coverage-map`) — ikon değil, dekoratif
  haritadır; kendi `viewBox`'ını korur.

## Erişilebilirlik

Bütün ikonlar dekoratiftir ve `aria-hidden="true"` taşır; anlam her zaman
yanlarındaki metinden gelir. Tek başına anlam taşıyan bir ikon eklenirse
`aria-hidden` kaldırılıp `<title>` veya kapsayıcıya `aria-label` verilmelidir.

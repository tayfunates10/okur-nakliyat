# Galeri bölümü

Bölüm kurulu ama **henüz yayında değil**: fotoğraf gelmeden boş bir galeri
yayınlamanın anlamı yok. Kod tarafı hazır, eksik olan tek şey görseller.

- **Önizleme:** `docs/galeri-onizleme.html` — tarayıcıda açın. Sitenin gerçek
  CSS ve JS dosyalarını kullanır, yani gördüğünüz davranış birebir yayına
  çıkacak olan davranıştır. Oradaki fotoğraflar sitede zaten bulunan
  görseller; sadece düzeni göstermek için tekrar kullanıldı.
- `docs/` klasörü yayın klasörüne kopyalanmadığı için bu dosya siteye çıkmaz
  (bkz. `.github/workflows/deploy.yml`, "Yayın klasörünü hazırla" adımı).

## Nasıl çalışıyor

| Parça | Yer |
| --- | --- |
| Izgara ve büyütme penceresi stilleri | `assets/css/style.css` → "9. Galeri" |
| Büyütme penceresi davranışı | `assets/js/main.js` → `initializeGallery()` |
| Yayına taşınacak HTML | `docs/galeri-onizleme.html` içindeki işaretli blok |

Izgara `repeat(auto-fill, minmax(260px, 1fr))` ile kurulur: fotoğraf sayısı
değiştiğinde kırılma noktalarına dokunmak gerekmez. 1440 px'te 4, 768 px'te 2,
390 px'te 1 sütun oluyor (ölçüldü).

Her kart sabit 4:3 oranında (`aspect-ratio` + `object-fit: cover`). Bu sayede
farklı boyutlardaki fotoğraflar ızgarayı bozmaz ve yükleme sırasında sayfa
kaymaz.

Büyütme için native `<dialog>` + `showModal()` kullanılır. Odak tuzağı, Esc ile
kapanma ve arka planın inert olması tarayıcıdan gelir. Ek olarak: sol/sağ ok
tuşlarıyla gezinme, arka plana tıklayınca kapanma, kapanınca odağın tıklanan
karta geri dönmesi ve `src`'nin boşaltılması (kapalı pencere bellekte görsel
tutmasın diye).

> `reset.css` içindeki `* { margin: 0 }`, `<dialog>`'un `margin: auto` ile
> ortalanmasını iptal ediyordu; pencere sol üst köşeye yapışıyordu.
> `.gallery-lightbox` içinde `margin: auto` açıkça geri veriliyor. Bu kuralı
> silmeyin.

## Fotoğrafları hazırlarken

**Ne çekilmeli** (6–12 fotoğraf yeterli, 20'den fazlası sayfayı ağırlaştırır):

- Yüklenmiş araç ve açık kasa
- Paketleme anı: mobilya, beyaz eşya, koli
- Koruyucu malzemeyle sarılmış eşya
- Ekip çalışırken
- Yeni adreste yerleştirme / montaj
- Öncesi–sonrası aynı odadan

**Nelere dikkat edilmeli:**

- **Müşteri yüzü ve ev içi mahremiyet:** izin almadan yayınlamayın. Aile
  fotoğrafı, kimlik, fatura gibi ayrıntılar kadraja girmesin.
- **Plaka ve kapı numarası:** kendi aracınızın plakası sorun değil; üçüncü
  kişilerin aracı, apartman numarası ve zil panosu görünmesin.
- Yatay (landscape) çekim tercih edin — ızgara 4:3'e kırpıyor, dikey
  fotoğrafların üstü ve altı kesiliyor.
- Gündüz, doğal ışık. Flaşla çekilmiş karanlık kare sitede kötü duruyor.

**Bana nasıl gönderin:** ham JPG/PNG olarak, boyutu küçültmeden. Dönüştürme
işini ben yapıyorum:

| Amaç | Genişlik | Dosya adı |
| --- | --- | --- |
| Izgara (küçük ekran) | 600 px | `okur-nakliyat-galeri-01-600.webp` |
| Izgara (büyük ekran) | 900 px | `okur-nakliyat-galeri-01-900.webp` |
| Büyütme penceresi | 1400 px | `okur-nakliyat-galeri-01-1400.webp` |

Her fotoğraf için bir de **tek cümlelik açıklama** yazın ("Akçay'da 3+1 daire
taşıması, mobilya söküm ve montaj dahil" gibi). Bu cümle hem kartın üstünde
görünüyor hem de görselin `alt` metnine temel oluyor — yer adı geçmesi yerel
aramada işe yarıyor.

## Yayına alma

Fotoğraflar gelince yapılacaklar:

1. Görselleri `assets/images/gallery/` altına WebP olarak koy.
2. `docs/galeri-onizleme.html` içindeki işaretli bloğu `index.html`'e,
   hizmet bölgesi bölümünden sonra taşı; yolları `../assets/` → `assets/`
   olarak düzelt ve `srcset`/`sizes` ekle.
3. Header ve mobil menüye "Galeri" bağlantısı ekle, footer hızlı menüsüne de.
4. `?v=` numarasını artır.
5. `ImageObject` girdilerini `sitemap.xml`'e ekle.

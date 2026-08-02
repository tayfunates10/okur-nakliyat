# Galeri bölümü

Bölüm kurulu ama **henüz yayında değil**: fotoğraf gelmeden boş bir galeri
yayınlamanın anlamı yok. Kod tarafı hazır, eksik olan tek şey görseller.

## Fotoğraf eklemek — tek yerden

1. Ham fotoğrafı `galeri-kaynak/` klasörüne koyun, başına sıra numarası
   verin: `07-yukleme.jpg`.
2. `galeri-kaynak/liste.json` içindeki `fotograflar` dizisinin **sonuna**
   bir satır ekleyin:

       { "no": 7, "aciklama": "Edremit'te yükleme öncesi hazırlanan araç" }

3. `main` dalına gönderin.

Gerisi kendiliğinden olur: "Galeri görselleri" iş akışı fotoğrafa marka
bandını basıp WebP'lere çevirir, `tools/sayfa.py` ana sayfadaki bölümü ve
`/galeri/` sayfasını yeniden üretir, "Yayına al (FTP)" siteyi günceller.

**Numarası büyük olan fotoğraf en başta görünür.** Yani sona eklediğiniz
fotoğraf sitede ilk sırada çıkar.

`aciklama` hem kartın altındaki yazı hem de görselin alt metni olur; boş
bırakmayın. Farklı bir alt metin isterseniz kayda `"alt": "..."` ekleyin.

Ana sayfada ilk **6** fotoğraf ve "Tümünü gör" bağlantısı görünür;
tamamı `/galeri/` sayfasındadır. Sayı `tools/sayfa.py` içindeki
`GALERI_ONIZLEME_ADEDI` ile değişir.

Liste boşken ne ana sayfadaki bölüm ne de `/galeri/` sayfası üretilir —
boş bir galeri yayına çıkmaz. İlk fotoğraflar eklendiğinde `sitemap.xml`
dosyasına `/galeri/` satırını da eklemeyi unutmayın; `tools/sayfa.py`
çalışırken bunu hatırlatıyor.

Listeye numara ekleyip fotoğrafı koymayı unutursanız üretim hata verip
durur; sessizce eksik yayınlanmaz.

Fotoğrafın altına marka bandı (logo, telefon, adres) basan bir sürüm
vardı; bant istenmediği için kaldırıldı. Araç artık yalnızca 4:3 kırpma,
boyutlandırma ve WebP'ye çevirme yapıyor.

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

Her fotoğraf için bir de **tek cümlelik açıklama** yazın ("Akçay'da 3+1 daire
taşıması, mobilya söküm ve montaj dahil" gibi). Bu cümle hem kartın üstünde
görünüyor hem de görselin `alt` metnine temel oluyor — yer adı geçmesi yerel
aramada işe yarıyor.

## Çerçeve otomasyonu

Ham fotoğrafları `galeri-kaynak/` klasörüne koymanız yeterli. Kırpma,
çerçeveleme, boyutlandırma ve WebP dönüşümü otomatik:

    python3 tools/galeri-goruntu.py     # yerelde
    # ya da: main dalına push edin, "Galeri görselleri" iş akışı çalıştırır

Her fotoğraftan üç dosya üretilir:

| Amaç | Genişlik | Dosya adı |
| --- | --- | --- |
| Izgara (küçük ekran) | 600 px | `okur-nakliyat-galeri-01-600.webp` |
| Izgara (büyük ekran) | 900 px | `okur-nakliyat-galeri-01-900.webp` |
| Büyütme penceresi | 1400 px | `okur-nakliyat-galeri-01-1400.webp` |

`galeri-kaynak/` yayın klasörüne kopyalanmaz; sunucuya yalnızca çıktılar gider.

### Marka bandı kaldırıldı

Fotoğrafın altına logo, telefon ve adres içeren siyah-sarı bir bant basan
bir sürüm vardı (`tools/cerceve.py`). Bant istenmediği için kaldırıldı;
araç `tools/galeri-goruntu.py` adıyla yalnızca 4:3 kırpma, boyutlandırma
ve WebP'ye çevirme yapıyor. Ayarlar `tools/galeri-goruntu.json` içinde:
çıktı genişlikleri, oran ve WebP kalitesi.

### Google Business Profile

Fotoğrafları GBP'den **otomatik çekmek** bu kurulumda mümkün değil: site
tamamen statik (sunucu yok), GBP API'si OAuth istiyor ve token'ı tarayıcıda
tutmak güvenli değil. Places API ile çekmek teknik olarak mümkün ama Google'ın
şartları o fotoğrafları değiştirmeyi (çerçeve eklemeyi) ve saklamayı
yasaklıyor.

Pratik yol: aynı fotoğrafları hem `galeri-kaynak/` klasörüne koyun hem de
GBP'ye elle yükleyin. Çerçeveli çıktılar (`assets/images/gallery/`) GBP'ye
yüklemek için de uygundur — marka bilgisi görselin içinde olduğu için
paylaşıldığında iletişim bilgisi kaybolmaz.

## Yayına alma

Fotoğraflar gelince yapılacaklar:

1. Görselleri `assets/images/gallery/` altına WebP olarak koy.
2. `docs/galeri-onizleme.html` içindeki işaretli bloğu `index.html`'e,
   hizmet bölgesi bölümünden sonra taşı; yolları `../assets/` → `assets/`
   olarak düzelt ve `srcset`/`sizes` ekle.
3. Header ve mobil menüye "Galeri" bağlantısı ekle, footer hızlı menüsüne de.
4. `?v=` numarasını artır.
5. `ImageObject` girdilerini `sitemap.xml`'e ekle.

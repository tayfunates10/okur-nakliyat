# Tüm ekran boyutlarında yerleşim denetimi

19 senaryoda (16 viewport + 3 yatay) tam sayfa görüntü alındı ve her öğe
ölçüldü. Ölçülenler: yatay taşma, kırpılan metin, sabit çubukla çakışma,
44 px altı dokunma hedefi, görsel oran bozulması, kapsayıcı dışına taşan
çocuk öğe ve gutter simetrisi.

## Sonuç

| Ölçüm | Sonuç |
| --- | --- |
| `scrollWidth == clientWidth` | 19/19 ✅ |
| Gutter simetrisi (sol − sağ) | 0,0 px — tüm genişliklerde ✅ |
| 44 px altı dokunma hedefi | 0 ✅ |
| Görsel oran bozulması | 0 ✅ |
| Sayfa sonunda sabit çubuk altında kalan içerik | 0 ✅ |

## Düzeltilen

### 1. Harita kapsayıcıdan taşıyordu

Görsel bilerek büyütülüyordu — masaüstünde `width: 112%` + `translateX(-2%)`,
720 px altında ise `.coverage-map { width: 118%; margin-left: -9% }`. Amaç
tam genişlik etkisiydi ama sonuç, gerçek cihazda Türkiye'nin **batı ucunu
(Edremit'in bulunduğu yer) ve doğu ucunu kırpmaktı**. Taşma
`body { overflow-x: hidden }` tarafından yutulduğu için sayfa kaymıyor, kara
parçası görünmez oluyordu.

Her iki taşma kuralı da kaldırıldı; görsel artık kapsayıcıya tam oturuyor.
12 genişlikte ölçüldü (320 → 2560 px): görselin viewport dışına taşan
piksel sayısı **0**, kapsayıcı dışına taşan **0**, yatay kaydırma yok.

### 2. Edremit işareti yanlış konumdaydı

Halka, Edremit'in **216 px doğusunda ve 50 px güneyinde** duruyordu — kabaca
Afyon/Kütahya hizası. Konum, Türkiye anakarasının uç koordinatları
(26,0°–44,8° boylam · 35,8°–42,1° enlem) taban görselin kara sınırına
oturtularak hesaplandı; Edremit (27,024°D · 39,596°K) görselin **%8,0
solunda, %42,3 üstünde** çıkıyor.

İşaret görselin içine gömülü olduğu için CSS ile taşınamıyordu. `tools/harita.py`
eklendi:

- `tools/harita-taban.webp` — halka ve güzergâhlar silinmiş taban (kara
  parçası + şehir noktaları). Silme maskesi genişletilerek yapıldı; ilk
  denemede kenar yumuşatma pikselleri kalıp hayalet halka bırakmıştı.
- Betik her çalıştığında halkayı ve üç kesikli güzergâhı doğru konumdan
  yeniden çizer, 1300 ve 900 px WebP üretir. Konum değişirse görsel elle
  rötuşlanmaz — koordinat değiştirilip betik yeniden çalıştırılır.

Edremit kıyıda olduğu için işaretin bir kısmı denize (sarı zemine) taşıyor;
altına kara rengiyle aynı koyu disk konuldu — karada görünmez, denizin
üstünde rozet gibi okunur.

HTML'deki "EDREMİT" etiketi de yeni halkaya taşındı. Halka sol kenara yakın
olduğu için etiket ortalanmıyor; ortalansaydı görselin sol kenarından
taşardı. Sol kenarı halkanın merkezine oturur, sağa doğru uzar.

## Rapor edilen ama düzeltilmeyenler

Denetim betiği bunları işaretliyor; incelendi, hepsi tasarım gereği:

| Bulgu | Neden sorun değil |
| --- | --- |
| `.hero-background` taşması | Parallax katmanı bilerek büyük; `.hero` `overflow: hidden` ile kırpıyor. Sayfa kaymıyor. |
| `.hero-visual-image` taşması | Araç görseli kenardan bilerek taşıyor. |
| Hero şeridindeki `span`/`i` taşması | Şerit yatay kaydırılabilir; öğelerin viewport dışına çıkması beklenen davranış. |
| `.service-card` "kırpık" | Yanlış pozitif: kartın hiçbir çocuğu kutunun altına taşmıyor (ölçüldü); `scrollHeight` farkı pseudo-element kaynaklı. |
| Sabit çubuk × hero düğmeleri | Yalnız belirli kaydırma konumlarında; kaydırınca açılıyor. Sayfa sonunda örtülen içerik yok. |

## Ölçüm yönteminde bulunan hata

İlk turda tam sayfa görüntülerde harita **boş** görünüyordu ve bunu site
hatası sanmak işten değildi. Doğrudan ölçüm görselin yüklendiğini gösterince
(`complete: true`, doğru kutu boyutu) sorunun yakalama yönteminde olduğu
anlaşıldı: `loading="lazy"` görseller `fullPage` ekran görüntüsünde
boyanmıyordu.

Betik, ekran görüntüsünden önce tüm görselleri `eager`'a çevirip
`img.decode()` ile çözülmesini bekleyecek şekilde düzeltildi. Ondan sonra
alınan görüntülerde harita her boyutta görünüyor.

## Önbellek tuzağı: değişen görsel ziyaretçiye ulaşmadı

Harita yeniden çizildi, yayına alındı, denetim geçti — ama gerçek cihazda
**eski harita görünmeye devam etti**.

Sebep: `.htaccess` her `.webp/.svg/.jpg/.css/.js` dosyasına
`max-age=31536000, immutable` veriyor. `immutable`, tarayıcıya "bu URL'i bir
daha doğrulama" demek. Dosya adları ve URL'ler değişmediği için tarayıcı bir
yıl boyunca eski görseli göstermeye devam ederdi.

Bu, daha önce `components.css` için bulunup düzeltilen hatanın aynısı;
düzeltme o zaman yalnızca stil ve betiklere uygulanmış, görseller atlanmıştı.

Kalıcı çözüm iki parçalı:

1. **Önbelleklenen her varlık aynı `?v=` numarasını taşır** — stil, betik ve
   görseller. Herhangi biri değişince numara artırılır. Tek numara olduğu
   için birini unutmak zorlaşıyor.
2. **Denetim bunu artık kontrol ediyor.** `Sayfa içerik bütünlüğü` adımı
   yayındaki HTML'de `?v=` taşımayan `assets/...` bağlantısı arar; bulursa
   adım durur ve hangi dosya olduğunu yazar.

Ödünleşme: yalnız CSS değiştiğinde görseller de yeniden indirilir. Sitenin
toplam görsel yükü ~500 KB ve sürüm artışı seyrek olduğu için bu, sessizce
eski içerik sunma riskine tercih edildi.

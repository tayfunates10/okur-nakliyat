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

**Hizmet bölgesi haritasındaki "EDREMİT" etiketi yanlış konumdaydı.**

`left: 12%` etiketin **sol kenarını** oraya koyuyordu; halkanın merkezi ise
%24,6'da. Etiket halkanın ~%8,5 soluna düşüyor, işaretin adı değil bağımsız
bir yazı gibi duruyordu. Kaynak görselden ölçüldü (1300×618): halka merkezi
%24,6 soldan · %50,3 üstten, dış yarıçap ≈ %9,7 yükseklik.

Düzeltme üç parçalı:

1. `left` merkez hizasına alındı, `transform: translateX(-50%)` eklendi.
2. 1080 px üstünde görsel kapsayıcıdan geniş (%112) ve sola kaydırılmış
   olduğu için oradaki değer ayrı hesaplandı:
   `0,246 × 1,12 − 0,0224 = %25,3`. Altındaki kırılmada %24,6'ya döner.
3. Etiketin hemen solundaki şehir noktası çipin kenarından yarım kalıyordu.
   Çipin çevresindeki 14 px'lik şeritte kalan sarı piksel sayısı taranarak
   iç boşluk belirlendi (0,75em → solda 61 piksel; 1,2em → 0). Ayrıca punto
   `vw`'ye bağlı olduğu için çip 768 px'te haritanın yalnızca %11,6'sı
   kadar kalıyor ve nokta yine örtülmüyordu; `min-width: 17%` çipi haritaya
   bağladı.

Doğrulama — dört genişlikte, etiket merkezi ile halka merkezi arasındaki
yatay fark ve çipin iki yanındaki sarı piksel:

| Genişlik | Yatay fark | Sol | Sağ |
| --- | --- | --- | --- |
| 390 px | −0,01 px | 0 | 0 |
| 768 px | −0,01 px | 0 | 0 |
| 1440 px | −0,09 px | 0 | 0 |
| 2560 px | −0,09 px | 0 | 0 |

## Rapor edilen ama düzeltilmeyenler

Denetim betiği bunları işaretliyor; incelendi, hepsi tasarım gereği:

| Bulgu | Neden sorun değil |
| --- | --- |
| `.hero-background` taşması | Parallax katmanı bilerek büyük; `.hero` `overflow: hidden` ile kırpıyor. Sayfa kaymıyor. |
| `.hero-visual-image` taşması | Araç görseli kenardan bilerek taşıyor. |
| Hero şeridindeki `span`/`i` taşması | Şerit yatay kaydırılabilir; öğelerin viewport dışına çıkması beklenen davranış. |
| `.coverage-map` taşması | Tam genişlik taşma, iki yanda **simetrik** (ör. 390 px'te −16,2 / +16,2). |
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

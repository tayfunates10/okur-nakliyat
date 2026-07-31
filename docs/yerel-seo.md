# Yerel SEO

Hedef sorgular: "edremit nakliyat", "edremit evden eve nakliyat", "akçay
nakliyat", "altınoluk evden eve", "balıkesir şehirler arası nakliyat".

## Yapılanlar

### Yapısal veri (`index.html`)

Dağınık tek bir `MovingCompany` bloğu yerine, `@id` ile birbirine bağlı bir
`@graph` kuruldu:

| Düğüm | Ne işe yarıyor |
| --- | --- |
| `MovingCompany` | İşletme kimliği: ad, telefon, bölge, hizmet kataloğu |
| `WebSite` | Site düzeyi kimlik, yayıncı olarak işletmeye bağlı |
| `WebPage` | Sayfa kimliği, `about` ile işletmeye bağlı |
| `FAQPage` | 5 soru–cevap |

`FAQPage` en somut kazanç: Google bu işaretlemeyi arama sonucunda açılır
soru–cevap olarak gösterebiliyor, sonuç kutusu büyüyor. Şart olan şey,
şemadaki metnin sayfada **görünen** metinle birebir aynı olması — otomatik
kontrol edildi, 5 soru ve 5 cevapta 0 fark.

Hizmet kataloğundaki altı `Service` düğümüne `serviceType`, `description`,
`provider` ve `areaServed` eklendi.

### Hizmet bölgesi

`areaServed` on kayda çıkarıldı: Edremit, Akçay, Altınoluk, Güre, Zeytinli,
Burhaniye, Havran, Ayvalık, Balıkesir, Türkiye.

Aynı liste hizmet bölgesi bölümünde **sayfada da görünür** hale getirildi
(`.coverage-local`). Bu bilinçli: Google, yapısal verinin sayfa içeriğiyle
örtüşmesini bekliyor; yalnızca şemada geçen ama sayfada olmayan yer adları
işe yaramıyor, ters de tepebiliyor.

> Bu ilçelerden hizmet vermediğiniz varsa hem `index.html` içindeki
> `.coverage-local-list` listesinden hem de yapısal verideki `areaServed`
> dizisinden çıkarılmalı. İkisi her zaman aynı kalmalı.

### Sayfa içi

- Hero açıklamasına "Edremit merkezli evden eve nakliyat" ifadesi doğal
  biçimde yerleştirildi. Başlıklara dokunulmadı.
- Araç görselinin `alt` metni hizmet adını içerecek şekilde güncellendi.
- `sitemap.xml`: `lastmod` güncellendi, üç görsel için `image:image` girdisi
  eklendi.

## Yapılmayanlar ve nedenleri

**Uydurulmayan alanlar.** Yanlış NAP (ad–adres–telefon) bilgisi yerel
sıralamayı doğrudan düşürür; eksik alan yanlış alandan iyidir. Şu alanlar
doğrulanamadığı için hiç yazılmadı:

| Alan | Neden gerekli |
| --- | --- |
| `streetAddress` | Google Business Profile ile birebir eşleşmesi gerekiyor |
| `openingHoursSpecification` | "Şu an açık" rozeti bunu kullanıyor |
| `geo` (enlem/boylam) | Harita sonuçlarında konum doğruluğu |
| `sameAs` | Google Business Profile, Instagram, Facebook bağlantıları |
| `priceRange` | Fiyat aralığı göstergesi |

**`aggregateRating` bilerek eklenmedi.** Gerçek olmayan puan/yorum
işaretlemesi Google'ın açık ihlal listesinde; yakalandığında yapısal veri
tamamen devre dışı bırakılıyor. Puan ancak gerçek yorumlar toplandıktan
sonra eklenmeli.

**`geo.region` / `geo.placename` meta etiketleri eklenmedi.** Google bunları
yıllardır yok sayıyor; sayfaya ağırlık dışında katkısı yok.

**H1 keyword içermiyor.** Ana başlık "Eşyalarınızı değil, güveninizi
taşıyoruz." — marka cümlesi, arama terimi yok. Bu bilinçli bir seçim değil,
tasarımın mevcut hâli; değiştirmek onayınızı gerektirir. Üç seçenek:

1. Olduğu gibi kalsın — marka tonu güçlü, `<title>` zaten hedef terimi
   içeriyor.
2. İkinci satır eklensin: "Edremit evden eve nakliyat" gibi bir alt cümle.
3. Başlık değişsin: "Edremit'te evden eve nakliyat, güvenle." — SEO açısından
   en güçlüsü, marka tonu açısından en zayıfı.

## Sıradaki adım: Google Business Profile

Yerel aramada en büyük etken site değil, **Google Business Profile** (eski
adıyla Google My Business). Harita paketinde ("local pack") çıkmanın başka
yolu yok. Sitede yapılabilecekler bittikten sonra sıralamayı asıl belirleyen
şey burası.

Yapılması gerekenler:

1. `google.com/business` üzerinden işletmeyi oluşturun/talep edin.
2. Kategori: **Nakliyat şirketi** (birincil).
3. Hizmet bölgesi işletmesi olarak kurun (müşteri adrese gelmiyorsa adres
   gizlenebilir), Edremit ve çevre ilçeleri bölge olarak ekleyin.
4. Telefonu sitedekiyle **birebir aynı** yazın: `0537 226 50 43`.
5. Fotoğraf yükleyin — galeri için hazırlayacağınız fotoğrafların aynısı.
6. Tamamlanan işlerden sonra müşterilerden yorum isteyin. Yorum sayısı ve
   yeniliği, yerel sıralamanın en güçlü sinyallerinden.

Ardından **Google Search Console**'a siteyi ekleyip `sitemap.xml`'i gönderin;
hangi sorgudan geldiğinizi ancak orada görebilirsiniz.

## Doğrulama

- Yapısal veri: <https://search.google.com/test/rich-results> adresine
  `https://okurnakliyatedremit.com/` yazın. `FAQPage` ve `MovingCompany`
  hatasız görünmeli.
- SSS metni eşleşmesi: `docs/` altındaki denetim betiği sayfadaki `<details>`
  içeriğiyle şemayı karşılaştırıyor; fark çıkarsa yayınlamayın.

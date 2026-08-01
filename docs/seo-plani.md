# Çok sayfalı SEO planı — onay bekliyor

Bu bir **plan**, henüz uygulanmadı. Maddeleri ekleyip çıkarın; onaydan sonra
uygulamaya başlanacak.

Hedef: "edremit nakliyat", "edremit evden eve nakliyat", "akçay nakliyat",
"altınoluk evden eve", "balıkesir şehirler arası nakliyat" gibi sorgularda
çıkmak.

---

## Önce karar verilmesi gereken: sayfalar nasıl üretilecek?

Sitede şu an **iki** HTML dosyası var (`index.html`, `404.html`) ve derleme
adımı yok. 15+ sayfa demek, header/footer/menü kodunun her dosyada tekrar
etmesi demek — menüye bir bağlantı eklemek 15 dosya düzenlemek olur ve
birinin unutulması kaçınılmaz.

| Seçenek | Artı | Eksi |
| --- | --- | --- |
| **A. Küçük derleyici** (önerilen) | Ortak parçalar tek yerde; menü değişikliği tek dosyada. `tools/` altındaki mevcut betik düzenine uyar, dağıtım öncesi çalışır. | Bir kerelik kurulum işi |
| B. Her sayfa tam HTML | Kurulum yok | 15 dosyada tekrar; tutarsızlık kaçınılmaz |
| C. Header/footer'ı JS ile bas | Kurulum yok | Arama motoru için riskli, sayfa kayması yaratır — **önerilmiyor** |

**Öneri: A.** `tools/sayfa.py` ortak şablon + sayfa içeriklerinden statik HTML
üretir; `Yayına al` iş akışı dağıtımdan önce çalıştırır. Çıktı yine tamamen
statik, sunucu tarafında hiçbir şey değişmez.

---

## Sayfalar

Sayı değil kalite belirleyici. Birbirinin kopyası bölge sayfaları Google'ın
"doorway page" tanımına girer ve **cezalandırılır**. Bu yüzden her sayfada
gerçekten farklı içerik olmalı — aşağıdaki listede her sayfa için "sizden
gereken bilgi" ayrıca yazıldı.

### Aşama 1 — Hizmet sayfaları (6)

Bunlar en güvenli grup: hizmetler birbirinden gerçekten farklı, içerik doğal
olarak özgün olur.

| URL | Başlık | Sizden gereken |
| --- | --- | --- |
| `/evden-eve-nakliyat/` | Edremit Evden Eve Nakliyat | Tipik süreç, kaç kişilik ekip, ortalama süre |
| `/sehirler-arasi-nakliyat/` | Edremit Şehirler Arası Nakliyat | En sık gidilen 5-6 şehir |
| `/ofis-tasima/` | Edremit Ofis ve İş Yeri Taşıma | Hafta sonu/mesai dışı çalışıyor musunuz? |
| `/parca-esya-tasima/` | Parça Eşya ve Tek Parça Taşıma | Minimum tutar/koşul var mı? |
| `/paketleme-hizmeti/` | Paketleme ve Koruma | Kullandığınız malzemeler |
| `/kurulum-montaj/` | Ücretsiz Kurulum ve Montaj | Hangi mobilyalar kapsam dışı? |

### Aşama 2 — Bölge sayfaları (4)

Sadece **gerçekten yoğun çalıştığınız** yerler. Sekiz ilçeye sekiz sayfa
açmak yerine dördüne dolu sayfa açmak daha iyi sonuç verir.

| URL | Sizden gereken |
| --- | --- |
| `/edremit-nakliyat/` | — (ana pazar) |
| `/akcay-nakliyat/` | Yazlık yoğunluğu, sezon farkı |
| `/altinoluk-nakliyat/` | Site/apartman yapısı, asansör durumu |
| `/burhaniye-nakliyat/` | Edremit'e uzaklık, tipik iş türü |

> Güre, Zeytinli, Havran, Ayvalık için ayrı sayfa **açılmayacak**; ana
> sayfadaki hizmet bölgesi listesinde kalmaya devam edecekler. İsterseniz
> ekleriz ama her biri için özgün içerik gerekir.

### Aşama 3 — Destek sayfaları (4)

| URL | Neden |
| --- | --- |
| `/iletisim/` | Yerel SEO'da güçlü: NAP, harita, çalışma saatleri tek yerde |
| `/hakkimizda/` | Güven sinyali; kuruluş yılı, ekip, araç bilgisi |
| `/sikca-sorulan-sorular/` | Mevcut 5 soru + genişletilmiş sürüm, `FAQPage` şeması |
| `/nakliyat-fiyatlari/` | "nakliyat fiyatları" yüksek hacimli sorgu; fiyat vermeden "neye göre belirlenir" anlatılır |

### Aşama 4 — Yasal (2) · **atlanmamalı**

Sitede ad, telefon ve adres toplayan bir form var. Türkiye'de bu, KVKK
kapsamında aydınlatma yükümlülüğü doğurur. Bu sayfalar SEO için değil,
**yasal gereklilik** oldukları için listede.

| URL | İçerik |
| --- | --- |
| `/kvkk-aydinlatma-metni/` | Hangi veri, ne amaçla, ne kadar süre, kime aktarılıyor |
| `/gizlilik-politikasi/` | Çerez kullanımı (şu an çerez yok — bu da yazılmalı) |

> Metinleri taslak olarak hazırlarım ama **hukuki metin sorumluluğu size
> aittir**; yayına almadan önce kontrol ettirmenizi öneririm.

---

## Her sayfada standart olarak yapılacaklar

- Benzersiz `<title>` (55-60 karakter) ve `meta description` (150-160)
- Tek `<h1>`, hedef terimi doğal biçimde içeren
- `canonical`
- `BreadcrumbList` şeması (Ana Sayfa › Hizmetler › Evden Eve Nakliyat)
- Sayfaya özel `Service` veya `Place` şeması, ana `MovingCompany` düğümüne
  `@id` ile bağlı
- Sayfaya özel OG/Twitter etiketleri
- İç bağlantı: her sayfa ilgili 2-3 sayfaya bağlanır
- `sitemap.xml`'e eklenir
- Görseller `?v=` ile sürümlenir (bkz. `docs/ekran-denetimi.md`)

## Ana sayfada yapılacak değişiklikler

- Menüye "Hizmetler" açılır listesi (6 hizmet sayfası)
- Hizmet kartlarındaki "Teklif iste" bağlantıları ilgili hizmet sayfasına
- Footer'a bölge ve yasal sayfa bağlantıları
- Hizmet bölgesi listesindeki dört ilçe kendi sayfasına bağlanır

## Ölçüm

- Google Search Console'a site ve `sitemap.xml` eklenir
- Her sayfa için Rich Results Test ile şema doğrulanır
- Yayına aldıktan sonra site denetimine yeni sayfalar eklenir (200 dönüyor mu,
  başlık benzersiz mi, `?v=` eksik mi)

---

## Yapılmayacaklar ve nedenleri

| Yapılmayacak | Neden |
| --- | --- |
| Her ilçe için sayfa | Doorway page riski; Google açıkça cezalandırıyor |
| Anahtar kelime doldurma | 2010'lardan kalma; bugün zarar veriyor |
| Uydurma yorum/puan (`aggregateRating`) | Google'ın açık ihlal listesinde; yakalandığında tüm yapısal veri devre dışı kalıyor |
| Uydurma adres, çalışma saati, kuruluş yılı | Yanlış NAP yerel sıralamayı doğrudan düşürür |
| Otomatik üretilmiş blog yazıları | İnce içerik; sitenin genel kalitesini düşürür |

---

## Sizden gereken bilgiler (tek listede)

Bunlar olmadan sayfalar yarım kalır ya da uydurmak gerekir — uydurmayacağım.

1. **Açık adres** (varsa; yoksa "hizmet bölgesi işletmesi" olarak kalır)
2. **Çalışma saatleri**
3. **E-posta adresi**
4. **Kuruluş yılı / kaç yıldır bu işte olduğunuz**
5. **Araç sayısı ve tipi, ekip büyüklüğü**
6. **En sık gidilen şehirler** (şehirler arası sayfası için)
7. **Sosyal medya hesapları** (varsa — `sameAs` için)
8. **Google Business Profile** açıldı mı?
9. Yukarıdaki tablolarda sayfa başına sorulan ayrıntılar

Bilgi gelmeyen alanlar sayfalarda **hiç yazılmaz**; eksik alan, yanlış
alandan iyidir.

---

## Sıra ve tahmini kapsam

| Aşama | İçerik | Not |
| --- | --- | --- |
| 0 | `tools/sayfa.py` derleyici + şablon | Diğer her şeyin önkoşulu |
| 1 | 6 hizmet sayfası | En yüksek getiri |
| 2 | 4 bölge sayfası | Bilgi geldikçe |
| 3 | 4 destek sayfası | |
| 4 | 2 yasal sayfa | Taslak; hukuki kontrol size ait |
| 5 | Ana sayfa bağlantıları, sitemap, denetim | Kapanış |

Her aşama ayrı PR olarak açılır; onaylamadan yayına çıkmaz.

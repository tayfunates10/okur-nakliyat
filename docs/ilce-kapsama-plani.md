# İlçe kapsama planı — A–E ve G uygulandı

Aşamalar A, B, C, D, E ve G uygulandı. **F (ayrı bölge sayfaları) hâlâ
beklemede** — gerekçesi aşağıda.

Kullanıcı kararıyla iki ekleme yapıldı:

1. Hedef ifadeler şu dört biçimde kullanılıyor: **Edremit evden eve**,
   **Edremit eşya taşıma**, **Edremit şehirler arası**, **Edremit ofis
   taşıma**. Her biri kendi sayfasında `<title>`, `<h1>` ve gövde metninde
   olmak üzere üç kez, ana sayfada iki-üç kez geçiyor.
2. **Balıkesir'in yirmi ilçesinin tamamı** adıyla yazıldı: Altıeylül,
   Ayvalık, Balya, Bandırma, Bigadiç, Burhaniye, Dursunbey, Edremit, Erdek,
   Gömeç, Gönen, Havran, İvrindi, Karesi, Kepsut, Manyas, Marmara,
   Savaştepe, Sındırgı, Susurluk. "Komşu ilçeler" gibi toplu ifadeler
   kaldırıldı — arayan kişi kendi ilçesinin adını görmeli.

   İki düzeltme: "Balıkesir merkez" diye tek bir ilçe yok, merkez
   **Altıeylül** ve **Karesi** olarak ikiye ayrılmış. Ayrıca Zeytinli,
   Akçay, Güre ve Altınoluk ilçe değil, Edremit'e bağlı yerleşimler; yerel
   arama açısından önemli oldukları için ayrı grup hâlinde listeleniyorlar.

Sorun: Akçay, Altınoluk, Burhaniye gibi ilçe adları sitede neredeyse hiç
geçmiyor. "altınoluk nakliyat" arayan biri için Google'ın eşleştireceği
bağlam yok.

---

## Ölçüm — mevcut durum

Görünür metindeki geçiş sayısı (etiketler ve `<script>` blokları hariç):

| Sayfa | Edremit | Akçay | Altınoluk | Güre | Zeytinli | Burhaniye | Havran | Ayvalık |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| (ana sayfa) | 12 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| evden-eve-nakliyat | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sehirler-arasi-nakliyat | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ofis-tasima | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| parca-esya-tasima | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| paketleme-hizmeti | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kurulum-montaj | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sikca-sorulan-sorular | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| nakliyat-fiyatlari | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kvkk-aydinlatma-metni | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| gizlilik-politikasi | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

Edremit dışındaki yedi ilçenin **tek geçişi** ana sayfadaki şu listede:

```html
<ul class="coverage-local-list">
  <li>Edremit</li>
  <li>Akçay</li>
  <li>Altınoluk</li>
  …
</ul>
```

Çıplak liste maddesi. Çevresinde cümle yok, bağlantı yok, bağlam yok.

### Şemadaki tutarsızlık

| Düğüm | `areaServed` |
| --- | --- |
| İşletme (`#isletme`) | 8 ilçe + Balıkesir + Türkiye ✅ |
| Her `Service` düğümü | yalnızca `Edremit` ❌ |

İşletme "sekiz yerde hizmet veriyorum" diyor, hizmetlerin her biri "yalnızca
Edremit'te" diyor. Görünür metin de ikincisini destekliyor.

---

## Yapılacaklar

### Aşama A — Ana sayfa hizmet bölgesi bölümü

Bilgi gerekmez. Sitenin **zaten yayınladığı** "bu sekiz yerde hizmet
veriyoruz" bilgisine dayanır; yeni bir iddia üretilmez.

- Çıplak liste, her ilçe için kısa ve gerçek bir bağlam cümlesiyle
  değiştirilir (körfezdeki konumu, tipik iş türü).
- İlçe adları ilgili hizmet sayfalarına bağlanır. Şu an listede hiç bağlantı
  yok; iç bağlantı sinyali tamamen kayıp.
- Bölüm başlığı ilçe adlarını doğal olarak içerecek biçimde yeniden yazılır.

### Aşama B — Altı hizmet sayfası

Bilgi gerekmez.

- Her sayfaya "Hangi ilçelerde" bölümü eklenir; metin **hizmete özgü**
  olur, altı sayfada aynı paragraf tekrarlanmaz.
- `Service.areaServed` yalnızca `Edremit` yerine sekiz ilçeyi kapsayacak
  şekilde düzeltilir — görünür metinle şema arasındaki çelişki kapanır.

Hizmete göre doğal ayrım:

| Sayfa | İlçe bağlamı |
| --- | --- |
| Evden eve | Körfezdeki yerleşimler arası taşınma; Akçay ve Altınoluk'ta yazlık yoğunluğu |
| Şehirler arası | Edremit çıkışlı güzergâh; Burhaniye, Havran, Ayvalık'tan katılım |
| Ofis taşıma | Edremit merkez ve Burhaniye çarşı iş yerleri |
| Parça eşya | Körfez içi kısa mesafe taşımalar |
| Paketleme | Aynı kapsama, hizmetin kendisi konumdan bağımsız |
| Kurulum/montaj | Aynı kapsama |

### Aşama C — SSS sayfası

Bilgi gerekmez.

- Gerçekten sorulan türde ilçe soruları eklenir: "Altınoluk'a geliyor
  musunuz?", "Burhaniye'den İstanbul'a taşıma yapıyor musunuz?"
- `FAQPage` şemasına eklenir. **Şema metni görünür metinle birebir aynı
  olmalı** — aksi Google'ın açık ihlal listesinde.

### Aşama D — Fiyatlar sayfası

Bilgi gerekmez, **rakam verilmez**.

- "Fiyatı ne belirler" anlatılırken mesafe maddesi ilçeler üzerinden
  somutlaşır. Fiyat, tutar veya oran yazılmaz.

### Aşama E — Başlık ve açıklamalar

Seçici olunacak.

- Her `<title>`'a ilçe adı doldurmak benzersizliği ve doğallığı bozar.
- Yalnızca gerçekten anlamlı olduğu yerde, `meta description` içinde
  kullanılır.

### Aşama F — Ayrı bölge sayfaları (4) — **ertelendi**

`/edremit-nakliyat/`, `/akcay-nakliyat/`, `/altinoluk-nakliyat/`,
`/burhaniye-nakliyat/`.

Bu aşama bilinçli olarak beklemede. Birbirinin kopyası bölge sayfaları
Google'ın "doorway page" tanımına girer ve cezalandırılır. Dördü de gerçek
ve farklı içerik gerektirir; o içerik için sizden bilgi gelmeden
yazılmayacak.

**A–D aşamaları bu sayfalar olmadan da işe yarar.** Hatta önce onlar
yapılmalı: mevcut sayfalar ilçe bağlamı kazandığında, ayrı sayfa ihtiyacının
gerçekten olup olmadığı da ölçülebilir hâle gelir.

### Aşama G — Denetime ilçe kontrolü

Bu eksiklik aylardır fark edilmedi çünkü hiçbir kontrol bakmıyordu.

- Site kontrolüne, her sayfada beklenen ilçe adlarının görünür metinde
  geçip geçmediğini ölçen bir adım eklenir.
- Ölçüm Unicode duyarlı yapılır. Bu planın ilk ölçümü `grep`'in çok baytlı
  karakterleri bayt olarak eşleştirmesi yüzünden yanlış çıktı: Akçay ve
  Altınoluk "hiç geçmiyor" göründü, oysa listede vardılar.

---

## Yazılmayacaklar

| Yazılmayacak | Neden |
| --- | --- |
| Uydurma mesafe, süre, km | Doğrulanamıyor; yanlış bilgi güveni de sıralamayı da düşürür |
| "Akçay'da 200 taşıma yaptık" türü iş hacmi iddiası | Uydurma |
| Her sayfaya aynı ilçe paragrafı | Yinelenen içerik; altı sayfayı birden zayıflatır |
| Anahtar kelime doldurma ("Edremit nakliyat Edremit evden eve Edremit…") | Bugün zarar veriyor |
| İlçe adı geçen uydurma müşteri yorumu | Google'ın açık ihlal listesinde |

---

## Sizden gereken

A–D aşamaları için **hiçbir bilgi gerekmiyor**; sitenin zaten yayınladığı
kapsama bilgisine dayanıyorlar.

Şunlar gelirse içerik belirgin biçimde güçlenir:

1. Sekiz yerin hepsine gerçekten gidiyor musunuz, yoksa bazıları
   "gerekirse" mi? Yanlış kapsama iddiası, eksik olandan kötüdür.
2. Yazlık sezonunda (Akçay/Altınoluk) iş yoğunluğu gerçekten değişiyor mu?
3. Ayvalık ve Havran düzenli çalıştığınız yerler mi?

Aşama F için gereken bilgiler `docs/seo-plani.md` içinde zaten listeli.

---

## Karar noktası

**Öneri: A → G sırasıyla uygulansın, F beklesin.**

Alternatif, F'yi de şimdi yapmak; ancak ilçe başına gerçek fark
üretilemezse dört sayfa da doorway riski taşır ve mevcut sayfalara da zarar
verebilir.

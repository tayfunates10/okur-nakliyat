#!/usr/bin/env python3
"""Okur Nakliyat güvenli SEO içerik ve teknik yapı geçişi.

Bu betik yalnızca seo/guvenli-site-iyilestirmeleri dalında bir kez çalıştırılmak
üzere hazırlanmıştır. Değişiklikleri kaynak şablonlara ve sayfalara uygular;
ardından tools/sayfa.py statik çıktıları yeniden üretir.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "sayfalar"
TEMPLATES = ROOT / "sablon"

CORE_CITIES = [
    "Edremit",
    "Zeytinli",
    "Akçay",
    "Güre",
    "Altınoluk",
    "Burhaniye",
    "Gömeç",
    "Ayvalık",
    "Havran",
]

META_RE = re.compile(r"\A\s*<!--json\s*(\{.*?\})\s*-->\s*", re.S)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip("\n") + "\n", encoding="utf-8")


def load_page(path: Path) -> tuple[dict[str, Any], str]:
    text = read(path)
    match = META_RE.match(text)
    if not match:
        raise RuntimeError(f"{path}: metadata bloğu bulunamadı")
    return json.loads(match.group(1)), text[match.end():].lstrip("\n")


def save_page(path: Path, data: dict[str, Any], body: str) -> None:
    meta = json.dumps(data, ensure_ascii=False, indent=2)
    write(path, f"<!--json\n{meta}\n-->\n{body}")


def local_area_schema(include_country: bool = False) -> list[dict[str, str]]:
    areas: list[dict[str, str]] = [
        {"@type": "City", "name": city} for city in CORE_CITIES
    ]
    areas.append({"@type": "AdministrativeArea", "name": "Balıkesir"})
    if include_country:
        areas.append({"@type": "Country", "name": "Türkiye"})
    return areas


def recursive_replace(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, str):
        for old, new in replacements.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [recursive_replace(item, replacements) for item in value]
    if isinstance(value, dict):
        return {key: recursive_replace(item, replacements) for key, item in value.items()}
    return value


TEXT_REPLACEMENTS = {
    "dar merdivende zarar riski ortadan kalkıyor":
        "dar merdiven geçişlerinden kaynaklanabilecek hasar riskini azaltmaya yardımcı oluyor",
    "mobilyayı dar merdivenden geçirme riskini ortadan kaldırıyor":
        "mobilyayı dar merdivenden geçirme riskini azaltıyor",
    "zarar görme riski ortadan kalkıyor":
        "zarar görme riski azalıyor",
    "iş düzenini aksatmadan":
        "iş düzenindeki kesintiyi azaltacak biçimde",
    "iş akışını durdurmadan.":
        "iş akışındaki kesintiyi azaltacak planla.",
    "Edremit içi taşımalarda genellikle aynı gün başlayıp aynı gün bitiriyoruz.":
        "Edremit içi taşımalar, eşya miktarı ve bina erişimi uygun olduğunda aynı gün tamamlanabilir.",
    "Körfez içi kısa mesafe olduğu için taşınma çoğunlukla aynı gün tamamlanıyor.":
        "Körfez içindeki taşımalar, eşya miktarı ve bina erişimi uygun olduğunda aynı gün tamamlanabilir.",
    "Taşıma sırasında oluşan hasarların büyük kısmı, eşyanın araca girmeden önce yeterince korunmamış olmasından kaynaklanıyor. Doğru paketlenmiş bir eşya, yol ne kadar uzun olursa olsun aynı şekilde çıkıyor.":
        "Taşıma sırasında oluşabilecek çizilme, sürtünme ve darbe riskini azaltmanın en önemli adımlarından biri doğru paketlemedir. Eşyayı türüne ve güzergâha uygun malzemelerle hazırlamak, yol boyunca korunmasına yardımcı olur.",
    "İnternette \"evden eve nakliyat 5.000 TL\" gibi tek bir rakam görürseniz o rakam sizin taşınmanız için hesaplanmış değildir.":
        "İnternette tek bir sabit nakliyat fiyatı görürseniz, bu rakam sizin taşınmanızın koşullarına göre hesaplanmış olmayabilir.",
    "özel eşya koruması ya da depolama ihtiyacı":
        "özel eşya koruması ya da ek işçilik ihtiyacı",
    "Bu başlıkları WhatsApp'tan tek mesajda yazarsanız, karşılıklı soru-cevap olmadan doğrudan fiyat ve uygunluk bilgisiyle dönüş yaparız.":
        "Bu başlıkları WhatsApp'tan tek mesajda yazmanız, fiyatlandırma ve uygunluk için gereken bilgilerin büyük bölümünü tamamlar.",
    "Çok düşük tekliflerde genellikle ekip sayısı azaltılmış olur; süre uzar, hasar riski artar.":
        "Çok düşük tekliflerde ekip sayısını, paketleme kapsamını, kat farkını ve sonradan çıkabilecek ek ücretleri özellikle sorun.",
}


def clean_region_claims(body: str) -> str:
    body = re.sub(
        r"<li><strong>Havran, İvrindi, Savaştepe, Altıeylül ve Karesi</strong>\s*—.*?</li>",
        "<li><strong>Havran ve Balıkesir çevresi</strong> — uygunluk; adres, eşya miktarı ve planlanan tarihe göre ayrıca değerlendirilir.</li>",
        body,
        flags=re.S,
    )
    body = body.replace(
        """            <p class="coverage-local-intro coverage-local-ikinci">
              Edremit'ten Balıkesir merkeze uzanan hat üzerindeki ilçelere de
              taşıma yapıyoruz.
            </p>
            <ul class="coverage-local-list">
              <li>Havran</li>
              <li>İvrindi</li>
              <li>Savaştepe</li>
              <li>Altıeylül</li>
              <li>Karesi</li>
            </ul>""",
        """            <p class="coverage-local-intro coverage-local-ikinci">
              Havran ve Balıkesir çevresindeki diğer adresler için uygunluğu;
              eşya miktarı, güzergâh ve planlanan tarihe göre değerlendiriyoruz.
            </p>""",
    )
    body = body.replace(
        "Edremit Körfezi ve Edremit'ten Balıkesir merkeze uzanan hat: Edremit, Zeytinli, Akçay, Güre, Altınoluk, Burhaniye, Gömeç, Ayvalık, Havran, İvrindi, Savaştepe, Altıeylül ve Karesi.",
        "Edremit, Zeytinli, Akçay, Güre, Altınoluk, Burhaniye, Gömeç, Ayvalık ve Havran'da hizmet veriyoruz. Balıkesir çevresindeki diğer adresleri güzergâh ve tarihe göre ayrıca değerlendiriyoruz.",
    )
    return body


def update_page(path: Path) -> None:
    data, body = load_page(path)
    data = recursive_replace(data, TEXT_REPLACEMENTS)
    body = recursive_replace(body, TEXT_REPLACEMENTS)
    body = clean_region_claims(body)

    for node in data.get("sema", []):
        if node.get("@type") == "Service":
            if node.get("serviceType") == "Şehirler arası nakliyat":
                node["areaServed"] = {"@type": "Country", "name": "Türkiye"}
            else:
                node["areaServed"] = local_area_schema()

    stem = path.stem
    if stem in {"nakliyat-fiyatlari", "sikca-sorulan-sorular", "galeri"}:
        data["seritAlt"] = False
    if stem in {"kvkk-aydinlatma-metni", "gizlilik-politikasi"}:
        data["seritUst"] = False
        data["seritAlt"] = False

    if stem == "anasayfa":
        data["baslik"] = "Edremit Nakliyat | Evden Eve ve Şehirler Arası | Okur"
        data["aciklama"] = (
            "Edremit merkezli evden eve, şehirler arası, ofis ve asansörlü "
            "nakliyat. Paketleme ve ücretsiz kurulum-montaj desteği."
        )
        for node in data.get("sema", []):
            if node.get("@type") == "MovingCompany":
                node.pop("openingHoursSpecification", None)
                node["areaServed"] = local_area_schema(include_country=True)
                logo = node.get("logo")
                if isinstance(logo, dict):
                    logo["url"] = (
                        "https://okurnakliyatedremit.com/"
                        "assets/images/logo/favicon-okur.svg"
                    )
                catalog = node.get("hasOfferCatalog", {})
                for offer in catalog.get("itemListElement", []):
                    service = offer.get("itemOffered", {})
                    if service.get("serviceType") == "Şehirler arası nakliyat":
                        service["areaServed"] = {
                            "@type": "Country",
                            "name": "Türkiye",
                        }
                    else:
                        service.pop("areaServed", None)

        body = body.replace(
            """          <h1 class="hero-title" id="heroTitle">
            <span class="hero-title-line"><span>Eşyalarınızı değil,</span></span>
            <span class="hero-title-line"><span><span class="hero-title-accent">güveninizi</span> taşıyoruz.</span></span>
          </h1>""",
            """          <h1 class="hero-title" id="heroTitle">
            <span class="hero-title-line"><span>Edremit <span class="hero-title-accent">nakliyat</span></span></span>
            <span class="hero-title-line"><span>Eşyalarınızı değil, güveninizi taşıyoruz.</span></span>
          </h1>""",
        )
        body = body.replace(
            '<span class="floating-card-title">Keşif ve teklif ücretsiz</span>\n'
            '              <span class="floating-card-text">Ölçüm için ücret almıyoruz</span>',
            '<span class="floating-card-title">Ücretsiz teklif</span>\n'
            '              <span class="floating-card-text">Detayları birlikte netleştiriyoruz</span>',
        )
        body = body.replace(
            '<span class="floating-card-title">Aynı gün dönüş</span>\n'
            '              <span class="floating-card-text">Mesajınıza aynı gün yanıt</span>',
            '<span class="floating-card-title">Doğrudan iletişim</span>\n'
            '              <span class="floating-card-text">Telefon ve WhatsApp\'tan ulaşın</span>',
        )
        body = body.replace(
            '<a class="service-link" href="/evden-eve-nakliyat/">Teklif iste <span aria-hidden="true">→</span></a>\n'
            "          </article>\n"
            "        </div>",
            '<a class="service-link" href="/asansorlu-nakliyat/">Hizmeti incele <span aria-hidden="true">→</span></a>\n'
            "          </article>\n"
            "        </div>",
            1,
        )
        body = body.replace(
            "teslim tarihini önceden konuşuyoruz; aracın ne zaman yola çıkacağı ve varış\n"
            "            gününün ne olacağı baştan belli oluyor.",
            "teslim tarihini önceden konuşuyoruz; çıkış ve tahmini varış planını\n"
            "            taşıma öncesinde netleştiriyoruz.",
        )
        body = body.replace(
            "                <option>Ofis / iş yeri taşıma</option>\n"
            "                <option>Parça eşya taşıma</option>",
            "                <option>Ofis / iş yeri taşıma</option>\n"
            "                <option>Asansörlü nakliyat</option>\n"
            "                <option>Parça eşya taşıma</option>",
        )

    if stem == "evden-eve-nakliyat":
        body = body.replace(
            '            <li><a href="/paketleme-hizmeti/">Paketleme ve Koruma</a></li>',
            '            <li><a href="/asansorlu-nakliyat/">Asansörlü Nakliyat</a></li>\n'
            '            <li><a href="/paketleme-hizmeti/">Paketleme ve Koruma</a></li>',
        )

    if stem == "ofis-tasima":
        data["aciklama"] = (
            "Edremit ofis ve iş yeri taşıma: mobilya, ekipman ve evrakların "
            "iş düzenindeki kesintiyi azaltacak planla taşınması."
        )
        for node in data.get("sema", []):
            if node.get("@type") == "Service":
                node["description"] = data["aciklama"]

    if stem == "sikca-sorulan-sorular":
        data = recursive_replace(data, TEXT_REPLACEMENTS)
        body = recursive_replace(body, TEXT_REPLACEMENTS)
        body = clean_region_claims(body)

    save_page(path, data, body)


def update_templates() -> None:
    for name in ("serit.html", "serit-alt.html"):
        path = TEMPLATES / name
        text = read(path)
        text, count = re.subn(
            r'\n\s*<ul class="site-serit-liste" aria-hidden="true">.*?</ul>',
            "",
            text,
            count=1,
            flags=re.S,
        )
        if count == 0 and text.count('class="site-serit-liste"') != 1:
            raise RuntimeError(f"{path}: kayan şerit listesi beklenmedik yapıda")
        text = text.replace(
            "İçerik iki kez basılır -- ilk kopya ekranı terk ederken ikincisi\n"
            "       yerine geçer, dönüşte boşluk oluşmaz. İkinci kopya aria-hidden;\n"
            "       ekran okuyucu listeyi iki kez okumasın.",
            "İkinci görsel kopya assets/js/marquee.js tarafından çalışma anında\n"
            "       aria-hidden olarak oluşturulur; kaynak HTML'de hizmetler tekrar etmez.",
        )
        write(path, text)

    marquee_js = r"""/* Kayan şeritlerin yalnızca görsel döngü için gereken ikinci kopyasını
   tarayıcıda üretir. Kaynak HTML'de aynı hizmet/konum metni iki kez bulunmaz. */
(function () {
  "use strict";

  document.querySelectorAll(".site-serit-satir").forEach(function (row) {
    if (row.querySelector("[data-marquee-clone]")) return;

    var list = row.querySelector(".site-serit-liste");
    if (!list) return;

    var clone = list.cloneNode(true);
    clone.setAttribute("aria-hidden", "true");
    clone.setAttribute("inert", "");
    clone.setAttribute("data-marquee-clone", "true");
    row.appendChild(clone);
  });
})();
"""
    write(ROOT / "assets/js/marquee.js", marquee_js)

    taban = TEMPLATES / "taban.html"
    text = read(taban)
    text = text.replace(
        """  <link rel="preload" href="/assets/images/hero/okur-nakliyat-hero-background.webp?v={{v}}"
        as="image" type="image/webp" fetchpriority="high">

""",
        "",
    )
    if 'marquee.js?v={{v}}' not in text:
        text = text.replace(
            '  <script defer src="/assets/js/main.js?v={{v}}"></script>',
            '  <script defer src="/assets/js/main.js?v={{v}}"></script>\n'
            '  <script defer src="/assets/js/marquee.js?v={{v}}"></script>',
        )
    text = text.replace(
        "    Uydurma alan yok: adres, çalışma saati, koordinat ve puan bilgisi\n"
        "    doğrulanamadığı için hiç yazılmadı — eksik alan, yanlış alandan iyidir\n"
        "    (yanlış NAP yerel sıralamayı doğrudan düşürür).",
        "    İşletme şemasında yalnızca sitede görünür ve işletme tarafından verilen\n"
        "    bilgiler kullanılır. Doğrulanmamış puan, koordinat veya çalışma saati\n"
        "    eklenmez; eksik alan yanlış bilgiden daha güvenlidir.",
    )
    if 'name="twitter:image:alt"' not in text:
        text = text.replace(
            '  <meta name="twitter:image" content="https://okurnakliyatedremit.com/assets/images/og/okur-nakliyat-og.jpg?v={{v}}">',
            '  <meta name="twitter:image" content="https://okurnakliyatedremit.com/assets/images/og/okur-nakliyat-og.jpg?v={{v}}">\n'
            '  <meta name="twitter:image:alt" content="Okur Nakliyat hizmetleri ve iletişim bilgilerini gösteren tanıtım görseli.">',
        )
    write(taban, text)

    footer = TEMPLATES / "footer.html"
    text = read(footer)
    text = re.sub(
        r'\n\s*<!-- Hesap adresi henüz verilmedi;.*?</li>',
        "",
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace(
        '<a href="/evden-eve-nakliyat/"><span>Asansörlü Taşıma</span></a>',
        '<a href="/asansorlu-nakliyat/"><span>Asansörlü Taşıma</span></a>',
    )
    write(footer, text)


def update_generator() -> None:
    path = ROOT / "tools/sayfa.py"
    text = read(path)
    text = text.replace('ONBELLEK_SURUMU = "32"', 'ONBELLEK_SURUMU = "33"')
    marker = "    html = sablonlar[\"taban\"]\n"
    insertion = (
        "    serit_ust = sablonlar[\"serit\"] if veri.get(\"seritUst\", True) else \"\"\n"
        "    serit_alt = sablonlar[\"serit-alt\"] if veri.get(\"seritAlt\", True) else \"\"\n\n"
        "    html = sablonlar[\"taban\"]\n"
    )
    if insertion not in text:
        if marker not in text:
            raise RuntimeError("tools/sayfa.py: şerit ayarı ekleme noktası yok")
        text = text.replace(marker, insertion, 1)
    text = text.replace('("{{SERIT}}", sablonlar["serit"]),', '("{{SERIT}}", serit_ust),')
    text = text.replace(
        'html = html.replace("{{SERIT_ALT}}", sablonlar["serit-alt"])',
        'html = html.replace("{{SERIT_ALT}}", serit_alt)',
    )
    write(path, text)


ASANSOR_PAGE = r"""<!--json
{
  "slug": "asansorlu-nakliyat",
  "baslik": "Edremit Asansörlü Nakliyat | Okur Nakliyat",
  "aciklama": "Edremit ve çevresinde yüksek katlar için dış cephe asansörlü nakliyat. Bina uygunluğu, güvenli kurulum alanı ve eşya koruması önceden planlanır.",
  "kirinti": [
    [
      "Asansörlü Nakliyat",
      null
    ]
  ],
  "sema": [
    {
      "@type": "Service",
      "@id": "https://okurnakliyatedremit.com/asansorlu-nakliyat/#hizmet",
      "name": "Asansörlü Nakliyat",
      "serviceType": "Asansörlü nakliyat",
      "description": "Edremit ve çevresinde yüksek katlar için dış cephe asansörlü nakliyat. Bina uygunluğu, güvenli kurulum alanı ve eşya koruması önceden planlanır.",
      "provider": {
        "@id": "https://okurnakliyatedremit.com/#isletme"
      },
      "areaServed": []
    }
  ]
}
-->
<main id="main">

  <section class="section section-dark hizmet-hero" aria-labelledby="hizmetBaslik">
    <div class="container">
      <nav class="kirinti" aria-label="Site yolu">
        <a href="/">Ana Sayfa</a>
        <span aria-hidden="true">›</span>
        <span aria-current="page">Asansörlü Nakliyat</span>
      </nav>

      <h1 class="section-title section-title-on-dark" id="hizmetBaslik">
        Edremit
        <span>asansörlü nakliyat</span>
        yüksek katlarda kontrollü taşıma.
      </h1>

      <p class="hizmet-giris">Dış cephe taşıma asansörü, uygun binalarda eşyaların dar merdivenlerden geçirilmesini azaltarak taşıma sürecini kolaylaştırabilir. Kurulumdan önce bina cephesi, pencere veya balkon erişimi, kat bilgisi ve aracın güvenli biçimde konumlanabileceği alan birlikte değerlendirilir.</p>

      <div class="hizmet-eylem">
        <a class="btn btn-primary" href="/#teklif">Ücretsiz Teklif Al</a>
        <a class="btn btn-secondary" href="tel:+905372265043">0537 226 50 43</a>
      </div>
    </div>
  </section>

{{SERIT_ALT}}

  <section class="section section-light" aria-labelledby="surecBaslik">
    <div class="container">
      <h2 class="section-title" id="surecBaslik">Nasıl <span>planlıyoruz?</span></h2>
      <ol class="hizmet-adimlar">
        <li class="hizmet-adim">
          <h3>Bina ve cephe kontrolü</h3>
          <p>Kat, pencere veya balkon ölçüsü, bina önü erişimi ve aracın kurulacağı zemin hakkında bilgi alıyoruz. Gerekirse bina önünün fotoğrafını istiyoruz.</p>
        </li>
        <li class="hizmet-adim">
          <h3>Güvenli kurulum alanı</h3>
          <p>Asansör aracının yaklaşabileceği alanı, yaya ve araç geçişini ve bina yönetimiyle ilgili izin ihtiyacını taşıma öncesinde değerlendiriyoruz.</p>
        </li>
        <li class="hizmet-adim">
          <h3>Koruma ve taşıma</h3>
          <p>Mobilya, beyaz eşya ve kırılabilir ürünler asansöre alınmadan önce uygun malzemelerle korunuyor; yükleme sırası eşyanın boyutuna göre belirleniyor.</p>
        </li>
        <li class="hizmet-adim">
          <h3>İndirme ve yerleştirme</h3>
          <p>Eşyalar yeni adreste uygun noktadan alınarak ilgili odalara taşınıyor; taşıma kapsamında söktüğümüz uygun mobilyalar yeniden kuruluyor.</p>
        </li>
      </ol>
    </div>
  </section>

  <section class="section section-neutral" aria-labelledby="uygunlukBaslik">
    <div class="container hizmet-bilgi">
      <h2 class="section-title" id="uygunlukBaslik">Her bina için uygun mu?</h2>
      <ul class="hizmet-liste">
        <li>Bina önünde asansör aracının güvenli biçimde konumlanabileceği yeterli alan bulunmalıdır.</li>
        <li>Pencere veya balkon açıklığı eşyanın geçişine uygun olmalıdır.</li>
        <li>Elektrik hattı, ağaç, tente, dar sokak ve yoğun trafik gibi engeller önceden değerlendirilir.</li>
        <li>Hava ve zemin koşulları güvenli kuruluma uygun değilse yöntem veya tarih yeniden planlanabilir.</li>
        <li>Site ya da apartman yönetiminden izin gerekiyorsa taşıma gününden önce alınmalıdır.</li>
      </ul>
      <p class="hizmet-kapanis">Asansörlü taşımanın uygun olup olmadığını yalnızca kat sayısına bakarak söylemek doğru değildir. Bina önü ve cephe bilgilerini paylaştığınızda en uygun yöntemi birlikte belirleriz.</p>
    </div>
  </section>

  <section class="section section-light" aria-labelledby="bolgeBaslik">
    <div class="container hizmet-bilgi">
      <h2 class="section-title" id="bolgeBaslik">Hizmet bölgeleri</h2>
      <p class="hizmet-bolge-giris">Edremit merkez, Zeytinli, Akçay, Güre, Altınoluk, Burhaniye, Gömeç, Ayvalık ve Havran'daki talepleri bina ve güzergâh uygunluğuna göre planlıyoruz. Balıkesir çevresindeki diğer adresleri ayrıca değerlendiriyoruz.</p>
    </div>
  </section>

  <section class="section section-neutral" aria-labelledby="ilgiliBaslik">
    <div class="container">
      <h2 class="section-title" id="ilgiliBaslik">İlgili <span>hizmetler</span></h2>
      <ul class="hizmet-ilgili">
        <li><a href="/evden-eve-nakliyat/">Evden Eve Nakliyat</a></li>
        <li><a href="/sehirler-arasi-nakliyat/">Şehirler Arası Nakliyat</a></li>
        <li><a href="/paketleme-hizmeti/">Paketleme ve Koruma</a></li>
      </ul>
    </div>
  </section>

</main>
"""


def create_asansor_page() -> None:
    path = PAGES / "asansorlu-nakliyat.html"
    if not path.exists():
        write(path, ASANSOR_PAGE)
    update_page(path)


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = read(path).replace("<lastmod>2026-08-01</lastmod>", "<lastmod>2026-08-02</lastmod>")
    loc = "https://okurnakliyatedremit.com/asansorlu-nakliyat/"
    if loc not in text:
        block = """  <url>
    <loc>https://okurnakliyatedremit.com/asansorlu-nakliyat/</loc>
    <lastmod>2026-08-02</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
"""
        anchor = "  <url>\n    <loc>https://okurnakliyatedremit.com/evden-eve-nakliyat/</loc>"
        index = text.find(anchor)
        if index < 0:
            raise RuntimeError("sitemap.xml: ekleme noktası bulunamadı")
        text = text[:index] + block + text[index:]
    write(path, text)


def main() -> None:
    update_templates()
    update_generator()

    for page in sorted(PAGES.glob("*.html")):
        update_page(page)

    create_asansor_page()
    update_sitemap()

    print("Güvenli SEO iyileştirmeleri kaynak dosyalara uygulandı.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""İletişim sayfasını tek bilgi kartına dönüştürür ve harita butonunu düzeltir."""

from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
SAYFA = KOK / "sayfalar" / "iletisim.html"
STYLE = KOK / "assets" / "css" / "style.css"
URETICI = KOK / "tools" / "sayfa.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: beklenen parça {count} kez bulundu; 1 olmalı")
    return text.replace(old, new, 1)


def main() -> int:
    sayfa = SAYFA.read_text(encoding="utf-8")

    eski_kanallar = '''  <section class="section section-light" aria-labelledby="kanallarBaslik">
    <div class="container">
      <h2 class="section-title" id="kanallarBaslik">Bize nasıl <span>ulaşabilirsiniz?</span></h2>
      <ol class="hizmet-adimlar">
        <li class="hizmet-adim">
          <h3>Telefon</h3>
          <p>Taşıma ayrıntılarını doğrudan görüşmek için <a href="tel:+905372265043">0537 226 50 43</a> numarasını arayabilirsiniz.</p>
        </li>
        <li class="hizmet-adim">
          <h3>WhatsApp</h3>
          <p>Adres, kat, oda sayısı ve fotoğraf gibi bilgileri <a href="https://wa.me/905372265043" target="_blank" rel="noopener">WhatsApp üzerinden</a> iletebilirsiniz.</p>
        </li>
        <li class="hizmet-adim">
          <h3>İşletme konumu</h3>
          <p>ATATÜRK MAH. KALKIM CAD, 15 İÇ KAPI TOKİ SİTESİ NO: 4 Y1 NO: 112, 10300 Edremit / Balıkesir.</p>
        </li>
        <li class="hizmet-adim">
          <h3>Google Harita</h3>
          <p>İşletme profilini görüntülemek ve yol tarifi almak için <a href="https://maps.app.goo.gl/RJbrWRR5zmvahEiu8" target="_blank" rel="noopener noreferrer">Google Harita'yı açın</a>.</p>
        </li>
      </ol>
    </div>
  </section>'''

    yeni_kanallar = '''  <section class="section section-light" aria-labelledby="kanallarBaslik">
    <div class="container">
      <h2 class="section-title" id="kanallarBaslik">Tüm iletişim bilgilerimiz <span>tek yerde.</span></h2>
      <p class="hizmet-bolge-giris">Arama, WhatsApp mesajı, işletme adresi ve yol tarifi seçeneklerini aynı kart içinden kullanabilirsiniz.</p>

      <div class="iletisim-bilgi-karti" role="group" aria-label="Okur Nakliyat iletişim bilgileri">
        <div class="iletisim-bilgi-grid">
          <div class="iletisim-bilgi-oge">
            <span class="iletisim-bilgi-ikon" aria-hidden="true">
              <svg class="icon" viewBox="0 0 24 24" width="25" height="25"><path d="M5.2 3.8 8 3.2l2.1 5.1-1.9 1.5a15.5 15.5 0 0 0 6 6l1.5-1.9 5.1 2.1-.6 2.8a2.5 2.5 0 0 1-2.5 2C9.7 20.8 3.2 14.3 3.2 6.3a2.5 2.5 0 0 1 2-2.5Z"/></svg>
            </span>
            <div class="iletisim-bilgi-govde">
              <p class="iletisim-bilgi-etiket">Telefon</p>
              <a class="iletisim-bilgi-deger" href="tel:+905372265043">0537 226 50 43</a>
              <p class="iletisim-bilgi-aciklama">Taşıma ayrıntılarını doğrudan görüşmek ve ücretsiz teklif almak için arayın.</p>
              <a class="btn btn-primary btn-sm iletisim-bilgi-eylem" href="tel:+905372265043">Hemen Ara</a>
            </div>
          </div>

          <div class="iletisim-bilgi-oge">
            <span class="iletisim-bilgi-ikon" aria-hidden="true">
              <svg class="icon icon-whatsapp" viewBox="0 0 24 24" width="25" height="25"><path d="M12 2a9.7 9.7 0 0 0-8.4 14.6L2 22l5.6-1.5A9.8 9.8 0 1 0 12 2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3.3.9.9-3.2-.2-.3A8 8 0 1 1 12 19.7Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.6.1-.2.3-.6.8-.8 1-.1.2-.3.2-.5.1-1.4-.7-2.4-1.5-3.3-3-.2-.3 0-.5.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5-.1-.1-.6-1.5-.9-2-.2-.5-.5-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1.1 2.7c.1.2 1.8 2.8 4.4 3.9.6.3 1.1.4 1.5.5.6.2 1.2.2 1.7.1.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .2-1.1-.1-.1-.3-.2-.6-.3Z"/></svg>
            </span>
            <div class="iletisim-bilgi-govde">
              <p class="iletisim-bilgi-etiket">WhatsApp</p>
              <a class="iletisim-bilgi-deger" href="https://wa.me/905372265043" target="_blank" rel="noopener">Fotoğraf ve bilgileri gönderin</a>
              <p class="iletisim-bilgi-aciklama">Adres, kat, oda sayısı ve eşya fotoğraflarını tek mesajda paylaşın.</p>
              <a class="btn btn-secondary btn-on-light btn-sm iletisim-bilgi-eylem" href="https://wa.me/905372265043?text=Merhaba%20Okur%20Nakliyat%2C%20ta%C5%9F%C4%B1mac%C4%B1l%C4%B1k%20hizmetiniz%20hakk%C4%B1nda%20%C3%BCcretsiz%20fiyat%20teklifi%20almak%20istiyorum." target="_blank" rel="noopener">Mesaj Gönder</a>
            </div>
          </div>

          <div class="iletisim-bilgi-oge">
            <span class="iletisim-bilgi-ikon" aria-hidden="true">
              <svg class="icon" viewBox="0 0 24 24" width="25" height="25"><path d="M12 21s7-5.2 7-11a7 7 0 1 0-14 0c0 5.8 7 11 7 11Z"/><circle cx="12" cy="10" r="2.4"/></svg>
            </span>
            <div class="iletisim-bilgi-govde">
              <p class="iletisim-bilgi-etiket">İşletme adresi</p>
              <address class="iletisim-bilgi-adres">Atatürk Mah. Kalkım Cad. 15 İç Kapı TOKİ Sitesi No: 4 Y1 No: 112, 10300 Edremit / Balıkesir</address>
              <p class="iletisim-bilgi-aciklama">Okur Nakliyat işletme konumu Edremit merkezlidir.</p>
            </div>
          </div>

          <div class="iletisim-bilgi-oge">
            <span class="iletisim-bilgi-ikon" aria-hidden="true">
              <svg class="icon" viewBox="0 0 24 24" width="25" height="25"><path d="m4 6 5-2 6 2 5-2v14l-5 2-6-2-5 2Z"/><path d="M9 4v14M15 6v14"/></svg>
            </span>
            <div class="iletisim-bilgi-govde">
              <p class="iletisim-bilgi-etiket">Google Harita</p>
              <a class="iletisim-bilgi-deger" href="https://maps.app.goo.gl/RJbrWRR5zmvahEiu8" target="_blank" rel="noopener noreferrer">Okur Nakliyat konumunu açın</a>
              <p class="iletisim-bilgi-aciklama">İşletme profilini görüntüleyin veya bulunduğunuz yerden rota oluşturun.</p>
              <a class="btn btn-secondary btn-on-light btn-sm iletisim-bilgi-eylem" href="https://maps.app.goo.gl/RJbrWRR5zmvahEiu8" target="_blank" rel="noopener noreferrer">Yol Tarifi Al</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>'''

    sayfa = replace_once(sayfa, eski_kanallar, yeni_kanallar, "iletişim kanalları")
    sayfa = replace_once(
        sayfa,
        'class="btn btn-secondary" href="https://maps.app.goo.gl/RJbrWRR5zmvahEiu8"',
        'class="btn btn-secondary btn-on-light" href="https://maps.app.goo.gl/RJbrWRR5zmvahEiu8"',
        "harita butonu açık zemin varyantı",
    )
    SAYFA.write_text(sayfa, encoding="utf-8")

    style = STYLE.read_text(encoding="utf-8")
    sentinel = "19. İletişim sayfası tek bilgi kartı"
    if sentinel in style:
        raise SystemExit("iletişim kartı CSS bloğu zaten mevcut")

    style = style.replace("?v=34", "?v=35")
    css = r'''
/* ==========================================================================
   19. İletişim sayfası tek bilgi kartı
   --------------------------------------------------------------------------
   Telefon, WhatsApp, adres ve harita ayrı kartlar yerine tek dış yüzeyde,
   ayırıcılarla düzenlenir. Açık zeminli ikincil butonlar btn-on-light
   varyantını kullanır; beyaz yazının kaybolması engellenir.
   ========================================================================== */

.iletisim-bilgi-karti {
  margin-top: var(--space-lg);
  overflow: hidden;
  background: var(--color-white);
  border: 1px solid var(--border-card);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-card-hover);
}

.iletisim-bilgi-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.iletisim-bilgi-oge {
  display: grid;
  grid-template-columns: 54px minmax(0, 1fr);
  gap: var(--space-sm);
  min-width: 0;
  padding: clamp(1.3rem, 3vw, 2rem);
  border-bottom: 1px solid var(--border-on-light);
}

.iletisim-bilgi-oge:nth-child(odd) {
  border-right: 1px solid var(--border-on-light);
}

.iletisim-bilgi-oge:nth-last-child(-n + 2) {
  border-bottom: 0;
}

.iletisim-bilgi-ikon {
  display: grid;
  place-items: center;
  width: 54px;
  height: 54px;
  color: var(--color-black);
  background: var(--color-yellow);
  border-radius: var(--radius-md);
  box-shadow: 0 10px 24px rgba(245, 196, 0, 0.2);
}

.iletisim-bilgi-govde {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.iletisim-bilgi-etiket {
  margin: 0;
  font-family: var(--font-heading);
  font-size: var(--fs-micro);
  font-weight: var(--weight-black);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  color: var(--color-yellow-dark);
}

.iletisim-bilgi-deger,
.iletisim-bilgi-adres {
  margin-top: 0.45rem;
  font-family: var(--font-heading);
  font-size: clamp(1.05rem, 2vw, 1.3rem);
  font-weight: var(--weight-black);
  line-height: var(--leading-snug);
  color: var(--color-black);
  overflow-wrap: anywhere;
}

.iletisim-bilgi-deger:hover {
  color: var(--color-yellow-dark);
}

.iletisim-bilgi-adres {
  font-style: normal;
}

.iletisim-bilgi-aciklama {
  margin: var(--space-xs) 0 0;
  font-size: var(--fs-sm);
  color: var(--text-on-light-muted);
}

.iletisim-bilgi-eylem {
  align-self: flex-start;
  margin-top: auto;
  padding-top: 0.7rem;
}

@media (max-width: 720px) {
  .iletisim-bilgi-grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .iletisim-bilgi-oge,
  .iletisim-bilgi-oge:nth-child(odd),
  .iletisim-bilgi-oge:nth-last-child(-n + 2) {
    grid-template-columns: 46px minmax(0, 1fr);
    border-right: 0;
    border-bottom: 1px solid var(--border-on-light);
  }

  .iletisim-bilgi-oge:last-child {
    border-bottom: 0;
  }

  .iletisim-bilgi-ikon {
    width: 46px;
    height: 46px;
  }

  .iletisim-bilgi-eylem {
    width: 100%;
  }
}
'''
    STYLE.write_text(style.rstrip() + "\n\n" + css.strip() + "\n", encoding="utf-8")

    uretici = URETICI.read_text(encoding="utf-8")
    uretici = replace_once(
        uretici,
        'ONBELLEK_SURUMU = "34"',
        'ONBELLEK_SURUMU = "35"',
        "önbellek sürümü",
    )
    URETICI.write_text(uretici, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

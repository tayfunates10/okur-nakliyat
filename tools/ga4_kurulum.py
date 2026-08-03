#!/usr/bin/env python3
"""GA4 ölçümünü, izin yönetimini ve dönüşüm olaylarını projeye ekler."""

from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
OLCUM_KIMLIGI = "G-DPRPQ2YL2E"


def oku(yol: Path) -> str:
    return yol.read_text(encoding="utf-8")


def yaz(yol: Path, metin: str) -> None:
    yol.write_text(metin.rstrip("\n") + "\n", encoding="utf-8")


def degistir_bir(metin: str, eski: str, yeni: str, etiket: str) -> str:
    adet = metin.count(eski)
    if adet != 1:
        raise SystemExit(f"{etiket}: beklenen parça {adet} kez bulundu; 1 olmalı")
    return metin.replace(eski, yeni, 1)


def tabani_guncelle() -> None:
    yol = KOK / "sablon" / "taban.html"
    metin = oku(yol)

    betik_capa = '  <script defer src="/assets/js/main.js?v={{v}}"></script>'
    baslangic = f'''  <!-- Google Analytics 4: kullanıcı izin verene kadar harici etiket yüklenmez. -->
  <script>
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () {{ window.dataLayer.push(arguments); }};
    window.OKUR_ANALYTICS_ID = "{OLCUM_KIMLIGI";
    window.gtag("consent", "default", {{
      analytics_storage: "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
      wait_for_update: 500
    }});
  </script>'''
    # Yukarıdaki f-string içinde kimlik kapanışını açıkça kur; yanlış süslü
    # parantezlerin Python tarafından yorumlanmasını önle.
    baslangic = baslangic.replace(f'"{OLCUM_KIMLIGI";', f'"{OLCUM_KIMLIGI}";')
    metin = degistir_bir(
        metin,
        betik_capa,
        baslangic + "\n\n" + betik_capa,
        "GA4 başlatma bloğu",
    )

    banner = '''{{FOOTER}}

  <section class="analytics-consent" id="analyticsConsent" role="dialog"
           aria-labelledby="analyticsConsentTitle" aria-describedby="analyticsConsentText" hidden>
    <div class="analytics-consent-inner">
      <div class="analytics-consent-copy">
        <p class="analytics-consent-title" id="analyticsConsentTitle">Gizlilik tercihiniz</p>
        <p id="analyticsConsentText">Site kullanımını anlamak için Google Analytics ölçümüne izin verebilirsiniz. İzin vermediğiniz sürece Analytics etiketi yüklenmez.</p>
        <a href="/gizlilik-politikasi/">Gizlilik politikasını inceleyin</a>
      </div>
      <div class="analytics-consent-actions" aria-label="Analiz tercihi">
        <button class="btn btn-secondary btn-sm" type="button" data-analytics-consent="denied">Reddet</button>
        <button class="btn btn-primary btn-sm" type="button" data-analytics-consent="granted">İzin ver</button>
      </div>
    </div>
  </section>'''
    metin = degistir_bir(metin, "{{FOOTER}}", banner, "izin banner'ı")
    yaz(yol, metin)


def main_js_guncelle() -> None:
    yol = KOK / "assets" / "js" / "main.js"
    metin = oku(yol)

    metin = degistir_bir(
        metin,
        "   9. WhatsApp teklif formu\n",
        "   9. WhatsApp teklif formu\n   10. İzinli GA4 ve dönüşüm olayları\n",
        "main.js bölüm listesi",
    )

    analytics = r'''  var ANALYTICS_CONSENT_KEY = "okur_analytics_consent";
  var analyticsTagLoaded = false;

  function readAnalyticsConsent() {
    try {
      var value = window.localStorage.getItem(ANALYTICS_CONSENT_KEY);
      return value === "granted" || value === "denied" ? value : null;
    } catch (error) {
      return null;
    }
  }

  function writeAnalyticsConsent(value) {
    try {
      window.localStorage.setItem(ANALYTICS_CONSENT_KEY, value);
    } catch (error) {
      /* Depolama kapalıysa tercih yalnızca mevcut sayfa için uygulanır. */
    }
  }

  function updateGoogleConsent(value) {
    if (typeof window.gtag !== "function") return;

    window.gtag("consent", "update", {
      analytics_storage: value === "granted" ? "granted" : "denied",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied"
    });
  }

  function loadGoogleAnalytics() {
    if (analyticsTagLoaded) return;

    var measurementId = window.OKUR_ANALYTICS_ID;
    if (!measurementId || typeof window.gtag !== "function") return;

    analyticsTagLoaded = true;

    var script = document.createElement("script");
    script.async = true;
    script.src =
      "https://www.googletagmanager.com/gtag/js?id=" +
      encodeURIComponent(measurementId);
    document.head.appendChild(script);

    window.gtag("js", new Date());
    window.gtag("config", measurementId, {
      send_page_view: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
  }

  function clearAnalyticsCookies() {
    var hostname = window.location.hostname;
    var domains = ["", hostname, "." + hostname];

    document.cookie.split(";").forEach(function (part) {
      var name = part.split("=")[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;

      domains.forEach(function (domain) {
        var suffix = domain ? "; domain=" + domain : "";
        document.cookie =
          name + "=; Max-Age=0; path=/; SameSite=Lax" + suffix;
      });
    });
  }

  function analyticsElementLocation(element) {
    if (element.closest("header")) return "header";
    if (element.closest("footer")) return "footer";
    if (element.closest(".mobile-fixed-actions")) return "mobile_actions";
    if (element.closest(".iletisim-bilgi-karti")) return "contact_card";
    if (element.closest("#teklif")) return "quote_section";
    if (element.closest(".hizmet-hero")) return "hero";
    return "main";
  }

  function sendAnalyticsEvent(eventName, parameters) {
    if (readAnalyticsConsent() !== "granted") return;
    if (typeof window.gtag !== "function") return;

    var payload = {
      page_path: window.location.pathname,
      page_title: document.title
    };

    Object.keys(parameters || {}).forEach(function (key) {
      payload[key] = parameters[key];
    });

    window.gtag("event", eventName, payload);
  }

  function initializeAnalyticsConsent() {
    var banner = document.getElementById("analyticsConsent");
    if (!banner) return;

    var stored = readAnalyticsConsent();

    function hideBanner() {
      banner.hidden = true;
    }

    function showBanner() {
      banner.hidden = false;
      var firstButton = banner.querySelector("button");
      if (firstButton) firstButton.focus();
    }

    function applyConsent(value) {
      writeAnalyticsConsent(value);
      updateGoogleConsent(value);

      if (value === "granted") {
        loadGoogleAnalytics();
      } else {
        clearAnalyticsCookies();
      }

      hideBanner();
    }

    banner.addEventListener("click", function (event) {
      var button = event.target.closest("[data-analytics-consent]");
      if (!button) return;
      applyConsent(button.getAttribute("data-analytics-consent"));
    });

    var footerBottom = document.querySelector(".footer-bottom");
    if (footerBottom && !document.getElementById("analyticsPreferencesButton")) {
      var preferencesButton = document.createElement("button");
      preferencesButton.id = "analyticsPreferencesButton";
      preferencesButton.className = "analytics-preferences-button";
      preferencesButton.type = "button";
      preferencesButton.textContent = "Çerez tercihleri";
      preferencesButton.addEventListener("click", showBanner);
      footerBottom.appendChild(preferencesButton);
    }

    if (stored === "granted") {
      updateGoogleConsent("granted");
      loadGoogleAnalytics();
      hideBanner();
    } else if (stored === "denied") {
      updateGoogleConsent("denied");
      hideBanner();
    } else {
      showBanner();
    }
  }

  function initializeAnalyticsEvents() {
    document.addEventListener("click", function (event) {
      var link = event.target.closest("a[href]");
      if (!link) return;

      var href = String(link.getAttribute("href") || "");
      var lowerHref = href.toLowerCase();
      var eventName = null;

      if (lowerHref.indexOf("tel:") === 0) {
        eventName = "phone_click";
      } else if (
        lowerHref.indexOf("wa.me/") !== -1 ||
        lowerHref.indexOf("whatsapp.com/") !== -1
      ) {
        eventName = "whatsapp_click";
      } else if (
        lowerHref.indexOf("maps.app.goo.gl/") !== -1 ||
        lowerHref.indexOf("google.com/maps") !== -1 ||
        lowerHref.indexOf("maps.google.") !== -1
      ) {
        eventName = "directions_click";
      }

      if (!eventName) return;

      sendAnalyticsEvent(eventName, {
        link_text: String(link.textContent || "").trim().replace(/\s+/g, " ").slice(0, 100),
        link_url: href.slice(0, 500),
        element_location: analyticsElementLocation(link)
      });
    });
  }

'''
    metin = degistir_bir(
        metin,
        "  function initializeCurrentYear() {",
        analytics + "  function initializeCurrentYear() {",
        "GA4 fonksiyonları",
    )

    form_capa = '''      function value(name) {
        return String(data.get(name) || "").trim();
      }

      var lines = ['''
    form_yeni = '''      function value(name) {
        return String(data.get(name) || "").trim();
      }

      sendAnalyticsEvent("quote_submit", {
        form_id: form.id || "quoteForm",
        service_type: value("service") || "belirtilmedi",
        element_location: "quote_section"
      });

      var lines = ['''
    metin = degistir_bir(metin, form_capa, form_yeni, "teklif dönüşüm olayı")

    init_capa = '''  function initialize() {
    initializeHeaderScroll();'''
    init_yeni = '''  function initialize() {
    initializeAnalyticsConsent();
    initializeAnalyticsEvents();
    initializeHeaderScroll();'''
    metin = degistir_bir(metin, init_capa, init_yeni, "GA4 başlatma çağrıları")
    yaz(yol, metin)


def css_guncelle() -> None:
    yol = KOK / "assets" / "css" / "style.css"
    metin = oku(yol)
    metin = metin.replace("?v=35", "?v=36")

    if "21. Analytics izin paneli" in metin:
        raise SystemExit("Analytics izin paneli CSS bloğu zaten mevcut")

    ek = r'''

/* ==========================================================================
   21. Analytics izin paneli
   ========================================================================== */

.analytics-consent[hidden] {
  display: none;
}

.analytics-consent {
  position: fixed;
  left: 50%;
  bottom: max(1rem, env(safe-area-inset-bottom, 0px));
  z-index: 1400;
  width: min(720px, calc(100% - 2rem));
  transform: translateX(-50%);
  color: var(--text-on-dark);
  background: rgba(11, 11, 11, 0.97);
  border: 1px solid var(--border-on-dark-strong);
  border-radius: var(--radius-lg);
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.48);
  backdrop-filter: blur(16px);
}

.analytics-consent-inner {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: var(--space-lg);
  padding: clamp(1rem, 3vw, 1.5rem);
}

.analytics-consent-title {
  margin: 0;
  font-family: var(--font-heading);
  font-size: 1.05rem;
  font-weight: var(--weight-black);
  color: var(--color-white);
}

.analytics-consent-copy p:not(.analytics-consent-title) {
  margin: 0.45rem 0 0;
  font-size: var(--fs-sm);
  color: var(--text-on-dark-muted);
}

.analytics-consent-copy a {
  display: inline-block;
  margin-top: 0.55rem;
  color: var(--color-yellow);
  font-size: var(--fs-xs);
  font-weight: var(--weight-bold);
  text-decoration: underline;
  text-underline-offset: 0.2em;
}

.analytics-consent-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: var(--space-xs);
}

.analytics-preferences-button {
  min-height: 36px;
  padding: 0.35rem 0.65rem;
  font: inherit;
  font-size: var(--fs-xs);
  color: inherit;
  background: transparent;
  border: 0;
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 0.2em;
}

.analytics-preferences-button:hover,
.analytics-preferences-button:focus-visible {
  color: var(--color-yellow);
}

.analytics-preferences-button:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 2px;
}

@media (max-width: 720px) {
  .analytics-consent {
    bottom: calc(4.75rem + env(safe-area-inset-bottom, 0px));
    width: min(100% - 1rem, 680px);
  }

  .analytics-consent-inner {
    grid-template-columns: minmax(0, 1fr);
    gap: var(--space-md);
  }

  .analytics-consent-actions {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .analytics-consent-actions .btn {
    width: 100%;
  }
}
'''
    yaz(yol, metin.rstrip() + ek)


def gizlilik_guncelle() -> None:
    yol = KOK / "sayfalar" / "gizlilik-politikasi.html"
    metin = oku(yol)

    eski = '''        <h3>Çerez kullanılmıyor</h3>
        <p class="hizmet-kapanis">Bu site çerez (cookie) kullanmıyor. Reklam ağı, izleme pikseli ya da üçüncü taraf analiz aracı da bulunmuyor. Bu yüzden çerez onayı isteyen bir pencere de göstermiyoruz.</p>

        <h3>Form verileri sunucuya gitmiyor</h3>'''
    yeni = '''        <h3>Analiz ve çerez tercihi</h3>
        <p class="hizmet-kapanis">Site kullanımını ölçmek için Google Analytics 4 kullanılabilir. Analytics etiketi yalnızca ziyaretçi “İzin ver” seçeneğini kullandığında yüklenir; reddedildiğinde ölçüm çerezi oluşturulmaz ve dönüşüm olayları gönderilmez.</p>
        <p class="hizmet-kapanis">Tercihiniz tarayıcınızın yerel depolama alanında saklanır. Footer bölümündeki “Çerez tercihleri” düğmesiyle kararınızı daha sonra değiştirebilirsiniz. Reklam depolama, reklam kullanıcı verisi ve kişiselleştirilmiş reklam izni her durumda kapalıdır.</p>

        <h3>Form verileri sunucuya gitmiyor</h3>'''
    metin = degistir_bir(metin, eski, yeni, "gizlilik analiz açıklaması")

    eski_liste = '''        <h3>Dış bağlantılar</h3>
        <ul class="hizmet-liste">
          <li>WhatsApp bağlantıları sizi WhatsApp'a yönlendirir; orada WhatsApp'ın kendi koşulları geçerlidir.</li>
          <li>Sitenin yazı tipleri Google Fonts üzerinden yüklenir. Bu istek sırasında tarayıcınızın IP adresi Google'a ulaşır.</li>
        </ul>'''
    yeni_liste = '''        <h3>Dış hizmetler</h3>
        <ul class="hizmet-liste">
          <li>Google Analytics, yalnızca izin verildiğinde sayfa görüntüleme ile telefon, WhatsApp, yol tarifi ve teklif formu etkileşimlerini ölçer. Formdaki ad, telefon ve açıklama alanları Analytics'e gönderilmez.</li>
          <li>WhatsApp bağlantıları sizi WhatsApp'a yönlendirir; orada WhatsApp'ın kendi koşulları geçerlidir.</li>
          <li>Google Haritalar konum önizlemesi ve yol tarifi bağlantıları Google'ın hizmetlerini kullanır.</li>
          <li>Sitenin yazı tipleri Google Fonts üzerinden yüklenir. Bu istek sırasında tarayıcınızın IP adresi Google'a ulaşabilir.</li>
        </ul>'''
    metin = degistir_bir(metin, eski_liste, yeni_liste, "gizlilik dış hizmetler")
    yaz(yol, metin)


def surum_guncelle() -> None:
    yol = KOK / "tools" / "sayfa.py"
    metin = oku(yol)
    metin = degistir_bir(
        metin,
        'ONBELLEK_SURUMU = "35"',
        'ONBELLEK_SURUMU = "36"',
        "önbellek sürümü",
    )
    yaz(yol, metin)


def main() -> int:
    tabani_guncelle()
    main_js_guncelle()
    css_guncelle()
    gizlilik_guncelle()
    surum_guncelle()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

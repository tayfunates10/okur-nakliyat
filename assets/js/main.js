/* ========================================================================== 
   Okur Nakliyat — main.js
   Harici kütüphane kullanılmaz.
   1. Header kaydırma durumu
   2. Mobil menü ve odak yönetimi
   3. Yumuşak kaydırma
   4. Aktif menü bağlantısı
   5. Hero parallax ve bilgi kutuları
   6. Görünürlük animasyonları
   7. SSS davranışı
   8. Galeri büyütme penceresi
   9. WhatsApp teklif formu
   10. İzinli GA4 ve dönüşüm olayları
   ========================================================================== */

(function () {
  "use strict";

  var reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

  function prefersReducedMotion() {
    return reducedMotionQuery.matches;
  }

  function initializeHeaderScroll() {
    var header = document.getElementById("siteHeader");
    if (!header) return;

    var threshold = 24;
    var ticking = false;

    /* Kayan şerit sayfanın en başında, akışta duruyor ve sayfayla birlikte
       yukarı kayıyor. Header ise sabit; hiçbir şey yapılmazsa top=0'da
       durup şeridi baştan örter. Header, şeridin ekranda kalan yüksekliği
       kadar aşağıda tutuluyor; şerit tamamen çıkınca 0'a iniyor.
       Şerit yoksa (alt sayfalar) hiç dokunulmuyor. */
    var serit = document.querySelector(".site-serit-ust");
    var seritYuksekligi = serit ? serit.getBoundingClientRect().height : 0;
    var oncekiUst = -1;

    function updateHeaderState() {
      header.classList.toggle("is-scrolled", window.scrollY > threshold);

      if (seritYuksekligi) {
        var kalan = Math.max(0, seritYuksekligi - window.scrollY);
        /* Yalnızca değer değiştiğinde yazılır. `top`, header sabit
           konumlu olduğu için yerleşimi tetikliyor ve header kaydırınca
           `backdrop-filter: blur(16px)` kazanıyor: her karede yazmak
           bulanıklığı her karede yeniden hesaplatıyordu. Şerit yalnızca
           ilk 26px'te görünür, sonrasında değer 0'da sabit kalır. */
        if (kalan !== oncekiUst) {
          oncekiUst = kalan;
          header.style.top = kalan + "px";
        }
      }

      ticking = false;
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(updateHeaderState);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () {
      if (serit) seritYuksekligi = serit.getBoundingClientRect().height;
      onScroll();
    });
    updateHeaderState();
  }

  function initializeMobileMenu() {
    var toggle = document.getElementById("mobileMenuToggle");
    var panel = document.getElementById("mobileMenu");
    var overlay = document.getElementById("mobileMenuOverlay");
    var closeButton = document.getElementById("mobileMenuClose");

    if (!toggle || !panel || !overlay) return;

    var focusableSelector =
      'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
    var isOpen = false;
    var lastFocusedElement = null;

    panel.removeAttribute("hidden");
    overlay.removeAttribute("hidden");

    function getFocusableElements() {
      return Array.prototype.slice.call(panel.querySelectorAll(focusableSelector));
    }

    function lockBodyScroll() {
      var scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
      if (scrollbarWidth > 0) {
        document.body.style.paddingRight = scrollbarWidth + "px";
      }
      document.body.classList.add("is-menu-open");
    }

    function unlockBodyScroll() {
      document.body.classList.remove("is-menu-open");
      document.body.style.paddingRight = "";
    }

    function openMenu() {
      if (isOpen) return;
      isOpen = true;
      lastFocusedElement = document.activeElement;

      lockBodyScroll();
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Menüyü kapat");

      window.requestAnimationFrame(function () {
        var focusables = getFocusableElements();
        if (focusables.length) focusables[0].focus();
      });
    }

    function closeMenu() {
      if (!isOpen) return;
      isOpen = false;

      unlockBodyScroll();
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Menüyü aç");

      if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
        lastFocusedElement.focus();
      }
    }

    function trapFocus(event) {
      if (event.key !== "Tab") return;

      var focusables = getFocusableElements();
      if (!focusables.length) return;

      var first = focusables[0];
      var last = focusables[focusables.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    toggle.addEventListener("click", function () {
      if (isOpen) closeMenu();
      else openMenu();
    });

    overlay.addEventListener("click", closeMenu);

    if (closeButton) {
      closeButton.addEventListener("click", closeMenu);
    }

    panel.addEventListener("click", function (event) {
      if (event.target.closest("a[href]")) closeMenu();
    });

    document.addEventListener("keydown", function (event) {
      if (!isOpen) return;

      if (event.key === "Escape") {
        closeMenu();
        return;
      }

      trapFocus(event);
    });

    var desktopQuery = window.matchMedia("(min-width: 1080px)");
    var onDesktopChange = function (event) {
      if (event.matches) closeMenu();
    };

    if (typeof desktopQuery.addEventListener === "function") {
      desktopQuery.addEventListener("change", onDesktopChange);
    } else if (typeof desktopQuery.addListener === "function") {
      desktopQuery.addListener(onDesktopChange);
    }
  }

  function initializeSmoothScroll() {
    document.addEventListener("click", function (event) {
      var link = event.target.closest('a[href^="#"]');
      if (!link) return;

      var hash = link.getAttribute("href");
      if (!hash || hash === "#") return;

      var target = document.querySelector(hash);
      if (!target) return;

      event.preventDefault();

      target.scrollIntoView({
        behavior: prefersReducedMotion() ? "auto" : "smooth",
        block: "start"
      });

      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, "", hash);
      }
    });
  }

  function initializeActiveNavigation() {
    if (!("IntersectionObserver" in window)) return;

    var sections = Array.prototype.slice.call(
      document.querySelectorAll("main section[id]")
    );
    var links = Array.prototype.slice.call(
      document.querySelectorAll('.nav-link[href^="#"], .mobile-nav-link[href^="#"]')
    );

    if (!sections.length || !links.length) return;

    function setActive(id) {
      links.forEach(function (link) {
        var isActive = link.getAttribute("href") === "#" + id;
        if (isActive) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
      });
    }

    var visibleSections = new Map();

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            visibleSections.set(entry.target.id, entry.intersectionRatio);
          } else {
            visibleSections.delete(entry.target.id);
          }
        });

        var activeId = null;
        var activeRatio = -1;

        visibleSections.forEach(function (ratio, id) {
          if (ratio > activeRatio) {
            activeRatio = ratio;
            activeId = id;
          }
        });

        if (activeId) setActive(activeId);
      },
      {
        rootMargin: "-28% 0px -58% 0px",
        threshold: [0, 0.2, 0.5, 0.8]
      }
    );

    sections.forEach(function (section) {
      observer.observe(section);
    });
  }

  function initializeHeroParallax() {
    var visual = document.getElementById("heroVisual");
    var hero = document.getElementById("anasayfa");
    if (!visual || !hero) return;

    var finePointerQuery = window.matchMedia("(pointer: fine)");
    if (!finePointerQuery.matches || prefersReducedMotion()) return;

    var maxShift = 8;
    var ticking = false;
    var pointerX = 0;
    var pointerY = 0;

    function applyParallax() {
      visual.style.setProperty("--parallax-x", pointerX.toFixed(2) + "px");
      visual.style.setProperty("--parallax-y", pointerY.toFixed(2) + "px");
      ticking = false;
    }

    function onPointerMove(event) {
      var bounds = hero.getBoundingClientRect();
      var relativeX = (event.clientX - bounds.left) / bounds.width - 0.5;
      var relativeY = (event.clientY - bounds.top) / bounds.height - 0.5;

      pointerX = relativeX * maxShift * -2;
      pointerY = relativeY * maxShift * -2;

      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(applyParallax);
    }

    function resetParallax() {
      pointerX = 0;
      pointerY = 0;
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(applyParallax);
    }

    hero.addEventListener("mousemove", onPointerMove);
    hero.addEventListener("mouseleave", resetParallax);
  }

  function initializeRevealAnimations() {
    var elements = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
    if (!elements.length) return;

    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
      elements.forEach(function (element) {
        element.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        rootMargin: "0px 0px -8% 0px",
        threshold: 0.12
      }
    );

    elements.forEach(function (element, index) {
      element.style.transitionDelay = Math.min((index % 4) * 70, 210) + "ms";
      observer.observe(element);
    });
  }

  function initializeFaq() {
    var items = Array.prototype.slice.call(document.querySelectorAll(".faq-item"));
    if (!items.length) return;

    items.forEach(function (item) {
      item.addEventListener("toggle", function () {
        if (!item.open) return;

        items.forEach(function (other) {
          if (other !== item) other.removeAttribute("open");
        });
      });
    });
  }

  /*
   * Galeri büyütme penceresi.
   *
   * Native <dialog>.showModal() kullanılır: odak tuzağı, Esc ile kapanma ve
   * arka planın inert olması tarayıcıdan gelir. Elle yazılan çözümler bu
   * üçünü genelde eksik yapıyor. Odağın açılış düğmesine geri dönmesini
   * <dialog> garanti etmediği için onu biz saklıyoruz.
   *
   * Galeri bölümü sayfada yoksa fonksiyon hiçbir şey yapmadan çıkar.
   */
  function initializeGallery() {
    var dialog = document.getElementById("galleryLightbox");
    var triggers = Array.prototype.slice.call(document.querySelectorAll(".gallery-trigger"));
    if (!dialog || !triggers.length || typeof dialog.showModal !== "function") return;

    var image = document.getElementById("galleryLightboxImage");
    var caption = document.getElementById("galleryLightboxCaption");
    var counter = document.getElementById("galleryLightboxCounter");
    var prevButton = dialog.querySelector(".gallery-lightbox-prev");
    var nextButton = dialog.querySelector(".gallery-lightbox-next");
    var closeButton = dialog.querySelector(".gallery-lightbox-close");
    var lastTrigger = null;
    var current = 0;

    var single = triggers.length < 2;
    if (prevButton) prevButton.hidden = single;
    if (nextButton) nextButton.hidden = single;

    function show(index) {
      current = (index + triggers.length) % triggers.length;

      var trigger = triggers[current];
      var thumbnail = trigger.querySelector("img");

      image.src = trigger.getAttribute("data-full") || (thumbnail && thumbnail.currentSrc) || "";
      image.alt = (thumbnail && thumbnail.alt) || "";
      caption.textContent = trigger.getAttribute("data-caption") || "";
      counter.textContent = current + 1 + " / " + triggers.length;
    }

    function open(index) {
      lastTrigger = triggers[index];
      show(index);
      dialog.showModal();
      if (closeButton) closeButton.focus();
    }

    triggers.forEach(function (trigger, index) {
      trigger.addEventListener("click", function () {
        open(index);
      });
    });

    if (prevButton) {
      prevButton.addEventListener("click", function () {
        show(current - 1);
      });
    }

    if (nextButton) {
      nextButton.addEventListener("click", function () {
        show(current + 1);
      });
    }

    if (closeButton) {
      closeButton.addEventListener("click", function () {
        dialog.close();
      });
    }

    dialog.addEventListener("keydown", function (event) {
      if (single) return;
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        show(current - 1);
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        show(current + 1);
      }
    });

    /* Görselin dışına tıklayınca kapansın. <dialog>'un kendi kutusu tüm
       ekranı kaplamadığı için hedefi doğrudan dialog olan tıklama, arka
       plana (::backdrop) yapılan tıklamadır. */
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });

    dialog.addEventListener("close", function () {
      image.removeAttribute("src");
      if (lastTrigger) lastTrigger.focus();
    });
  }

  function initializeQuoteForm() {
    var form = document.getElementById("quoteForm");
    if (!form) return;

    var dateInput = form.querySelector('input[name="date"]');
    if (dateInput) {
      var today = new Date();
      var year = today.getFullYear();
      var month = String(today.getMonth() + 1).padStart(2, "0");
      var day = String(today.getDate()).padStart(2, "0");
      dateInput.min = year + "-" + month + "-" + day;
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      var data = new FormData(form);

      function value(name) {
        return String(data.get(name) || "").trim();
      }

      sendAnalyticsEvent("quote_submit", {
        form_id: form.id || "quoteForm",
        service_type: value("service") || "belirtilmedi",
        element_location: "quote_section"
      });

      var lines = [
        "Merhaba Okur Nakliyat, ücretsiz fiyat teklifi almak istiyorum.",
        "",
        "Ad Soyad: " + value("name"),
        "Telefon: " + value("phone"),
        "Nereden: " + value("from"),
        "Nereye: " + value("to"),
        "Taşıma Türü: " + value("service"),
        "Planlanan Tarih: " + (value("date") || "Belirtilmedi"),
        "Ek Bilgi: " + (value("message") || "Belirtilmedi")
      ];

      var url =
        "https://wa.me/905372265043?text=" +
        encodeURIComponent(lines.join("\n"));

      var opened = window.open(url, "_blank", "noopener,noreferrer");
      if (!opened) window.location.href = url;
    });
  }


  /* Hero bilgi kutuları: dağınık -> liste
     Kutular kamyonun çevresine dağınık başlar. Sayfa hero boyunca
     kaydırıldıkça sol kenarda düzenli bir listeye geçerler. Konumlar
     markup'ta data-dagi / data-liste ile "x,y" yüzdesi olarak duruyor;
     burada yalnızca aradaki oran hesaplanıp piksel kayması veriliyor.
     Böylece konumlar CSS/markup tarafında kalıyor. */
  /* Hero bilgi kutuları dağınık duruyor ve öyle kalıyor. Konumları
     markup'taki data-dagi içinde "x,y" yüzdesi olarak yazılı.

     Bir dönem kaydırmayla sol kenarda tek sütuna diziliyorlardı; bu
     davranış istenmediği için kaldırıldı. Masaüstünde kutular yalnızca
     fare hareketiyle (initializeHeroParallax) kıpırdıyor. */
  function initializeHeroCards() {
    var visual = document.getElementById("heroVisual");
    if (!visual) return;

    var cards = [].slice.call(visual.querySelectorAll(".floating-card[data-dagi]"));
    if (!cards.length) return;

    cards.forEach(function (card) {
      var parts = String(card.getAttribute("data-dagi") || "").split(",");
      card.style.left = (parseFloat(parts[0]) || 0) + "%";
      card.style.top = (parseFloat(parts[1]) || 0) + "%";
    });
  }

  /* Kamyonun sağdan sola, küçükten büyüyerek gelişi.

     Masaüstünde (>=1080px) sayfa açılışında, CSS animasyonuyla oluyor;
     burada hiçbir şey yazılmıyor. Daha küçük ekranlarda kamyon hero'nun
     altında kaldığı için açılışta görünmüyordu, bu yüzden kaydırmaya
     bağlanıyor: görselin merkezi ekran ortasının biraz üstüne geldiğinde
     başlıyor, "Asansörlü taşıma" kutusu header'ın hemen altına oturduğunda
     tamamlanıyor. */
  function initializeHeroTruck() {
    var visual = document.getElementById("heroVisual");
    if (!visual) return;

    var kamyon = visual.querySelector(".hero-visual-image");
    if (!kamyon || prefersReducedMotion()) return;

    var ilkKart = visual.querySelector(".floating-card");
    var header = document.getElementById("siteHeader");
    var masaustu = window.matchMedia("(min-width: 1080px)");

    var BASLANGIC = { x: -28, y: -13, olcek: 0.34 };
    var ticking = false;
    var oncekiT = -1;

    function yumusat(t) {
      return t * t * (3 - 2 * t);
    }

    function yaz(t) {
      var kx = BASLANGIC.x + (-50 - BASLANGIC.x) * t;
      var ky = BASLANGIC.y + (0 - BASLANGIC.y) * t;
      /* Ölçek %2'lik basamaklara yuvarlanıyor: 780px'lik görselin ölçeği
         her karede değişince tarayıcı onu yeniden rasterliyor ve kaydırma
         tökezliyor (ölçüldü). */
      var ko = Math.round((BASLANGIC.olcek + (1 - BASLANGIC.olcek) * t) * 50) / 50;
      kamyon.style.transform =
        "translate(" + kx.toFixed(2) + "%," + ky.toFixed(2) + "%) scale(" + ko.toFixed(2) + ")";
    }

    function update() {
      ticking = false;
      if (masaustu.matches) return;

      var kaydirma = window.pageYOffset;
      var rect = visual.getBoundingClientRect();

      // Görselin merkezi ekran yüksekliğinin %42'sine geldiğinde başlar:
      // tam ortanın biraz üstü.
      var basla = kaydirma + rect.top + rect.height / 2 - window.innerHeight * 0.42;

      // İlk kutu ("Asansörlü taşıma") header'ın altına oturunca biter.
      var kartUst = kaydirma + (ilkKart ? ilkKart.getBoundingClientRect().top : rect.top);
      var basYuksekligi = header ? header.getBoundingClientRect().height : 68;
      var bitis = kartUst - basYuksekligi;

      // Çok kısa bir yol sıçrama gibi görünür; en az 200px'lik pay bırakılır.
      if (bitis - basla < 200) basla = bitis - 200;

      var ilerleme = Math.min(1, Math.max(0, (kaydirma - basla) / (bitis - basla)));
      if (Math.abs(ilerleme - oncekiT) < 0.004) return;
      oncekiT = ilerleme;
      yaz(yumusat(ilerleme));
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }

    function kipDegisti() {
      if (masaustu.matches) {
        // Masaüstünde konumu CSS animasyonu belirler; satır içi değer silinir.
        kamyon.style.transform = "";
        oncekiT = -1;
      } else {
        oncekiT = -1;
        update();
      }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", function () {
      oncekiT = -1;
      onScroll();
    });
    window.addEventListener("load", function () {
      oncekiT = -1;
      onScroll();
    });

    if (typeof masaustu.addEventListener === "function") {
      masaustu.addEventListener("change", kipDegisti);
    } else if (typeof masaustu.addListener === "function") {
      masaustu.addListener(kipDegisti);
    }

    kipDegisti();
  }

  var ANALYTICS_CONSENT_KEY = "okur_analytics_consent";
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

  function initializeCurrentYear() {
    var element = document.getElementById("currentYear");
    if (element) element.textContent = String(new Date().getFullYear());
  }

  function initialize() {
    initializeAnalyticsConsent();
    initializeAnalyticsEvents();
    initializeHeaderScroll();
    initializeMobileMenu();
    initializeSmoothScroll();
    initializeActiveNavigation();
    initializeHeroParallax();
    initializeHeroCards();
    initializeHeroTruck();
    initializeRevealAnimations();
    initializeFaq();
    initializeGallery();
    initializeQuoteForm();
    initializeCurrentYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();

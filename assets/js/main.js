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
  function initializeHeroCards() {
    var visual = document.getElementById("heroVisual");
    if (!visual) return;

    var cards = [].slice.call(visual.querySelectorAll(".floating-card[data-dagi]"));
    if (!cards.length) return;

    function parsePair(value) {
      var parts = String(value || "").split(",");
      return { x: parseFloat(parts[0]) || 0, y: parseFloat(parts[1]) || 0 };
    }

    cards.forEach(function (card) {
      var dagi = parsePair(card.getAttribute("data-dagi"));
      card.style.left = dagi.x + "%";
      card.style.top = dagi.y + "%";
      card._dagi = dagi;
      card._liste = parsePair(card.getAttribute("data-liste"));
    });

    // Hareketi azaltma tercihi: kutular dağınık ve sabit kalır.
    if (prefersReducedMotion()) return;

    var ticking = false;
    var gorunur = true;
    var oncekiT = -1;
    var w = 0;
    var h = 0;

    /* Kamyon da aynı ilerlemeyi kullanır: kutularla eş zamanlı olarak
       sağdan sola gelir ve küçükten büyür. Başlangıç değerleri görselin
       kendi genişliğine oranla verildi; taban konum translateX(-50%). */
    var kamyon = visual.querySelector(".hero-visual-image");
    var KAMYON_BASLANGIC = { x: -28, y: -13, olcek: 0.34 };

    function olcuAl() {
      w = visual.clientWidth;
      h = visual.clientHeight;
    }

    function update() {
      ticking = false;

      /* Geçişin biteceği kaydırma mesafesi her karede yeniden hesaplanır.
         Bir kez hesaplanıp saklandığında yazı tipi geç yüklendiği için
         yerleşim kayıyor ve değer bayatlıyordu: sıralanma kamyon ekranı
         terk ederken tamamlanıyordu (ölçüldü). `kaydirma + rect.top` sabit
         olduğu için değer kaydırma boyunca zaten değişmiyor. */
      var rect = visual.getBoundingClientRect();
      var kaydirma = window.pageYOffset;
      // Kamyon ekranın ortasına geldiğinde sıralanma bitmiş olsun.
      var ortala = kaydirma + rect.top + rect.height / 2 - window.innerHeight / 2;
      /* Alt sınır: masaüstünde kamyon zaten ekranda olduğu için "ortala"
         sıfıra yakın çıkıyor ve kutular hiç dağınık görünmüyordu. Üst sınır:
         mobilde hero çok uzunsa geçiş kamyondan sonraya sarkmasın. */
      var bitis = Math.max(260, Math.min(ortala, 760));

      var ilerleme = Math.min(1, Math.max(0, kaydirma / bitis));
      if (Math.abs(ilerleme - oncekiT) < 0.002) return;
      oncekiT = ilerleme;

      /* Geçiş iki aşamalı: önce dikey, sonra yatay. Aynı anda hareket
         ettiklerinde sağdaki kutular sol sütunun üzerinden geçiyor ve yol
         boyunca üst üste biniyorlardı. Dikey konum önce oturunca her kutu
         kendi satırında kalıyor; yatay kayma artık çakışma üretmiyor. */
      var ty = yumusat(Math.min(1, ilerleme / 0.5));
      var tx = yumusat(Math.max(0, (ilerleme - 0.5) / 0.5));

      for (var i = 0; i < cards.length; i++) {
        var card = cards[i];
        var dx = ((card._liste.x - card._dagi.x) / 100) * w * tx;
        var dy = ((card._liste.y - card._dagi.y) / 100) * h * ty;
        /* Tek bir transform yazılıyor. Önce iki ayrı özel özellik (--kx/--ky)
           yazılıyordu; özel özellik değişimi kutunun alt ağacında stil yeniden
           hesabı tetiklediği için kaydırma tökezliyordu (ölçüldü). */
        card.style.transform = "translate3d(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px,0)";
      }

      if (kamyon) {
        /* Kutular iki aşamalı ilerliyor; kamyon tek eğriyle bütün yolu
           alıyor. İkisi de aynı `ilerleme` değerinden beslendiği için
           kaydırma boyunca eş zamanlı hareket ediyorlar. */
        var tk = yumusat(ilerleme);
        var kx = KAMYON_BASLANGIC.x + (-50 - KAMYON_BASLANGIC.x) * tk;
        var ky = KAMYON_BASLANGIC.y + (0 - KAMYON_BASLANGIC.y) * tk;
        var ko = KAMYON_BASLANGIC.olcek + (1 - KAMYON_BASLANGIC.olcek) * tk;
        /* Ölçek basamaklandırılıyor. Kaydırma taşıma (translate) bileşik
           iş parçacığında bedava, ama ölçek her değiştiğinde tarayıcı
           780px'lik görseli yeniden rasterlemek zorunda: her karede
           değişince kaydırma tökezliyordu (ölçüldü: düşen kare 4 -> 32).
           %4'lük basamaklarla yeniden rasterleme sayısı ~17'ye iniyor;
           taşıma sürekli olduğu için hareket yine akıcı görünüyor. */
        ko = Math.round(ko * 25) / 25;
        kamyon.style.transform =
          "translate(" + kx.toFixed(2) + "%," + ky.toFixed(2) + "%) scale(" + ko.toFixed(2) + ")";
      }
    }

    function yumusat(t) {
      return t * t * (3 - 2 * t);
    }

    function onScroll() {
      if (ticking || !gorunur) return;
      ticking = true;
      window.requestAnimationFrame(update);
    }

    function onResize() {
      olcuAl();
      oncekiT = -1;
      onScroll();
    }

    /* Hero ekrandan çıktığında kaydırma işi tamamen durur; sayfanın geri
       kalanında bu kod hiç çalışmaz. */
    if (typeof IntersectionObserver === "function") {
      new IntersectionObserver(function (girisler) {
        gorunur = girisler[0].isIntersecting;
        if (gorunur) onScroll();
      }, { rootMargin: "120px" }).observe(visual);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onResize);
    /* Ölçü DOMContentLoaded'da alınınca yazı tipi ve görseller yerleşmeden
       önce okunuyor ve "bitis" olduğundan uzun çıkıyordu: sıralanma kamyon
       ekranı terk ederken tamamlanıyordu. Yerleşim oturunca tekrar ölçülür. */
    window.addEventListener("load", onResize);
    olcuAl();
    update();
  }

  function initializeCurrentYear() {
    var element = document.getElementById("currentYear");
    if (element) element.textContent = String(new Date().getFullYear());
  }

  function initialize() {
    initializeHeaderScroll();
    initializeMobileMenu();
    initializeSmoothScroll();
    initializeActiveNavigation();
    initializeHeroParallax();
    initializeHeroCards();
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

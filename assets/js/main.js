/* ========================================================================== 
   Okur Nakliyat — main.js
   Harici kütüphane kullanılmaz.
   1. Header kaydırma durumu
   2. Mobil menü ve odak yönetimi
   3. Yumuşak kaydırma
   4. Aktif menü bağlantısı
   5. Hero parallax
   6. Görünürlük animasyonları
   7. SSS davranışı
   8. WhatsApp teklif formu
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

    function updateHeaderState() {
      header.classList.toggle("is-scrolled", window.scrollY > threshold);
      ticking = false;
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(updateHeaderState);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
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
    initializeRevealAnimations();
    initializeFaq();
    initializeQuoteForm();
    initializeCurrentYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();

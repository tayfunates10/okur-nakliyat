/* ==========================================================================
   Okur Nakliyat — main.js
   Vanilla JavaScript. Harici kütüphane kullanılmaz.
   Bölümler:
     1. initializeHeaderScroll   — kaydırmada header görünümü
     2. initializeMobileMenu     — sağdan açılan panel, odak yönetimi
     3. initializeSmoothScroll   — bölüm bağlantılarında yumuşak kaydırma
     4. initializeHeroParallax   — masaüstünde çok düşük yoğunluklu parallax
   ========================================================================== */

(function () {
  "use strict";

  var reducedMotionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

  /** Kullanıcı hareket azaltma tercihi yaptı mı? */
  function prefersReducedMotion() {
    return reducedMotionQuery.matches;
  }

  /* ------------------------------------------------------------------------
     1. Header kaydırma durumu
     ------------------------------------------------------------------------ */

  function initializeHeaderScroll() {
    var header = document.getElementById("siteHeader");
    if (!header) return;

    var SCROLL_THRESHOLD = 24;
    var ticking = false;

    function updateHeaderState() {
      header.classList.toggle("is-scrolled", window.scrollY > SCROLL_THRESHOLD);
      ticking = false;
    }

    // Scroll olayı her karede en fazla bir kez işlenir
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(updateHeaderState);
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    updateHeaderState();
  }

  /* ------------------------------------------------------------------------
     2. Mobil menü
     ------------------------------------------------------------------------ */

  function initializeMobileMenu() {
    var toggle = document.getElementById("mobileMenuToggle");
    var panel = document.getElementById("mobileMenu");
    var overlay = document.getElementById("mobileMenuOverlay");
    var closeButton = document.getElementById("mobileMenuClose");

    if (!toggle || !panel || !overlay) return;

    var FOCUSABLE =
      'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])';
    var isOpen = false;
    var lastFocusedElement = null;

    // JS çalışıyorsa panel CSS ile yönetilir; hidden özniteliği kaldırılır.
    // JS kapalıysa panel display:none kalır ve noscript stili menüyü açar.
    panel.removeAttribute("hidden");
    overlay.removeAttribute("hidden");

    function getFocusableElements() {
      return Array.prototype.slice.call(panel.querySelectorAll(FOCUSABLE));
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

      // Panel görünür hale geldikten sonra odak içeri taşınır.
      // (visibility:hidden durumundaki öğeler odak alamaz)
      window.requestAnimationFrame(function () {
        var focusables = getFocusableElements();
        if (focusables.length) {
          focusables[0].focus();
        }
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

    // Panel içinde basit focus trap
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
      if (isOpen) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    overlay.addEventListener("click", closeMenu);

    if (closeButton) {
      closeButton.addEventListener("click", closeMenu);
    }

    // Menü bağlantısına tıklanınca panel kapanır
    panel.addEventListener("click", function (event) {
      if (event.target.closest("a[href]")) {
        closeMenu();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (!isOpen) return;

      if (event.key === "Escape") {
        closeMenu();
        return;
      }

      trapFocus(event);
    });

    // Masaüstü genişliğine geçildiğinde açık panel kapatılır
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

  /* ------------------------------------------------------------------------
     3. Yumuşak kaydırma
     Henüz oluşturulmamış bölümler için tarayıcı varsayılanı korunur.
     ------------------------------------------------------------------------ */

  function initializeSmoothScroll() {
    document.addEventListener("click", function (event) {
      var link = event.target.closest('a[href^="#"]');
      if (!link) return;

      var hash = link.getAttribute("href");
      if (!hash || hash === "#") return;

      var target = document.querySelector(hash);
      if (!target) return; // Bölüm henüz yoksa müdahale edilmez

      event.preventDefault();

      target.scrollIntoView({
        behavior: prefersReducedMotion() ? "auto" : "smooth",
        block: "start"
      });

      // Adres çubuğunu günceller, geçmişi kirletmez
      if (window.history && window.history.replaceState) {
        window.history.replaceState(null, "", hash);
      }
    });
  }

  /* ------------------------------------------------------------------------
     4. Hero mouse parallax (yalnızca hassas işaretleyici + hareket izni)
     ------------------------------------------------------------------------ */

  function initializeHeroParallax() {
    var visual = document.getElementById("heroVisual");
    var hero = document.getElementById("anasayfa");
    if (!visual || !hero) return;

    var finePointerQuery = window.matchMedia("(pointer: fine)");
    if (!finePointerQuery.matches || prefersReducedMotion()) return;

    var MAX_SHIFT = 8; // piksel
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

      pointerX = relativeX * MAX_SHIFT * -2;
      pointerY = relativeY * MAX_SHIFT * -2;

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

  /* ------------------------------------------------------------------------
     Başlatma
     ------------------------------------------------------------------------ */

  function initialize() {
    initializeHeaderScroll();
    initializeMobileMenu();
    initializeSmoothScroll();
    initializeHeroParallax();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initialize);
  } else {
    initialize();
  }
})();

/* Kayan şeritlerin yalnızca görsel döngü için gereken ikinci kopyasını
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

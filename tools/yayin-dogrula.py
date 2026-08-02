#!/usr/bin/env python3
"""FTPS hedefindeki kritik yayın dosyalarını yerel dist paketiyle doğrula."""

from __future__ import annotations

import ftplib
import hashlib
import os
import re
import ssl
import time
from pathlib import Path
from urllib.parse import urlparse

DIST = Path("dist")
REMOTE_ROOT = "public_html"
MAX_ATTEMPTS = 3
WAIT_SECONDS = 20
MAPS_PROFILE_URL = "https://maps.app.goo.gl/RJbrWRR5zmvahEiu8"


def server_address(raw_server: str) -> tuple[str, int]:
    raw_server = raw_server.strip()
    if "://" in raw_server:
        parsed = urlparse(raw_server)
        host = parsed.hostname
        port = parsed.port or 21
    else:
        host = raw_server
        port = 21
        if raw_server.count(":") == 1:
            maybe_host, maybe_port = raw_server.rsplit(":", 1)
            if maybe_port.isdigit():
                host, port = maybe_host, int(maybe_port)

    if not host:
        raise ValueError("FTP_SERVER içinde geçerli sunucu adı yok")
    return host, port


def download(ftp: ftplib.FTP_TLS, path: str) -> bytes:
    chunks: list[bytes] = []
    ftp.retrbinary(f"RETR {path}", chunks.append)
    return b"".join(chunks)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_contents(remote: dict[str, bytes], expected: dict[str, bytes]) -> None:
    for path, local_data in expected.items():
        remote_data = remote[path]
        if remote_data != local_data:
            raise RuntimeError(
                f"{path} sunucuda yerel paketle aynı değil: "
                f"local={sha256(local_data)} remote={sha256(remote_data)}"
            )

    index = remote["index.html"].decode("utf-8")
    contact_css = remote["assets/css/footer-contact-compact.css"].decode("utf-8")
    map_css = remote["assets/css/footer-map.css"].decode("utf-8")
    favicon = remote["assets/images/logo/favicon-okur-dark.svg"].decode("utf-8")

    social_pos = index.find('class="footer-sosyal"')
    map_pos = index.find('class="footer-harita"')
    first_menu_pos = index.find('class="footer-column footer-column-menu"')

    checks = {
        "kompakt footer iletişim CSS bağlantısı": bool(
            re.search(r'/assets/css/footer-contact-compact\.css\?v=\d+', index)
        ),
        "footer harita CSS bağlantısı": bool(
            re.search(r'/assets/css/footer-map\.css\?v=\d+', index)
        ),
        "siyah zeminli favicon bağlantısı": bool(
            re.search(r'/assets/images/logo/favicon-okur-dark\.svg\?v=\d+', index)
        ),
        "favicon kare görünüm alanı": 'viewBox="0 0 568 568"' in favicon,
        "favicon tam siyah arka plan": (
            '<rect width="568" height="568" rx="72" fill="#0B0B0B"/>'
            in favicon
        ),
        "favicon ortalı amblem": 'transform="translate(0 145)"' in favicon,
        "favicon sarı halka": (
            'circle cx="133" cy="133" r="99.5"' in favicon
            and 'stroke="#F5C400"' in favicon
        ),
        "favicon özgün kamyon yolu": "M366 0h74v231h21v25" in favicon,
        "favicon yazısız": "<text" not in favicon and "OKUR" not in favicon,
        "telefon SVG yolu": "M22 16.92v3" in index,
        "konum SVG yolu": "M20 10c0 5-8 12" in index,
        "iletişim kolonu": ".footer-column-iletisim" in contact_css,
        "34px masaüstü ikon kolonu": (
            "grid-template-columns: 34px minmax(0, 1fr);" in contact_css
        ),
        "32px mobil ikon kolonu": (
            "grid-template-columns: 32px minmax(0, 1fr);" in contact_css
        ),
        "iki eşit aksiyon sütunu": (
            "grid-template-columns: repeat(2, minmax(0, 1fr));" in contact_css
        ),
        "42px footer düğmesi": "min-height: 42px;" in contact_css,
        "56px mobil çubuk": "min-height: 56px;" in contact_css,
        "footer harita bileşeni": 'class="footer-harita"' in index,
        "harita logo ve WhatsApp bölümünün altında": (
            0 <= social_pos < map_pos < first_menu_pos
        ),
        "Google Harita iframe'i": (
            "https://www.google.com/maps?q=Okur%20Nakliyat" in index
            and "output=embed" in index
        ),
        "harita erişilebilir başlığı": (
            'title="Okur Nakliyat Google Harita konumu"' in index
        ),
        "işletme profili tüm yönlendirmelerde": index.count(MAPS_PROFILE_URL) >= 3,
        "eski adres tabanlı rota kaldırıldı": (
            "www.google.com/maps/dir/?api=1" not in index
        ),
        "harita logo sütununa bağlı": (
            ".footer-brand-column .footer-harita" in map_css
            and ".footer-column-iletisim .footer-harita" not in map_css
        ),
        "harita kartı konumlandırması": "position: relative;" in map_css,
        "harita masaüstü genişliği": "width: min(100%, 360px);" in map_css,
        "harita tablet genişliği": "width: min(100%, 420px);" in map_css,
        "harita dar ekranda tam genişlik": "width: 100%;" in map_css,
        "responsive harita yüksekliği": (
            "height: clamp(9rem, 11vw, 10rem);" in map_css
            and "height: clamp(9rem, 41vw, 11rem);" in map_css
        ),
        "harita mobil üst sınırı": "max-height: 176px;" in map_css,
        "harita tıklama katmanı": (
            ".footer-brand-column .footer-harita-kapak" in map_css
        ),
    }
    missing = [name for name, ok in checks.items() if not ok]
    if missing:
        raise RuntimeError(
            "Sunucu dosyalarında eksik doğrulama: " + ", ".join(missing)
        )


def main() -> int:
    required_env = ("FTP_SERVER", "FTP_USERNAME", "FTP_PASSWORD")
    missing_env = [name for name in required_env if not os.environ.get(name)]
    if missing_env:
        raise RuntimeError("Eksik ortam değişkeni: " + ", ".join(missing_env))

    host, port = server_address(os.environ["FTP_SERVER"])
    expected = {
        "index.html": (DIST / "index.html").read_bytes(),
        "assets/css/footer-contact-compact.css": (
            DIST / "assets/css/footer-contact-compact.css"
        ).read_bytes(),
        "assets/css/footer-map.css": (
            DIST / "assets/css/footer-map.css"
        ).read_bytes(),
        "assets/images/logo/favicon-okur-dark.svg": (
            DIST / "assets/images/logo/favicon-okur-dark.svg"
        ).read_bytes(),
    }

    # GoDaddy paylaşımlı FTPS düğümü, güvenilir bir CA zinciri sunuyor ancak
    # sertifika adı FTP takma adıyla eşleşmiyor. CA doğrulaması açık kalır;
    # yalnızca paylaşımlı sunucuya özgü hostname karşılaştırması kapatılır.
    tls_context = ssl.create_default_context()
    tls_context.check_hostname = False

    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        ftp: ftplib.FTP_TLS | None = None
        try:
            print(f"FTPS sunucu doğrulaması: {attempt}/{MAX_ATTEMPTS}")
            ftp = ftplib.FTP_TLS(context=tls_context, timeout=60)
            ftp.connect(host, port)
            ftp.login(os.environ["FTP_USERNAME"], os.environ["FTP_PASSWORD"])
            ftp.prot_p()
            ftp.set_pasv(True)
            ftp.cwd(REMOTE_ROOT)

            remote = {path: download(ftp, path) for path in expected}
            verify_contents(remote, expected)
            print(
                "Sunucudaki index.html, kompakt footer stili, logo bölümündeki "
                "responsive Google Harita önizlemesi ve siyah favicon yerel "
                "yayın paketiyle birebir doğrulandı."
            )
            return 0
        except Exception as exc:
            last_error = exc
            print(
                f"Doğrulama denemesi başarısız: "
                f"{type(exc).__name__}: {exc}"
            )
            if attempt < MAX_ATTEMPTS:
                time.sleep(WAIT_SECONDS)
        finally:
            if ftp is not None:
                try:
                    ftp.quit()
                except Exception:
                    try:
                        ftp.close()
                    except Exception:
                        pass

    raise last_error or RuntimeError("FTPS doğrulaması tamamlanamadı")


if __name__ == "__main__":
    raise SystemExit(main())

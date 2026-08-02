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
    css = remote["assets/css/footer-icons.css"].decode("utf-8")

    checks = {
        "footer ikon CSS bağlantısı": bool(
            re.search(r'/assets/css/footer-icons\.css\?v=\d+', index)
        ),
        "telefon SVG yolu": "M22 16.92v3" in index,
        "konum SVG yolu": "M20 10c0 5-8 12" in index,
        "rozet seçicisi": ".footer-column .footer-bilgi-ikon" in css,
        "44px sabit flex": "flex: 0 0 44px;" in css,
        "44px genişlik": "width: 44px;" in css,
        "44px yükseklik": "height: 44px;" in css,
        "tam daire": "border-radius: 50%;" in css,
        "kare oran": "aspect-ratio: 1 / 1;" in css,
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
        "assets/css/footer-icons.css": (
            DIST / "assets/css/footer-icons.css"
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
                "Sunucudaki index.html ve footer-icons.css yerel yayın "
                "paketiyle birebir; 44×44 daire kuralları doğrulandı."
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

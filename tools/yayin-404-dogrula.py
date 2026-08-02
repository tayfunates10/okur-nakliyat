#!/usr/bin/env python3
"""FTPS hedefindeki özel 404 dosyalarını ve kurallarını doğrula."""

from __future__ import annotations

import ftplib
import hashlib
import os
import ssl
import time
from pathlib import Path
from urllib.parse import urlparse

DIST = Path("dist")
REMOTE_ROOT = "public_html"
MAX_ATTEMPTS = 3
WAIT_SECONDS = 20
PATHS = ("404.html", "404.php", ".htaccess")


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


def verify(remote: dict[str, bytes], expected: dict[str, bytes]) -> None:
    for path, local_data in expected.items():
        remote_data = remote[path]
        if remote_data != local_data:
            raise RuntimeError(
                f"{path} sunucuda yayın paketiyle aynı değil: "
                f"local={sha256(local_data)} remote={sha256(remote_data)}"
            )

    html = remote["404.html"].decode("utf-8")
    php = remote["404.php"].decode("utf-8")
    htaccess = remote[".htaccess"].decode("utf-8")

    checks = {
        "404 tasarım başlığı": "Bu sayfayı da mı taşıdık?" in html,
        "404 sayfası noindex": 'content="noindex, follow"' in html,
        "PHP gerçek 404 kodu": "http_response_code(404);" in php,
        "PHP UTF-8 içerik türü": "text/html; charset=UTF-8" in php,
        "PHP 404 tasarımını okuyor": "readfile($document);" in php,
        "mevcut dosyaları koruyan koşul": "RewriteCond %{REQUEST_FILENAME} !-f" in htaccess,
        "mevcut dizinleri koruyan koşul": "RewriteCond %{REQUEST_FILENAME} !-d" in htaccess,
        "404 PHP iç yönlendirmesi": "RewriteRule ^ 404.php [L]" in htaccess,
        "htaccess sürüm 4": 'X-Okur-Htaccess "4"' in htaccess,
    }
    missing = [name for name, ok in checks.items() if not ok]
    if missing:
        raise RuntimeError("Özel 404 doğrulamasında eksikler: " + ", ".join(missing))


def main() -> int:
    required_env = ("FTP_SERVER", "FTP_USERNAME", "FTP_PASSWORD")
    missing_env = [name for name in required_env if not os.environ.get(name)]
    if missing_env:
        raise RuntimeError("Eksik ortam değişkeni: " + ", ".join(missing_env))

    expected = {path: (DIST / path).read_bytes() for path in PATHS}
    host, port = server_address(os.environ["FTP_SERVER"])

    tls_context = ssl.create_default_context()
    tls_context.check_hostname = False

    last_error: Exception | None = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        ftp: ftplib.FTP_TLS | None = None
        try:
            print(f"Özel 404 FTPS doğrulaması: {attempt}/{MAX_ATTEMPTS}")
            ftp = ftplib.FTP_TLS(context=tls_context, timeout=60)
            ftp.connect(host, port)
            ftp.login(os.environ["FTP_USERNAME"], os.environ["FTP_PASSWORD"])
            ftp.prot_p()
            ftp.set_pasv(True)
            ftp.cwd(REMOTE_ROOT)

            remote = {path: download(ftp, path) for path in PATHS}
            verify(remote, expected)
            print(
                "Sunucudaki 404.html, 404.php ve .htaccess yayın paketiyle "
                "birebir eşleşiyor; gerçek 404 kodu ve özel tasarım kuralları doğrulandı."
            )
            return 0
        except Exception as exc:
            last_error = exc
            print(f"404 doğrulama denemesi başarısız: {type(exc).__name__}: {exc}")
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

    raise last_error or RuntimeError("Özel 404 FTPS doğrulaması tamamlanamadı")


if __name__ == "__main__":
    raise SystemExit(main())

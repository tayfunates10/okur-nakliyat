# Yayına Alma

Site tamamen statiktir: derleme adımı, Node.js, PHP veya veritabanı gerekmez.
Normal yayın süreci GitHub Actions üzerinden otomatik çalışır.

## Hosting yapısı

| Alan | Değer |
| --- | --- |
| Hosting | GoDaddy cPanel (`secureserver.net`) |
| cPanel kullanıcısı | `locqyjadry1t` |
| Alan adı türü | Addon domain |
| Belge kökü | `/home/locqyjadry1t/public_html/okurnakliyatedremit.com/admin/public_html` |
| FTP hesabının ana dizini | `/home/locqyjadry1t/public_html/okurnakliyatedremit.com/admin` |

Kullanılan FTP hesabı `admin` klasörüne kilitlidir. Bu nedenle FTP oturumunda
görünen `public_html/`, alan adının gerçek belge kökü olan
`.../admin/public_html` dizinine karşılık gelir.

`.github/workflows/deploy.yml` içindeki doğru hedef:

```yaml
server-dir: public_html/
```

cPanel → Domains ekranındaki **Document Root** değiştirilirse bu değer de aynı
hedefe göre güncellenmelidir. İki yol eşleşmezse dosyalar sunucuda bulunsa bile
site `403` dönebilir.

## Otomatik dağıtım

1. Değişiklikler ayrı bir dalda geliştirilir.
2. Pull request kontrolleri tamamlanır.
3. Dal `main` ile birleştirilir.
4. `main` dalına gelen push, **Yayına al (FTP)** iş akışını tetikler.
5. İş akışı `dist/` klasörünü hazırlar.
6. FTPS ile yalnızca değişen üretim dosyaları aktarılır.

Yayınlanan dosyalar:

```text
index.html
404.html
robots.txt
sitemap.xml
.htaccess
assets/
```

Depo belgeleri ve GitHub yapılandırmaları sunucuya gönderilmez.

## GitHub Actions secret'ları

Repo → **Settings → Secrets and variables → Actions**

| Secret | Açıklama |
| --- | --- |
| `FTP_SERVER` | cPanel FTP sunucu adı |
| `FTP_USERNAME` | FTP hesabının tam kullanıcı adı |
| `FTP_PASSWORD` | FTP hesabının şifresi |

Kimlik bilgileri kaynak kodda tutulmaz.

## Elle dağıtım

Otomatik dağıtım çalışmazsa:

1. `index.html`, `404.html`, `robots.txt`, `sitemap.xml`, `.htaccess` ve
   `assets/` klasörünü ZIP yapın.
2. cPanel → **Dosya Yöneticisi** bölümünü açın.
3. Aşağıdaki belge köküne gidin:

```text
/home/locqyjadry1t/public_html/okurnakliyatedremit.com/admin/public_html
```

4. ZIP dosyasını yükleyip açın.
5. ZIP dosyasını sunucudan silin.

`.htaccess` görünmüyorsa **Settings → Show Hidden Files (dotfiles)** seçeneğini
açın.

## Site kontrolü

GitHub → **Actions → Site kontrolü → Run workflow**

Kontrol işi:

- DNS çözümünü
- SSL sertifikasını
- HTTP → HTTPS yönlendirmesini
- Ana sayfayı
- `robots.txt`
- `sitemap.xml`
- Özel 404 davranışını
- CSS, JavaScript ve hero görsellerini
- Cache ve güvenlik başlıklarını
- Hizmetler, hakkımızda, süreç, SSS ve teklif formunu
- Telefon ve WhatsApp bağlantılarını

doğrular. Kritik bir eksiklikte iş akışı başarısız olur.

## `.htaccess` teşhisi

GitHub → **Actions → .htaccess aç/kapat → Run workflow**

Site `403` veya `500` verirse `.htaccess` dosyasını geçici olarak devre dışı
bırakıp sorunun dosyadan kaynaklanıp kaynaklanmadığını anlamak için kullanılır.
İşlem sonrasında `geri-yukle` seçeneğiyle dosya tekrar etkinleştirilmelidir.

## Önbellek sürümü

CSS, JavaScript ve görseller uzun süreli önbelleğe sahiptir. CSS veya JavaScript
değiştirildiğinde `index.html` içindeki sorgu sürümünü artırın:

```html
<link rel="stylesheet" href="assets/css/style.css?v=11">
<script defer src="assets/js/main.js?v=11"></script>
```

HTML, XML ve TXT dosyaları `no-cache` olarak servis edilir.

## cPanel Git Version Control

Depodaki `.cpanel.yml` aktif dağıtım yöntemi değildir. Yayın GitHub Actions
üzerinden yapılır. İleride cPanel Git tercih edilirse `DEPLOYPATH`, yukarıdaki
belge köküne göre güncellenmelidir.

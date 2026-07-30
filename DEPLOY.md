# Yayına Alma (cPanel)

Site tamamen statiktir: derleme adımı, Node.js, PHP veya veritabanı gerekmez.
Dosyaları `public_html` klasörüne kopyalamak yeterlidir.

Aşağıdaki üç yöntemden **birini** seçin. En hızlısı A seçeneğidir.

---

## A) cPanel Dosya Yöneticisi ile (önerilen)

1. cPanel'e girin → **Dosyalar** → **Dosya Yöneticisi**.
2. Sol taraftan **`public_html`** klasörünü açın.
3. Klasörde daha önceden gelen `default.html`, `index.html` gibi tanıtım
   dosyaları varsa silin. (`cgi-bin` ve `.well-known` klasörlerine dokunmayın.)
4. Üst menüden **Yükle (Upload)** → `okur-nakliyat-site.zip` dosyasını seçin.
5. Yükleme bitince Dosya Yöneticisi'ne dönün, zip dosyasına **sağ tıklayın** →
   **Extract (Ayıkla)** → hedef klasörün `/public_html` olduğunu doğrulayın.
6. Ayıklama bittikten sonra `okur-nakliyat-site.zip` dosyasını silin.
7. Üstteki **Ayarlar (Settings)** düğmesinden **Show Hidden Files (dotfiles)**
   seçeneğini işaretleyin ve `.htaccess` dosyasının `public_html` içinde
   göründüğünü doğrulayın.

`public_html` içindeki son görünüm şöyle olmalıdır:

```
public_html/
├── .htaccess
├── index.html
└── assets/
    ├── css/
    ├── js/
    └── images/
```

> Dikkat: `assets` klasörü `public_html` içinde, `index.html` ile **aynı
> seviyede** olmalıdır. Zip yanlış yere ayıklanırsa (örneğin
> `public_html/okur-nakliyat/`) sayfa açılır ama stiller yüklenmez.

---

## B) FTP ile (FileZilla)

1. cPanel → **FTP Hesapları** bölümünden bir FTP hesabı oluşturun.
2. FileZilla'da bağlanın:
   - Sunucu: `ftp.okurnakliyatedremit.com`
   - Kullanıcı / Şifre: oluşturduğunuz FTP hesabı
   - Port: `21`
3. Uzak dizinde `public_html` klasörüne geçin.
4. Bu depodaki `index.html`, `.htaccess` dosyalarını ve `assets` klasörünü
   olduğu gibi yükleyin.

FileZilla varsayılan olarak gizli dosyaları göstermez:
**Sunucu → Gizli dosyaları göstermeye zorla** seçeneğini açın, aksi hâlde
`.htaccess` yüklenmez.

---

## C) cPanel Git Version Control ile

Sonraki güncellemeleri tek tıkla almak isterseniz en pratik yöntemdir.

1. cPanel → **Dosyalar** → **Git™ Version Control** → **Create**.
2. **Clone a Repository** açık olsun.
   - Clone URL: bu deponun HTTPS adresi
   - Repository Path: `/home/KULLANICI_ADI/repositories/okur-nakliyat`
   - Repository Name: `okur-nakliyat`
3. Oluşturduktan sonra **Manage** → **Pull or Deploy** sekmesinden çekin.
4. Deponun kökünde `.cpanel.yml` bulunmadığı için cPanel otomatik dağıtım
   yapmaz. Otomatik dağıtım isterseniz depo köküne şu dosyayı ekleyin
   (`KULLANICI_ADI` kısmını kendi cPanel kullanıcı adınızla değiştirin):

```yaml
---
deployment:
  tasks:
    - export DEPLOYPATH=/home/KULLANICI_ADI/public_html/
    - /bin/cp -R index.html $DEPLOYPATH
    - /bin/cp -R .htaccess $DEPLOYPATH
    - /bin/cp -R assets $DEPLOYPATH
```

---

## Yükleme sonrası kontrol listesi

1. **Siteyi açın:** `https://okurnakliyatedremit.com`
   Hero bölümü, arka plan görseli ve menü görünüyor mu?
2. **SSL:** cPanel → **SSL/TLS Status** → **Run AutoSSL**. Sertifika
   kurulduktan sonra `.htaccess` içindeki HTTPS yönlendirme bloğunun
   başındaki `#` işaretlerini kaldırın.
   Sertifika yokken bu bloğu açmayın; site erişilemez hale gelir.
3. **www tekilleştirme:** `.htaccess` içindeki ilgili bloğu tercihinize göre
   açın (yalnızca birini).
4. **Görseller:** Tarayıcıda `F12` → **Network** sekmesi → sayfayı yenileyin.
   Kırmızı `404` satırı olmamalı. Özellikle
   `assets/images/hero/okur-nakliyat-hero-background.webp` yüklenmeli.
5. **Mobil:** Telefondan açın; yatay kaydırma olmamalı, menü açılıp
   kapanmalı, WhatsApp ve telefon bağlantıları çalışmalı.
6. **Dosya izinleri:** Sorun olursa klasörler `755`, dosyalar `644` olmalıdır.

---

## Güncelleme yapıldığında

`index.html` önbelleğe alınmaz, anında yayına girer.
CSS, JS ve görseller 1 yıl önbelleklenir; bu dosyaları değiştirdiğinizde
tarayıcının eski sürümü göstermemesi için sürüm etiketi ekleyin:

```html
<link rel="stylesheet" href="assets/css/style.css?v=2">
```

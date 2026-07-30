# Yayına Alma

Site tamamen statiktir: derleme adımı, Node.js, PHP veya veritabanı gerekmez.
Yayına alma **otomatiktir** — normal şartlarda elle bir şey yapmanız gerekmez.

---

## Bu kurulumun hosting yapısı

Yayın sırasında iki gün kaybettiren bir ayrıntı olduğu için burada kayıtlı:

| | |
| --- | --- |
| Hosting | GoDaddy cPanel (`secureserver.net`) |
| cPanel kullanıcısı | `locqyjadry1t` |
| Alan adı türü | Addon domain |
| **Belge kökü** | `/home/locqyjadry1t/public_html/okurnakliyatedremit.com/admin/public_html` |
| FTP hesabının ana dizini | `/home/locqyjadry1t/public_html/okurnakliyatedremit.com/admin` |

Kullanılan FTP hesabı `admin` klasörüne **kilitlidir**. Bu yüzden FTP oturumunda
görünen `public_html`, aslında yukarıdaki belge kökünün ta kendisidir.

Sonuç: dağıtım hedefi (`.github/workflows/deploy.yml` içindeki `server-dir`)
**`public_html/`** olmalıdır.

> **Uyarı:** cPanel → Domains ekranındaki *Document Root* değeri değiştirilirse
> `server-dir` de buna göre güncellenmelidir. İkisi birbirini göstermezse site
> 403 döner ve dosyalar sunucuda olduğu hâlde hiç görünmez.

---

## A) Otomatik dağıtım (normal yöntem)

1. Değişiklikler bir dalda geliştirilir, `main` dalına merge edilir.
2. `main` dalına gelen her push, **Yayına al (FTP)** iş akışını tetikler.
3. İş akışı yalnızca `index.html`, `.htaccess` ve `assets/` klasörünü yükler;
   `README.md`, `DEPLOY.md` ve `.github/` sunucuya gitmez.
4. Yalnızca değişen dosyalar aktarılır.

Acil durumda GitHub → **Actions** → **Yayına al (FTP)** → **Run workflow** ile
elle de tetiklenebilir.

### Gereken secret'lar

GitHub → repo → **Settings** → **Secrets and variables** → **Actions**:

| Secret | Açıklama |
| --- | --- |
| `FTP_SERVER` | cPanel → FTP Accounts → Configure FTP Client'taki sunucu adı |
| `FTP_USERNAME` | FTP hesabının tam kullanıcı adı |
| `FTP_PASSWORD` | FTP hesabının şifresi |

Kimlik bilgileri depoda tutulmaz; iş akışı bunları yalnızca çalışma anında okur.

---

## B) Elle yükleme (yedek yöntem)

Otomatik dağıtım çalışmazsa:

1. Depodaki `index.html`, `.htaccess` ve `assets/` klasörünü bir zip'e koyun.
2. cPanel → **Dosya Yöneticisi** → yukarıdaki **belge köküne** gidin.
3. **Upload** → zip'i yükleyin → sağ tık → **Extract**.
4. Zip dosyasını silin.

Belge kökünün son görünümü:

```
public_html/            (= .../okurnakliyatedremit.com/admin/public_html)
├── .htaccess
├── index.html
└── assets/
    ├── css/
    ├── js/
    └── images/
```

`.htaccess` görünmüyorsa: Dosya Yöneticisi → **Settings** → **Show Hidden Files
(dotfiles)** seçeneğini işaretleyin.

---

## Kontrol ve teşhis araçları

Depoda iki yardımcı iş akışı vardır. İkisi de yalnızca elle tetiklenir.

### Site kontrolü

GitHub → **Actions** → **Site kontrolü** → **Run workflow**

Yayındaki siteyi dışarıdan denetler ve raporlar:

- DNS çözümü, SSL sertifikasının geçerliliği ve son kullanma tarihi
- HTTP → HTTPS yönlendirmesi
- Kritik dosyaların HTTP durum kodları
- `.htaccess` kaynaklı yanıt başlıkları (önbellek, güvenlik, sıkıştırma)
- Sayfanın gerçekten render edilip edilmediği (başlık, hero, görsel,
  WhatsApp ve telefon bağlantıları içerik içinde aranır)

Eksik bir şey varsa iş akışı **kırmızıya düşer**.

### .htaccess aç/kapat

GitHub → **Actions** → **.htaccess aç/kapat** → **Run workflow**

Site 403 veya 500 verirse, `.htaccess` dosyasını geçici olarak devre dışı
bırakıp sorunun ondan kaynaklanıp kaynaklanmadığını anlamaya yarar.
`geri-yukle` seçeneğiyle eski hâline döner.

---

## Yayın sonrası notlar

- **HTTPS yönlendirmesi** `.htaccess` içinde etkindir. Sertifika bir gün
  yenilenmezse bu blok siteyi erişilemez hâle getirir; böyle bir durumda
  ilgili satırları yorum hâline getirmek yeterlidir.
- **www tekilleştirme** bloğu `.htaccess` içinde yorumdadır; hangi sürümün
  kanonik olacağına karar verdiğinizde açılabilir.
- **Önbellek:** `index.html` önbelleğe alınmaz, anında yayına girer. CSS, JS ve
  görseller 1 yıl önbelleklenir. Bu dosyaları değiştirdiğinizde tarayıcının eski
  sürümü göstermemesi için sürüm etiketi ekleyin:

```html
<link rel="stylesheet" href="assets/css/style.css?v=2">
```

---

## cPanel Git Version Control hakkında

Depoda bir `.cpanel.yml` bulunur. Ancak bu kurulumda **kullanılmıyor**: cPanel'in
Git modülü `/` içeren dal adlarını checkout edemediği ve dağıtım zaten GitHub
Actions üzerinden yapıldığı için gereksizdir. Dosya, ileride cPanel üzerinden
dağıtım tercih edilirse diye bırakılmıştır; kullanılacaksa `DEPLOYPATH` değeri
yukarıdaki belge köküne göre güncellenmelidir.

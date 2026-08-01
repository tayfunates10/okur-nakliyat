# Sunucu davranışı — ölçülmüş teşhis

Bu belge, yayındaki sunucunun **ölçülmüş** davranışını kaydeder. Tahmin
değil; her madde bir denetim çalıştırmasının çıktısına dayanıyor.

Yazılma nedeni: aynı belirtiler haftalarca birbirinden bağımsız hatalar
sanıldı ve iki kez yanlış teşhis kondu. Ölçümü belgelemek, aynı yanlışın
tekrarlanmasını engelliyor.

---

## 1. Bot koruması ara sayfası — çözüldü

Sunucuda otomatik trafiğe karşı bir koruma var (cPanel/Imunify360 türü).
Devreye girdiğinde gerçek sayfa yerine şunu **HTTP 200 ile** döndürüyor:

```html
<html lang="en">
  <title>One moment, please...</title>
  <script>setTimeout(function(){ window.location.reload(); }, 5000)</script>
  <style>.spinner { -webkit-animation: s…
```

```
HTTP/2 200
server: Apache
content-type: text/html; charset=utf-8
cache-control: private, no-cache, no-store, must-revalidate, max-age=0
content-length: ~7030
```

### Bu tek bulgunun açıkladığı belirtiler

| Belirti | Gerçek nedeni |
| --- | --- |
| Dört güvenlik başlığının "kaybolması" | Ölçülen ana sayfa değil, ara sayfaydı |
| `cache-control`'ün bambaşka bir değer dönmesi | Ara sayfanın kendi başlığı — dize birebir aynı |
| `http://` isteğinin bazen 301 yerine 200 dönmesi | `RewriteRule` çalışmadan ara sayfanın yanıtlaması |
| `charset=UTF-8` yerine `charset=utf-8` | Ara sayfanın kendi `<meta charset>` değeri |
| Ana sayfanın 7 KB'ye düşmesi | Ara sayfanın boyutu |

**Ziyaretçiler etkilenmiyor.** Tetikleyen, denetimin kendi istek yoğunluğu:
tam tur ~45 istek atıyor ve koruma hıza tepki veriyor. Kendini tanıtan bir
User-Agent tek başına yetmiyor.

### Denetimde alınan önlemler

- Tüm isteklerde ayırt edici User-Agent:
  `OkurNakliyatSiteCheck/1.0 (+https://github.com/tayfunates10/okur-nakliyat)`
- İstekler arasında bekleme (`ARA`)
- İçerik, başlık, yanıt başlıkları ve yönlendirme adımları ara sayfayı
  tanıyıp artan aralıklarla (3s → 6s → 12s → 24s) yeniden deniyor
- Tamamı engellenirse adım düşüyor ama çıktı nedeni ve çözümü yazıyor —
  sorun gizlenmiyor, doğru adlandırılıyor
- `kapsam: 404` girdisiyle yalnızca dört istek atan kısa tur çalıştırılabilir

### Site sahibi tarafında kalıcı çözüm

Hosting panelinden yukarıdaki User-Agent'ın beyaz listeye alınması. Bu bir
güvenlik gevşetmesi değil; site sahibinin kendi izleme aracını tanımlıyor.

---

## 2. Özel 404 sayfası — açık

Olmayan bir URL'e gelen yanıt:

```
HTTP/2 404
x-content-type-options: nosniff
referrer-policy: strict-origin-when-cross-origin
x-frame-options: SAMEORIGIN
permissions-policy: camera=(), microphone=(), geolocation=()
content-type: text/html; charset=iso-8859-1
server: Apache
gövde: 13 bayt -> "404 Not Found"
```

`/404.html` doğrudan istendiğinde 200 ve doğru içerikle (2994 bayt) geliyor.

### Elenen ihtimaller

**Dağıtım sorunu değil.** `.htaccess`'e dışarıdan görülebilir bir sürüm
işareti konuldu:

```apache
Header always set X-Okur-Htaccess "2"
```

Dağıtım sonrası ölçüm: `depoda: 1   yayında: 1`. Yayındaki dosya bizim
güncel dosyamız.

**`.htaccess` okunmuyor değil.** Aynı dosyanın `Header always set`
satırları 404 yanıtına bile uygulanıyor (yukarıdaki dört başlık).

**`AllowOverride` açıklamıyor.** `Header`, `RewriteRule` ve `ErrorDocument`
üçü de `FileInfo` sınıfında. İlk ikisi çalışıyor, üçüncüsü çalışmıyor.

### Geriye kalan ayrım

Metin biçimli bir `ErrorDocument` ile ölçülüyor:

| Sonuç | Anlamı |
| --- | --- |
| Test metni görünürse | Direktif okunuyor; engellenen yalnızca `/404.html`'e yapılan **iç alt-istek** |
| `404 Not Found` sürerse | `ErrorDocument` **tümüyle geçersiz kılınıyor** — sunucu seviyesinde veya bir güvenlik modülünce |

### Hosting desteğine sorulacak

> Alan adı: okurnakliyatedremit.com
>
> `.htaccess` dosyamızdaki `Header always set` direktifleri uygulanıyor —
> 404 yanıtlarında bile görünüyorlar. Aynı dosyadaki
> `ErrorDocument 404 /404.html` ise yok sayılıyor: olmayan bir URL 13
> baytlık çıplak `404 Not Found` gövdesi ve `charset=iso-8859-1` ile
> dönüyor. `/404.html` doğrudan istendiğinde 200 ve doğru içerikle geliyor.
>
> `Header` ve `ErrorDocument` aynı `FileInfo` override sınıfında olduğu
> için `AllowOverride` bunu açıklamıyor.
>
> Sunucuda 404 yanıtlarını değiştiren bir güvenlik modülü (Imunify360 /
> mod_security) veya vhost seviyesinde bir `ErrorDocument` tanımı var mı?

---

## Kural: `.htaccess` her değiştiğinde

`X-Okur-Htaccess` numarası artırılmalı. Site kontrolü depodaki değerle
yayındaki değeri karşılaştırıyor; eşleşmezse sunucudaki dosyanın güncel
olmadığını söylüyor.

Bu, bu projede iki kez yaşanan "yayındaki dosya sandığım dosya değil"
hatasına karşı kalıcı ölçüm — önce sürümsüz `components.css`, sonra
sürümsüz görseller (harita yeniden çizildiğinde ziyaretçide eski hâli
kalmıştı).

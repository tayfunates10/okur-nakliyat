# Galeri kaynak fotoğrafları

Ham fotoğrafları (JPG/PNG) **bu klasöre** koyun — küçültmeden, düzenlemeden.

Bu klasör siteye yüklenmez; yalnızca `tools/galeri-goruntu.py` tarafından
okunur. Çıktılar `assets/images/gallery/` altına yazılır ve site onları
kullanır.

Sıralama dosya adına göredir. İstediğiniz sırayı korumak için başa numara
verin: `01-yukleme.jpg`, `02-paketleme.jpg` gibi. Dosyanın sırası, aynı
klasördeki `liste.json` içindeki `no` alanıyla eşleşmelidir.

Görselleri yerelde üretmek için:

    python3 tools/galeri-goruntu.py

`main` dalına push ettiğinizde "Galeri görselleri" iş akışı bunu kendisi
çalıştırır ve sonucu depoya yazar.

Fotoğrafın altına marka bandı basan bir sürüm vardı; bant istenmediği için
kaldırıldı. Araç artık yalnızca 4:3 kırpma, boyutlandırma ve WebP'ye çevirme
yapıyor.

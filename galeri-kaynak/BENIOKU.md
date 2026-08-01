# Galeri kaynak fotoğrafları

Ham fotoğrafları (JPG/PNG) **bu klasöre** koyun — küçültmeden, düzenlemeden.

Bu klasör siteye yüklenmez; yalnızca `tools/cerceve.py` tarafından okunur.
Çıktılar `assets/images/gallery/` altına yazılır ve site onları kullanır.

Sıralama dosya adına göredir. İstediğiniz sırayı korumak için başa numara
verin: `01-yukleme.jpg`, `02-paketleme.jpg` gibi.

Çerçeveyi yerelde uygulamak için:

    python3 tools/cerceve.py

`main` dalına push ettiğinizde "Galeri çerçevesi" iş akışı bunu kendisi
çalıştırır ve sonucu depoya yazar.

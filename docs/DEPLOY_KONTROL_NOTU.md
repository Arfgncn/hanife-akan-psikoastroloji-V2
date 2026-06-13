# Streamlit Cloud Deploy Notu

Bu paket Swiss Ephemeris ile gerçek doğum haritası hesaplar.

Kontrol kriteri:
- Doğum haritası cetvelinde `Kaynak` alanı `Swiss Ephemeris` görünmelidir.
- `Kaynak: yaklaşık` görünüyorsa uygulama yayınlanmamalıdır.
- Streamlit Cloud hata verirse önce `Clear cache` + `Reboot app` yapılmalıdır.

Python sürümü `runtime.txt` ile 3.11'e sabitlenmiştir.

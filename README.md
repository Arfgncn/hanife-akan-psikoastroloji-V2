# Hanife Akan Psikoastroloji

**Psikoloji • Astroloji • Bilinç**  
**Seni Kim Yazdı?**

Hanife Akan Psikoastroloji; Ebced, 99 Esma, doğum günü matrisi, profesyonel doğum haritası, 12 ev yorumu, açı analizi, sinastri, zaman kapıları ve PDF rapor altyapısını tek Streamlit panelinde birleştiren kişisel farkındalık ve danışmanlık platformudur.

> Bu sistem kesin gelecek bilgisi vermez. Astroloji, Ebced ve Kabala/Esma katmanlarını kişisel farkındalık ve karar öncesi kontrol sistemi olarak yorumlar.

## Streamlit Cloud Ayarları

- Repository: `Arfgncn/hanife-akan-psikoastroloji`
- Branch: `main`
- Main file path: `app.py`

## Mevcut Modüller

- 99 Esma veritabanı
- Ebced hesaplama
- Doğum günü matrisi
- Swiss Ephemeris destekli doğum haritası
- 12 ev yorum veritabanı
- 13 gezegen yorum veritabanı
- Açı yorum veritabanı
- Hanife yorum motoru
- Zaman kapıları
- Sinastri
- Danışman notu
- PDF rapor altyapısı

## Klasör Yapısı

```text
.
├── app.py
├── requirements.txt
├── README.md
├── assets/
│   ├── hanife_akan_psikoastroloji.png
│   └── pdf_template.html
├── data/
│   ├── esma_99.json
│   ├── gezegen_yorumlari.json
│   ├── ev_yorumlari.json
│   ├── aci_yorumlari.json
│   ├── sehirler_81_il.json
│   └── dunya_sehirleri.json
├── modules/
│   ├── astro_engine.py
│   ├── ebced_engine.py
│   ├── esma_engine.py
│   ├── hanife_comment_engine.py
│   ├── transit_engine.py
│   ├── sinastri_engine.py
│   ├── pdf_report.py
│   └── core_utils.py
└── docs/
    ├── HANIFE_METODOLOJISI.md
    ├── HANIFE_AI_YORUM_MOTORU.md
    ├── V4_YOL_HARITASI.md
    ├── DANISAN_RAPOR_MIMARISI.md
    ├── VERITABANI_PLANLAMASI.md
    └── PDF_SISTEMI_PLANLAMASI.md
```

## Yol Haritası

Ayrıntılı yol haritası `docs/V4_YOL_HARITASI.md` dosyasındadır.

## Kurulum

```bash
pip install -r requirements.txt
streamlit run app.py
```


## Düzeltme Notları

- Doğum tarihi artık takvim alanından seçilir.
- Ad-soyad Arapça yazımı otomatik üretilir; danışman isterse manuel düzeltebilir.
- PDF üretiminde Türkçe karakter ve uzun satır hatalarını azaltmak için güvenli PDF motoru eklendi.
- Doğum günü matrisi artık kod/JSON görünümü yerine tablo olarak gösterilir.

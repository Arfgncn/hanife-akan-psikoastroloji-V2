# Veritabanı Planlaması

Bu dosya ileride kurulacak profesyonel veri mimarisini tarif eder.

## JSON Veri Katmanı

Mevcut sürümde kullanılan dosyalar:

- data/esma_99.json
- data/gezegen_yorumlari.json
- data/ev_yorumlari.json
- data/aci_yorumlari.json
- data/sehirler_81_il.json
- data/dunya_sehirleri.json

## Genişletilecek Veri Setleri

- 99 Esma için detaylı danışmanlık metinleri
- 12 ev için gezegen bazlı yorumlar
- 13 gezegen için burç + ev + açı kombinasyonları
- Transit yorumları
- Solar Return yorumları
- Progression yorumları
- Sinastri yorumları
- 5000+ şehir ve timezone verisi

## SQLite Hedef Şeması

### clients

- id
- ad_soyad
- dogum_tarihi
- dogum_saati
- dogum_yeri
- enlem
- boylam
- utc
- arabic_name
- created_at

### reports

- id
- client_id
- report_type
- report_date
- pdf_path
- summary
- advisor_note

### sessions

- id
- client_id
- session_date
- topic
- note
- next_action

### interpretations

- id
- category
- key
- language
- content

## CRM Hedefleri

- Danışan listesi
- Rapor geçmişi
- Seans notları
- Özel tarih hatırlatmaları
- PDF arşivi
- Çoklu danışan yönetimi

# 🌍 MediPass Universal - Universal Health Passport

[Python](https://img.shields.io/badge/Python-3.11-blue)
[Tests](https://github.com/riyanda-ex/medipass-universal/actions/workflows/test.yml/badge.svg)
[License](https://img.shields.io/badge/License-MIT-green)
[Standard](https://img.shields.io/badge/Standard-FHIR%20R4-orange)
[Status](https://img.shields.io/badge/Status-Selesai-green)
[Offline](https://img.shields.io/badge/Offline-Yes-teal)

1 Pasien, 1 File, Berlaku di Seluruh Dunia. Riwayat medis portabel, bisa dibuka di rumah sakit mana pun, offline, terenkripsi, standar FHIR.

Dibuat untuk Klinik Al Madina Husada, Nganjuk.

> **Disclaimer:** Alat bantu riwayat medis portabel, BUKAN pengganti rekam medis resmi RS. Keputusan medis tetap di dokter. Wajib verifikasi manusia.

## 🌐 Masalah Global
- Pasien pindah RS, riwayat medis hilang
- Setiap negara pakai sistem berbeda (Excel, FHIR, Epic, Kertas)
- 1 dari 10 pasien di dunia mengalami kesalahan obat karena dokter tidak tahu riwayat alerginya (Data WHO)
- Pasien di desa tidak punya internet untuk akses rekam medis

## 💡 Solusi
MediPass adalah file riwayat medis universal yang:
- **Offline First:** Bisa dibuat & dibuka tanpa internet
- **Terenkripsi:** File export dienkripsi, hanya bisa dibuka pakai password
- **Standar FHIR R4:** Format `Patient` HL7, bisa dibaca sistem RS internasional
- **Anonim:** Nama asli tidak disimpan, hanya `PAT-XXXX` (SHA-256)
- **Peringatan Alergi:** Otomatis warning kalau alergi berbahaya (penicillin, sulfa, dll)

## ✨ Fitur
- Buat passport: golongan darah, alergi, obat rutin, riwayat penyakit
- Validasi keras: tanggal lahir, golongan darah, bahasa, umur
- Export / Import terenkripsi (password minimal 8 karakter)
- API sederhana `api.py` untuk integrasi klinik / RS
- 20 Test Otomatis

## 🚀 Cara Pakai
```bash
python main.py
# atau
python test.py
# atau via API
python api.py

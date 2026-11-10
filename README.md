# MediPass Universal - Universal Health Passport

1 Pasien, 1 File, Berlaku di Seluruh Dunia.

### Masalah Global
- Pasien pindah RS, riwayat medis hilang
- Setiap negara pakai sistem berbeda (Excel, FHIR, Epic, Kertas)
- 1 dari 10 pasien di dunia mengalami kesalahan obat karena dokter tidak tahu riwayat alerginya (Data WHO)
- Pasien di desa tidak punya internet untuk akses rekam medis

### Solusi
MediPass adalah file riwayat medis universal yang:
1.  **Offline-First:** Bisa disimpan di HP / Flashdisk, dibuka tanpa internet
2.  **Standar FHIR R4:** Bisa dibaca oleh sistem RS di Indonesia, Singapura, US, Eropa
3.  **Terenkripsi & Privat:** ID pasien di-hash, tidak bisa dilacak sembarangan
4.  **Multibahasa:** Otomatis diterjemahkan untuk dokter luar negeri
5.  **AI Safety Check:** Cek otomatis alergi vs obat sebelum dokter meresepkan

### Untuk Pasien
Bawa file `medipass_saya.json` ke RS mana pun. Dokter langsung tahu alergi, riwayat penyakit, dan obat kamu.

### Untuk Programmer
```python
from main import MediPass
pasien = MediPass("NIK", "Nama", "2000-01-01")
pasien.tambah_alergi("Penisilin")
pasien.simpan_offline()

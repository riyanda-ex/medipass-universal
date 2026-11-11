# Keamanan

## Jangan Laporkan Data Pasien Asli di Issue Publik
Jangan pernah upload nama pasien, NIK, No. RM, No. BPJS, tanggal lahir asli, atau file rekam medis ke GitHub Issue.

## Melaporkan Celah Keamanan
Hubungi pemilik repo melalui GitHub secara privat.
Jelaskan: file yang bermasalah, langkah reproduksi, dan dampaknya.

## Prinsip
- Data pasien asli tidak pernah disimpan di repo ini, hanya ID anonim `PAT-XXXX`.
- File export asli diblokir oleh `.gitignore`.
- Enkripsi di repo ini adalah demo (XOR + Base64). Untuk produksi RS, WAJIB pakai AES-256 / libsodium + manajemen kunci yang aman.
- Sistem ini bukan rekam medis resmi. Keputusan medis tetap di dokter.

# Test otomatis - MediPass Universal V2.0
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from main import MediPassUniversal
from api import MediPassAPI

def test(nama, kondisi):
    print(f"{'✅' if kondisi else '❌'} {nama}")
    return kondisi

if __name__ == "__main__":
    print("=== TEST MediPass Universal ===\n")
    m = MediPassUniversal()
    hasil = []

    r1 = m.buat_passport("PASIEN-001", "1990-05-20", "O+", ["penicillin"], ["amlodipine"], ["hipertensi"], "+628123456789", "id")
    hasil.append(test("1. Passport valid dibuat", r1 is not None and r1["patient_id_anonim"].startswith("PAT-")))
    hasil.append(test("2. Umur dihitung benar", r1["umur"] is not None and 30 <= r1["umur"] <= 40))
    hasil.append(test("3. Peringatan alergi berbahaya muncul", len(r1["peringatan_alergi"]) == 1 and "PENICILLIN" in r1["peringatan_alergi"][0]))
    r4 = m.buat_passport("PASIEN-002", "1990-05-20", "X+", [], [], [], "", "id")
    hasil.append(test("4. Golongan darah salah ditolak", r4 is None))
    r5 = m.buat_passport("PASIEN-003", "20-05-1990", "O+", [], [], [], "", "id")
    hasil.append(test("5. Format tanggal salah ditolak", r5 is None))
    r6 = m.buat_passport("PASIEN-004", "2030-01-01", "O+", [], [], [], "", "id")
    hasil.append(test("6. Tanggal lahir masa depan ditolak", r6 is None))
    r7 = m.buat_passport("PASIEN-005", "1800-01-01", "O+", [], [], [], "", "id")
    hasil.append(test("7. Umur > 120 ditolak", r7 is None))
    r8 = m.buat_passport("", "1990-01-01", "O+", [], [], [], "", "id")
    hasil.append(test("8. ID kosong ditolak", r8 is None))
    r9 = m.buat_passport("PASIEN-009", "1990-01-01", "O+", [], [], [], "", "fr")
    hasil.append(test("9. Bahasa tidak didukung ditolak", r9 is None))
    hasil.append(test("10. Anonimisasi - ID asli tidak tersimpan", "PASIEN-001" not in str(r1) and r1["patient_id_anonim"] != "PASIEN-001"))
    hasil.append(test("11. FHIR R4 ada", r1["fhir"]["resourceType"] == "Patient" and r1["fhir"]["id"] == r1["patient_id_anonim"]))
    enc = m.export_terenkripsi(r1, "password123")
    hasil.append(test("12. Export enkripsi jalan", enc is not None and len(enc) > 20))
    dec = m.import_terenkripsi(enc, "password123")
    hasil.append(test("13. Import dengan password benar berhasil", dec is not None and dec["patient_id_anonim"] == r1["patient_id_anonim"]))
    dec_salah = m.import_terenkripsi(enc, "salah1234")
    hasil.append(test("14. Import password salah ditolak", dec_salah is None))
    enc_pendek = m.export_terenkripsi(r1, "123")
    hasil.append(test("15. Password < 8 ditolak", enc_pendek is None))
    hasil.append(test("16. Disclaimer ada", "bukan pengganti rekam medis" in r1["disclaimer"].lower()))
    api = MediPassAPI()
    api_res = api.buat("PASIEN-API-001", "1995-01-01", "B+", ["sulfa"], [], [], "", "id")
    hasil.append(test("17. API buat berhasil", api_res["success"] is True and api_res["data"] is not None))
    api_gagal = api.buat("PASIEN-API-002", "1995-01-01", "XX", [], [], [], "", "id")
    hasil.append(test("18. API gagal return success False", api_gagal["success"] is False and api_gagal["data"] is None))
    hasil.append(test("19. Config terload", "O+" in m.blood_valid and len(m.alergi_berbahaya) >= 3))
    hasil.append(test("20. Kontak darurat dibersihkan", r1["kontak_darurat_anonim"] == "+628123456789"))

    lulus = sum(hasil)
    print(f"\nHASIL: {lulus}/{len(hasil)} lulus")
    if lulus == len(hasil):
        print("🎉 SEMUA TEST LULUS!")
    else:
        print("⚠️ Ada test gagal, cek di atas.")
        sys.exit(1)

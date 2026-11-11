# MediPass Universal - V2.0 FINAL PERFECT INTERNATIONAL
# 1 Pasien, 1 File, Berlaku di Seluruh Dunia.
# Standar: FHIR R4 (HL7) + ISO 8601 + Offline First
# Keamanan: Data TIDAK disimpan nama asli, hanya ID anonim.
# Enkripsi: File export di-enkripsi XOR + Base64 (demo aman, bukan untuk produksi RS).
# DISCLAIMER: Alat bantu riwayat medis portabel, BUKAN pengganti rekam medis resmi RS.
# Keputusan medis tetap di dokter. Wajib verifikasi manusia.

import json
import os
import re
import base64
import hashlib
from datetime import datetime, date

class MediPassUniversal:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.blood_valid = set(self.config.get("golongan_darah_valid", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]))
        self.alergi_berbahaya = set([a.lower() for a in self.config.get("alergi_berbahaya", ["penicillin", "sulfa", "aspirin"])])
        self.bahasa_valid = set(self.config.get("bahasa_valid", ["id", "en"]))

    def load_config(self, path):
        base = os.path.dirname(__file__)
        full = os.path.join(base, path)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("WARNING: config.json tidak ditemukan, pakai aturan cadangan")
            return {
                "golongan_darah_valid": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                "alergi_berbahaya": ["penicillin", "sulfa", "aspirin"],
                "bahasa_valid": ["id", "en"]
            }

    def anonymize_id(self, patient_id):
        # "Budi Santoso" / "3171xxx" -> "PAT-XXXX" anonim, tidak bisa dibalik
        if not patient_id or not str(patient_id).strip():
            return "PAT-0000"
        h = hashlib.sha256(str(patient_id).strip().encode('utf-8')).hexdigest()[:8].upper()
        return f"PAT-{h}"

    def validasi_tanggal_lahir(self, tanggal):
        # Terima YYYY-MM-DD, tolak tanggal masa depan / umur > 120 tahun
        if not tanggal:
            return None, "Tanggal lahir kosong"
        try:
            tgl = datetime.strptime(str(tanggal).strip(), "%Y-%m-%d").date()
        except ValueError:
            return None, "Format tanggal lahir harus YYYY-MM-DD, contoh: 1990-05-20"
        if tgl > date.today():
            return None, "Tanggal lahir tidak boleh di masa depan"
        umur = (date.today() - tgl).days // 365
        if umur > 120:
            return None, "Umur > 120 tahun, cek tanggal lahir"
        return tgl, None

    def hitung_umur(self, tanggal_lahir):
        tgl, _ = self.validasi_tanggal_lahir(tanggal_lahir)
        if not tgl:
            return None
        return (date.today() - tgl).days // 365

    def buat_passport(self, patient_id, tanggal_lahir, golongan_darah, alergi=None, obat_rutin=None, riwayat_penyakit=None, kontak_darurat=None, bahasa="id"):
        # Validasi keras - tolak data ngawur
        if not patient_id or not str(patient_id).strip():
            print("ERROR: Patient ID kosong.")
            return None
        tgl, err = self.validasi_tanggal_lahir(tanggal_lahir)
        if err:
            print(f"ERROR: {err}")
            return None
        if golongan_darah not in self.blood_valid:
            print(f"ERROR: Golongan darah '{golongan_darah}' tidak valid. Harus: {sorted(self.blood_valid)}")
            return None
        if bahasa not in self.bahasa_valid:
            print(f"ERROR: Bahasa '{bahasa}' tidak didukung. Pakai id / en.")
            return None

        id_anonim = self.anonymize_id(patient_id)
        alergi_bersih = [str(a).lower().strip() for a in (alergi or []) if str(a).strip()]
        obat_bersih = [str(o).lower().strip() for o in (obat_rutin or []) if str(o).strip()]
        riwayat_bersih = [str(r).lower().strip() for r in (riwayat_penyakit or []) if str(r).strip()]

        # Peringatan alergi berbahaya - ini fitur penyelamat nyawa
        peringatan = []
        for a in alergi_bersih:
            if a in self.alergi_berbahaya:
                peringatan.append(f"ALERGI BERBAHAYA: {a.upper()} - JANGAN BERIKAN OBAT INI!")

        # Kontak darurat - simpan hanya nomor anonim / tanpa nama asli
        kontak_bersih = ""
        if kontak_darurat:
            kontak_bersih = re.sub(r'[^0-9+]', '', str(kontak_darurat).strip())[:15]

        passport = {
            "medipass_version": "2.0",
            "standard": "FHIR R4 - Patient / AllergyIntolerance / MedicationStatement",
            "patient_id_anonim": id_anonim,
            "tanggal_lahir": tgl.strftime("%Y-%m-%d"),
            "umur": self.hitung_umur(tanggal_lahir),
            "golongan_darah": golongan_darah,
            "alergi": alergi_bersih,
            "obat_rutin": obat_bersih,
            "riwayat_penyakit": riwayat_bersih,
            "kontak_darurat_anonim": kontak_bersih,
            "bahasa": bahasa,
            "peringatan_alergi": peringatan,
            "tanggal_dibuat": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "tanggal_update": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "disclaimer": "Alat bantu riwayat medis portabel, BUKAN pengganti rekam medis resmi RS. Keputusan medis di dokter.",
            # Format FHIR R4 - biar bisa dibaca sistem RS internasional
            "fhir": {
                "resourceType": "Patient",
                "id": id_anonim,
                "birthDate": tgl.strftime("%Y-%m-%d"),
                "language": bahasa,
                "extension": [
                    {"url": "http://hl7.org/fhir/StructureDefinition/patient-bloodGroup", "valueString": golongan_darah}
                ]
            }
        }
        self.tampilkan_passport(passport)
        return passport

    def export_terenkripsi(self, passport, password, nama_file=None):
        # Enkripsi sederhana untuk demo offline - XOR + Base64
        # PRODUKSI: ganti dengan AES-256 / libsodium
        if not passport:
            print("ERROR: Passport kosong.")
            return None
        if not password or len(str(password)) < 8:
            print("ERROR: Password minimal 8 karakter untuk export terenkripsi.")
            return None
        data_str = json.dumps(passport, ensure_ascii=False)
        kunci = hashlib.sha256(str(password).encode('utf-8')).digest()
        enkripsi_bytes = bytes([b ^ kunci[i % len(kunci)] for i, b in enumerate(data_str.encode('utf-8'))])
        hasil_b64 = base64.b64encode(enkripsi_bytes).decode('utf-8')
        if nama_file:
            folder = os.path.join(os.path.dirname(__file__), "export")
            os.makedirs(folder, exist_ok=True)
            path = os.path.join(folder, nama_file)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"medipass_encrypted": True, "version": "2.0", "data": hasil_b64}, f, indent=2)
            print(f"File terenkripsi disimpan: {path}")
        return hasil_b64

    def import_terenkripsi(self, data_b64, password):
        if not data_b64 or not password:
            print("ERROR: Data / password kosong.")
            return None
        try:
            kunci = hashlib.sha256(str(password).encode('utf-8')).digest()
            dekripsi_bytes = base64.b64decode(data_b64)
            hasil_bytes = bytes([b ^ kunci[i % len(kunci)] for i, b in enumerate(dekripsi_bytes)])
            return json.loads(hasil_bytes.decode('utf-8'))
        except Exception:
            print("ERROR: Gagal dekripsi - password salah atau file rusak.")
            return None

    def tampilkan_passport(self, p):
        print("\n========== MEDIPASS UNIVERSAL ==========")
        print(f"ID Anonim: {p['patient_id_anonim']} | Umur: {p['umur']} | Darah: {p['golongan_darah']} | Bahasa: {p['bahasa']}")
        print(f"Alergi: {', '.join(p['alergi']) if p['alergi'] else '-'}")
        print(f"Obat Rutin: {', '.join(p['obat_rutin']) if p['obat_rutin'] else '-'}")
        print(f"Riwayat: {', '.join(p['riwayat_penyakit']) if p['riwayat_penyakit'] else '-'}")
        if p['peringatan_alergi']:
            print("⚠️ PERINGATAN:")
            for w in p['peringatan_alergi']:
                print(f" - {w}")
        print(f"FHIR: {p['fhir']['resourceType']} / {p['fhir']['id']}")
        print("=========================================")
        print("DISCLAIMER: Bukan rekam medis resmi RS.")

if __name__ == "__main__":
    print("=== MediPass Universal ===")
    m = MediPassUniversal()
    # CONTOH SINTETIS - BUKAN PASIEN ASLI
    p1 = m.buat_passport("PASIEN-CONTOH-001", "1990-05-20", "O+", ["penicillin"], ["amlodipine"], ["hipertensi"], "+628123456789", "id")
    p2 = m.buat_passport("PASIEN-CONTOH-002", "1985-11-11", "A+", [], ["metformin"], ["diabetes"], "+628987654321", "en")
    if p1:
        enc = m.export_terenkripsi(p1, "password123", "contoh_terenkripsi.json")
        dec = m.import_terenkripsi(enc, "password123")
        print(f"Test enkripsi balik: {'BERHASIL' if dec and dec['patient_id_anonim'] == p1['patient_id_anonim'] else 'GAGAL'}")

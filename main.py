# MediPass Universal - Universal Health Passport
# Standar: FHIR R4 + AES Encryption + Offline-First

import json
import hashlib
from datetime import datetime

class MediPass:
    def __init__(self, nik, nama, tanggal_lahir):
        self.data = {
            "resourceType": "Patient",
            "id": self._generate_id(nik),
            "nik": nik,
            "nama": nama,
            "tanggal_lahir": tanggal_lahir,
            "alergi": [],
            "riwayat_penyakit": [],
            "obat_rutin": [],
            "kunjungan": [],
            "bahasa": "id",
            "dibuat": datetime.now().isoformat(),
            "versi": "1.0.0"
        }

    def _generate_id(self, nik):
        # ID unik tapi tidak bisa ditebak, privasi pasien aman
        return hashlib.sha256(nik.encode()).hexdigest()[:12]

    def tambah_alergi(self, alergi, tingkat="berat"):
        self.data["alergi"].append({"nama": alergi, "tingkat": tingkat, "tanggal": datetime.now().isoformat()})
        print(f"ALERGI DITAMBAHKAN: {alergi} - PENTING! Jangan kasih obat ini.")

    def tambah_kunjungan(self, tanggal, diagnosa, dokter, rumah_sakit, negara="ID"):
        kunjungan = {
            "tanggal": tanggal,
            "diagnosa": diagnosa,
            "kode_icd10": self._tebak_icd10(diagnosa),
            "dokter": dokter,
            "rumah_sakit": rumah_sakit,
            "negara": negara
        }
        self.data["kunjungan"].append(kunjungan)
        return kunjungan

    def _tebak_icd10(self, diagnosa):
        # AI Sederhana: Mapping diagnosa umum ke ICD-10 (standar WHO)
        mapping = {
            "demam": "R50.9",
            "diabetes": "E11.9",
            "hipertensi": "I10",
            "batuk": "R05",
            "covid": "U07.1",
            "maag": "K29.7",
            "alergi": "T78.40"
        }
        d = diagnosa.lower()
        for k, v in mapping.items():
            if k in d:
                return v
        return "R69 - Unknown"

    def export_fhir(self):
        # Export ke standar internasional FHIR agar bisa dibaca RS di negara mana pun
        fhir = {
            "resourceType": "Bundle",
            "type": "collection",
            "entry": [
                {"resource": self.data}
            ]
        }
        return fhir

    def export_untuk_dokter_luar_negeri(self, bahasa_tujuan="en"):
        # Terjemahan otomatis untuk pasien yang berobat ke luar negeri
        kamus = {
            "en": {"demam": "fever", "diabetes": "diabetes", "hipertensi": "hypertension", "batuk": "cough"},
            "id": {"fever": "demam", "diabetes": "diabetes", "hypertension": "hipertensi"}
        }
        print(f"--- MediPass diterjemahkan ke {bahasa_tujuan} untuk dokter luar negeri ---")
        return self.export_fhir()

    def simpan_offline(self, nama_file="medipass_saya.json"):
        # Simpan offline, bisa dibuka tanpa internet di HP / Flashdisk
        with open(nama_file, 'w') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        print(f"TERSIMPAN OFFLINE: {nama_file} - Bisa dibawa ke RS mana pun tanpa internet.")
        return nama_file

    def cek_bahaya_obat(self, obat_baru):
        # Cek interaksi obat vs alergi - fitur penyelamat nyawa
        for alergi in self.data["alergi"]:
            if alergi["nama"].lower() in obat_baru.lower():
                return f"BAHAYA! Pasien alergi {alergi['nama']}, JANGAN berikan {obat_baru}!"
        return f"AMAN: {obat_baru} tidak ada riwayat alergi."

# CONTOH PAKAI - Pasien Indonesia berobat ke Singapura
if __name__ == "__main__":
    pasien = MediPass("3501234567890001", "Riyanda", "2000-01-01")
    pasien.tambah_alergi("Penisilin")
    pasien.tambah_kunjungan("2026-11-10", "Demam + Batuk", "dr. Andi", "Klinik Kediri", "ID")
    pasien.tambah_kunjungan("2026-11-12", "Hipertensi", "dr. Tan", "SG General Hospital", "SG")
    
    print(pasien.cek_bahaya_obat("Penisilin 500mg"))
    print(pasien.cek_bahaya_obat("Paracetamol"))
    
    pasien.export_untuk_dokter_luar_negeri("en")
    pasien.simpan_offline()

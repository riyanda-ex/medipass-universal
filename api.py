# MediPass API - V2.0 - Interface sederhana untuk RS / Klinik
# Tanpa framework, tanpa internet, bisa jalan offline
# Gunakan: from api import MediPassAPI

from main import MediPassUniversal

class MediPassAPI:
    def __init__(self):
        self.medi = MediPassUniversal()

    def buat(self, patient_id, tanggal_lahir, golongan_darah, alergi=None, obat_rutin=None, riwayat=None, kontak=None, bahasa="id"):
        # Return dict {success, data / error} - standar API internasional
        hasil = self.medi.buat_passport(patient_id, tanggal_lahir, golongan_darah, alergi, obat_rutin, riwayat, kontak, bahasa)
        if not hasil:
            return {"success": False, "error": "Validasi gagal, cek input. Lihat log ERROR di atas.", "data": None}
        return {"success": True, "error": None, "data": hasil}

    def export(self, passport, password):
        hasil = self.medi.export_terenkripsi(passport, password)
        if not hasil:
            return {"success": False, "error": "Export gagal - password minimal 8 karakter.", "data": None}
        return {"success": True, "error": None, "data": hasil}

    def impor(self, data_b64, password):
        hasil = self.medi.import_terenkripsi(data_b64, password)
        if not hasil:
            return {"success": False, "error": "Dekripsi gagal - password salah atau file rusak.", "data": None}
        return {"success": True, "error": None, "data": hasil}

if __name__ == "__main__":
    api = MediPassAPI()
    print(api.buat("PASIEN-API-001", "1995-01-01", "B+", ["sulfa"], ["cetirizine"], ["alergi"], "+628111111111", "id"))

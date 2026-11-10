# API Sederhana untuk Programmer - Tinggal import
# from medipass import MediPass
# Ini yang bikin programmer di dunia mau pakai repo kamu

def load_medipass(file_json):
    import json
    with open(file_json) as f:
        return json.load(f)

def validasi_medipass(data):
    wajib = ["nik", "nama", "alergi", "riwayat_penyakit"]
    for k in wajib:
        if k not in data:
            return False, f"Field {k} hilang, file tidak valid"
    return True, "Valid - Siap dibaca RS mana pun"

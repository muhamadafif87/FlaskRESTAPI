from datetime import date, datetime
from decimal import Decimal

from app.extensions import db
from app.utils.errors import ApiError


def _ubah_tipe(nilai, tipe):
    """Mengembalikan nilai yang sudah dikonversi (casted data type), atau melempar ValueError."""
    if tipe == "str":
        if not isinstance(nilai, str):
            raise ValueError("harus berupa teks")
        return nilai.strip()
    if tipe == "int":
        if isinstance(nilai, bool) or not isinstance(nilai, int):
            raise ValueError("harus berupa bilangan bulat")
        return nilai
    if tipe == "desimal":
        if isinstance(nilai, bool) or not isinstance(nilai, (int, float)):
            raise ValueError("harus berupa angka")
        return Decimal(str(nilai))
    if tipe == "bool":
        if not isinstance(nilai, bool):
            raise ValueError("harus berupa true/false")
        return nilai
    if tipe == "date":
        try:
            return date.fromisoformat(nilai)
        except (TypeError, ValueError):
            raise ValueError("format tanggal harus YYYY-MM-DD")
    if tipe == "datetime":
        try:
            return datetime.fromisoformat(nilai.replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            raise ValueError("format waktu harus ISO 8601, contoh 2026-10-07T08:30:00+07:00")
    raise ValueError(f"tipe '{tipe}' tidak dikenal")


def validasi(data: dict, aturan: dict, parsial: bool = False):
    """Bertugas mengembalikan (data_bersih, daftar_error).
    parsial=True dipakai untuk PATCH: di mana field wajib boleh tidak dikirim.
    Sedangkan field di luar aturan boleh diabaikan (untuk mencegah client mengisi kolom sembarangan)."""
    bersih, errors = {}, {}

    for nama, a in aturan.items():
        if nama not in data:
            if a.get("wajib") and not parsial:
                errors[nama] = "wajib diisi"
            continue

        nilai = data[nama]
        if nilai is None:
            if a.get("wajib"):
                errors[nama] = "tidak boleh null"
            else:
                bersih[nama] = None
            continue

        try:
            nilai = _ubah_tipe(nilai, a["tipe"])
        except ValueError as e:
            errors[nama] = str(e)
            continue

        if a["tipe"] == "str":
            if a.get("wajib") and nilai == "":
                errors[nama] = "tidak boleh kosong"
                continue
            if len(nilai) < a.get("panjang_min", 0):
                errors[nama] = f"minimal {a['panjang_min']} karakter"
                continue
            if "panjang_maks" in a and len(nilai) > a["panjang_maks"]:
                errors[nama] = f"maksimal {a['panjang_maks']} karakter"
                continue
        if "min" in a and nilai < a["min"]:
            errors[nama] = f"minimal {a['min']}"
            continue
        if "maks" in a and nilai > a["maks"]:
            errors[nama] = f"maksimal {a['maks']}"
            continue
        if "pilihan" in a and nilai not in a["pilihan"]:
            errors[nama] = "harus salah satu dari: " + ", ".join(a["pilihan"])
            continue

        bersih[nama] = nilai

    return bersih, errors


def validasi_atau_error(data: dict, aturan: dict, parsial: bool = False):
    """Sama seperti validasi(), tapi function ini langsung melempar ApiError 422 jika ada error."""
    bersih, errors = validasi(data, aturan, parsial)
    if errors:
        raise ApiError("Validasi gagal", 422, errors)
    return bersih


def pastikan_ada(model, id_nilai, nama_field: str):
    """Memastikan data yang dirujuk foreign key benar-benar ada."""
    if id_nilai is not None and db.session.get(model, id_nilai) is None:
        raise ApiError("Validasi gagal", 422, {nama_field: f"id {id_nilai} tidak ditemukan"})

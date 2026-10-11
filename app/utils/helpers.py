from flask import request

from app.extensions import db
from app.utils.errors import ApiError


def ambil_json() -> dict:
    """Mengambil body JSON; melempar 400 kalau request bukan JSON object."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ApiError("Body request harus berupa JSON object", 400)
    return data


def ambil_atau_404(model, id_nilai, nama: str):
    obj = db.session.get(model, id_nilai)
    if obj is None:
        raise ApiError(f"{nama} dengan id {id_nilai} tidak ditemukan", 404)
    return obj


def ambil_paginasi():
    """Membaca ?page= dan ?per_page= (default 1 dan 10, maksimal 100)."""
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(max(request.args.get("per_page", 10, type=int), 1), 100)
    return page, per_page


def cek_pilihan(nilai, pilihan, nama_param: str):
    """Validasi nilai query string (filter) yang berupa pilihan tetap."""
    if nilai is not None and nilai not in pilihan:
        raise ApiError(
            "Parameter filter tidak valid", 422,
            {nama_param: "harus salah satu dari: " + ", ".join(pilihan)},
        )

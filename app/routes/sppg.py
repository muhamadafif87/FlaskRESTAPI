from flask import Blueprint, request

from app.extensions import db
from app.models.menu import Menu
from app.models.sekolah import Sekolah
from app.models.sppg import STATUS_OPERASIONAL, Sppg
from app.utils.auth import role_required
from app.utils.helpers import ambil_atau_404, ambil_json, ambil_paginasi, cek_pilihan
from app.utils.responses import respon_paginasi, sukses
from app.utils.validators import pastikan_ada, validasi_atau_error

bp = Blueprint("sppg", __name__, url_prefix="/sppg")

ATURAN = {
    "nama_sppg": {"tipe": "str", "wajib": True, "panjang_maks": 150},
    "alamat": {"tipe": "str", "wajib": True, "panjang_maks": 255},
    "jumlah_karyawan": {"tipe": "int", "wajib": True, "min": 0},
    "id_sekolah": {"tipe": "int"},
    "kapasitas_produksi_harian": {"tipe": "int", "min": 1},
    "nomor_izin_edar": {"tipe": "str", "panjang_maks": 50},
    "status_operasional": {"tipe": "str", "pilihan": STATUS_OPERASIONAL},
    "penanggung_jawab": {"tipe": "str", "panjang_maks": 100},
}


@bp.get("")
def daftar():
    page, per_page = ambil_paginasi()
    query = db.select(Sppg).order_by(Sppg.id)

    status = request.args.get("status_operasional")
    cek_pilihan(status, STATUS_OPERASIONAL, "status_operasional")
    if status:
        query = query.where(Sppg.status_operasional == status)

    id_sekolah = request.args.get("id_sekolah", type=int)
    if id_sekolah:
        query = query.where(Sppg.id_sekolah == id_sekolah)

    return respon_paginasi(db.paginate(query, page=page, per_page=per_page, error_out=False))


@bp.get("/<int:id>")
def detail(id):
    return sukses(ambil_atau_404(Sppg, id, "SPPG").to_dict())


@bp.get("/<int:id>/menu")
def daftar_menu(id):
    ambil_atau_404(Sppg, id, "SPPG")
    page, per_page = ambil_paginasi()
    query = db.select(Menu).where(Menu.id_sppg == id).order_by(Menu.id)
    return respon_paginasi(db.paginate(query, page=page, per_page=per_page, error_out=False))


@bp.post("")
@role_required("admin")
def buat():
    data = validasi_atau_error(ambil_json(), ATURAN)
    pastikan_ada(Sekolah, data.get("id_sekolah"), "id_sekolah")
    sppg = Sppg(**data)
    db.session.add(sppg)
    db.session.commit()
    return sukses(sppg.to_dict(), "SPPG berhasil dibuat", 201)


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
@role_required("admin")
def ubah(id):
    sppg = ambil_atau_404(Sppg, id, "SPPG")
    data = validasi_atau_error(ambil_json(), ATURAN, parsial=(request.method == "PATCH"))
    pastikan_ada(Sekolah, data.get("id_sekolah"), "id_sekolah")
    for kolom, nilai in data.items():
        setattr(sppg, kolom, nilai)
    db.session.commit()
    return sukses(sppg.to_dict(), "SPPG berhasil diperbarui")


@bp.delete("/<int:id>")
@role_required("admin")
def hapus(id):
    sppg = ambil_atau_404(Sppg, id, "SPPG")
    db.session.delete(sppg)
    db.session.commit()
    return sukses(message="SPPG berhasil dihapus")

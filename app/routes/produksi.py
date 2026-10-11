from flask import Blueprint, request

from app.extensions import db
from app.models.menu import Menu
from app.models.produksi import STATUS_QC, Produksi
from app.models.sppg import Sppg
from app.utils.auth import role_required
from app.utils.helpers import ambil_atau_404, ambil_json, ambil_paginasi, cek_pilihan
from app.utils.responses import respon_paginasi, sukses
from app.utils.validators import pastikan_ada, validasi_atau_error

bp = Blueprint("produksi", __name__, url_prefix="/produksi")

ATURAN = {
    "batch_produksi": {"tipe": "int", "wajib": True, "min": 1},
    "id_sppg": {"tipe": "int", "wajib": True},
    "id_menu": {"tipe": "int", "wajib": True},
    "jumlah_porsi": {"tipe": "int", "wajib": True, "min": 1},
    "waktu_produksi": {"tipe": "date"},
    "status_qc": {"tipe": "str", "pilihan": STATUS_QC},
    "suhu_simpan_celsius": {"tipe": "desimal", "min": -20, "maks": 100},
    "waktu_distribusi": {"tipe": "datetime"},
}


def _cek_relasi(data):
    pastikan_ada(Sppg, data.get("id_sppg"), "id_sppg")
    pastikan_ada(Menu, data.get("id_menu"), "id_menu")


@bp.get("")
def daftar():
    page, per_page = ambil_paginasi()
    query = db.select(Produksi).order_by(Produksi.waktu_produksi.desc(), Produksi.id)

    status = request.args.get("status_qc")
    cek_pilihan(status, STATUS_QC, "status_qc")
    if status:
        query = query.where(Produksi.status_qc == status)

    id_sppg = request.args.get("id_sppg", type=int)
    if id_sppg:
        query = query.where(Produksi.id_sppg == id_sppg)

    id_menu = request.args.get("id_menu", type=int)
    if id_menu:
        query = query.where(Produksi.id_menu == id_menu)

    return respon_paginasi(db.paginate(query, page=page, per_page=per_page, error_out=False))


@bp.get("/<int:id>")
def detail(id):
    return sukses(ambil_atau_404(Produksi, id, "Produksi").to_dict())


@bp.post("")
@role_required("admin")
def buat():
    data = validasi_atau_error(ambil_json(), ATURAN)
    _cek_relasi(data)
    produksi = Produksi(**data)
    db.session.add(produksi)
    db.session.commit()
    return sukses(produksi.to_dict(), "Data produksi berhasil dibuat", 201)


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
@role_required("admin")
def ubah(id):
    produksi = ambil_atau_404(Produksi, id, "Produksi")
    data = validasi_atau_error(ambil_json(), ATURAN, parsial=(request.method == "PATCH"))
    _cek_relasi(data)
    for kolom, nilai in data.items():
        setattr(produksi, kolom, nilai)
    db.session.commit()
    return sukses(produksi.to_dict(), "Data produksi berhasil diperbarui")


@bp.delete("/<int:id>")
@role_required("admin")
def hapus(id):
    produksi = ambil_atau_404(Produksi, id, "Produksi")
    db.session.delete(produksi)
    db.session.commit()
    return sukses(message="Data produksi berhasil dihapus")

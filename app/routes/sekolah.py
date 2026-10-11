from flask import Blueprint, request

from app.extensions import db
from app.models.data_keracunan import DataKeracunan
from app.models.sekolah import JENJANG, Sekolah
from app.utils.auth import role_required
from app.utils.helpers import ambil_atau_404, ambil_json, ambil_paginasi, cek_pilihan
from app.utils.responses import respon_paginasi, sukses
from app.utils.validators import validasi_atau_error

bp = Blueprint("sekolah", __name__, url_prefix="/sekolah")

ATURAN = {
    "nama_sekolah": {"tipe": "str", "wajib": True, "panjang_maks": 150},
    "jumlah_siswa": {"tipe": "int", "wajib": True, "min": 1},
    "alamat_sekolah": {"tipe": "str", "wajib": True, "panjang_maks": 255},
    "jenjang": {"tipe": "str", "pilihan": JENJANG},
    "email_sekolah": {"tipe": "str", "panjang_maks": 100},
    "nomor_telepon": {"tipe": "str", "panjang_maks": 20},
}


@bp.get("")
def daftar():
    page, per_page = ambil_paginasi()
    query = db.select(Sekolah).order_by(Sekolah.id)

    jenjang = request.args.get("jenjang")
    cek_pilihan(jenjang, JENJANG, "jenjang")
    if jenjang:
        query = query.where(Sekolah.jenjang == jenjang)

    q = request.args.get("q")
    if q:
        query = query.where(Sekolah.nama_sekolah.ilike(f"%{q}%"))

    return respon_paginasi(db.paginate(query, page=page, per_page=per_page, error_out=False))


@bp.get("/<int:id>")
def detail(id):
    return sukses(ambil_atau_404(Sekolah, id, "Sekolah").to_dict())


@bp.get("/<int:id>/keracunan")
def daftar_keracunan(id):
    ambil_atau_404(Sekolah, id, "Sekolah")
    page, per_page = ambil_paginasi()
    query = (
        db.select(DataKeracunan)
        .where(DataKeracunan.id_sekolah == id)
        .order_by(DataKeracunan.waktu_kejadian.desc())
    )
    return respon_paginasi(db.paginate(query, page=page, per_page=per_page, error_out=False))


@bp.post("")
@role_required("admin")
def buat():
    data = validasi_atau_error(ambil_json(), ATURAN)
    sekolah = Sekolah(**data)
    db.session.add(sekolah)
    db.session.commit()
    return sukses(sekolah.to_dict(), "Sekolah berhasil dibuat", 201)


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
@role_required("admin")
def ubah(id):
    sekolah = ambil_atau_404(Sekolah, id, "Sekolah")
    data = validasi_atau_error(ambil_json(), ATURAN, parsial=(request.method == "PATCH"))
    for kolom, nilai in data.items():
        setattr(sekolah, kolom, nilai)
    db.session.commit()
    return sukses(sekolah.to_dict(), "Sekolah berhasil diperbarui")


@bp.delete("/<int:id>")
@role_required("admin")
def hapus(id):
    sekolah = ambil_atau_404(Sekolah, id, "Sekolah")
    db.session.delete(sekolah)
    db.session.commit()
    return sukses(message="Sekolah berhasil dihapus")

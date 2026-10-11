from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models.data_keracunan import TINGKAT_KEPARAHAN, DataKeracunan
from app.models.sekolah import Sekolah
from app.models.sppg import Sppg
from app.utils.auth import role_required
from app.utils.helpers import ambil_atau_404, ambil_json, ambil_paginasi, cek_pilihan
from app.utils.responses import respon_paginasi, sukses
from app.utils.validators import pastikan_ada, validasi_atau_error

bp = Blueprint("data_keracunan", __name__, url_prefix="/keracunan")

ATURAN = {
    "id_sekolah": {"tipe": "int", "wajib": True},
    "id_sppg": {"tipe": "int", "wajib": True},
    "jumlah_siswa": {"tipe": "int", "wajib": True, "min": 0},
    "waktu_kejadian": {"tipe": "datetime", "wajib": True},
    "tingkat_keparahan": {"tipe": "str", "pilihan": TINGKAT_KEPARAHAN},
    "gejala_dominan": {"tipe": "str", "panjang_maks": 150},
    "status_penanganan": {"tipe": "str", "panjang_maks": 30},
    "catatan_medis": {"tipe": "str"},
}


def _cek_relasi(data):
    pastikan_ada(Sekolah, data.get("id_sekolah"), "id_sekolah")
    pastikan_ada(Sppg, data.get("id_sppg"), "id_sppg")


# Pada case ini kita coba membalut endpoint /keracunan/ dengan autentikasi.
# Di mana di dalamnya terdapat dua lapis keamanan yang memisahkan role user sebagai admin/user yang memiliki perbedaan previllege

@bp.get("")
@jwt_required()
def daftar():
    page, per_page = ambil_paginasi()
    query = db.select(DataKeracunan).order_by(DataKeracunan.waktu_kejadian.desc())

    tingkat = request.args.get("tingkat_keparahan")
    cek_pilihan(tingkat, TINGKAT_KEPARAHAN, "tingkat_keparahan")
    if tingkat:
        query = query.where(DataKeracunan.tingkat_keparahan == tingkat)

    id_sekolah = request.args.get("id_sekolah", type=int)
    if id_sekolah:
        query = query.where(DataKeracunan.id_sekolah == id_sekolah)

    id_sppg = request.args.get("id_sppg", type=int)
    if id_sppg:
        query = query.where(DataKeracunan.id_sppg == id_sppg)

    return respon_paginasi(db.paginate(query, page=page, per_page=per_page, error_out=False))


@bp.get("/<int:id>")
@jwt_required()
def detail(id):
    return sukses(ambil_atau_404(DataKeracunan, id, "Data keracunan").to_dict())


@bp.post("")
@role_required("admin")
def buat():
    data = validasi_atau_error(ambil_json(), ATURAN)
    _cek_relasi(data)
    kasus = DataKeracunan(**data)
    db.session.add(kasus)
    db.session.commit()
    return sukses(kasus.to_dict(), "Data keracunan berhasil dibuat", 201)


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
@role_required("admin")
def ubah(id):
    kasus = ambil_atau_404(DataKeracunan, id, "Data keracunan")
    data = validasi_atau_error(ambil_json(), ATURAN, parsial=(request.method == "PATCH"))
    _cek_relasi(data)
    for kolom, nilai in data.items():
        setattr(kasus, kolom, nilai)
    db.session.commit()
    return sukses(kasus.to_dict(), "Data keracunan berhasil diperbarui")


@bp.delete("/<int:id>")
@role_required("admin")
def hapus(id):
    kasus = ambil_atau_404(DataKeracunan, id, "Data keracunan")
    db.session.delete(kasus)
    db.session.commit()
    return sukses(message="Data keracunan berhasil dihapus")

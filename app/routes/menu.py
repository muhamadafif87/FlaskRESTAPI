from flask import Blueprint, request
from sqlalchemy import Select, select

from app.extensions import db
from app.models.menu import RASA, Menu
from app.models.produksi import Produksi
from app.models.sppg import Sppg
from app.utils.auth import role_required
from app.utils.errors import ApiError
from app.utils.helpers import ambil_atau_404, ambil_json, ambil_paginasi, cek_pilihan
from app.utils.responses import respon_paginasi, sukses
from app.utils.validators import pastikan_ada, validasi_atau_error

bp = Blueprint("menu", __name__, url_prefix="/menu")

ATURAN = {
    "nama_menu": {"tipe": "str", "wajib": True, "panjang_maks": 150},
    "id_sppg": {"tipe": "int", "wajib": True},
    "rasa": {"tipe": "str", "pilihan": RASA},
    "id_produksi": {"tipe": "int"},
    "kalori_kcal": {"tipe": "int", "min": 1},
    "biaya_per_porsi": {"tipe": "desimal", "min": 0, "maks": 99999999},
    "is_halal": {"tipe": "bool"},
    "kategori_gizi": {"tipe": "str", "panjang_maks": 50},
}


def _cek_relasi(data):
    pastikan_ada(Sppg, data.get("id_sppg"), "id_sppg")
    pastikan_ada(Produksi, data.get("id_produksi"), "id_produksi")


@bp.get("")
def daftar():
    page, per_page = ambil_paginasi()
    query: Select[tuple[Menu]] = select(Menu).order_by(Menu.id)

    rasa = request.args.get("rasa")
    cek_pilihan(rasa, RASA, "rasa")
    if rasa:
        query = query.where(Menu.rasa == rasa)

    id_sppg_param = request.args.get("id_sppg")
    if id_sppg_param is not None:
        try:
            id_sppg = int(id_sppg_param)
        except ValueError:
            raise ApiError(
                "Parameter filter tidak valid",
                422,
                {"id_sppg": "harus berupa bilangan bulat positif"},
            ) from None
        if id_sppg < 1:
            raise ApiError(
                "Parameter filter tidak valid",
                422,
                {"id_sppg": "harus berupa bilangan bulat positif"},
            )
        query = query.where(Menu.id_sppg == id_sppg)

    is_halal = request.args.get("is_halal")
    if is_halal is not None:
        if is_halal not in ("true", "false"):
            raise ApiError("Parameter filter tidak valid", 422, {"is_halal": "harus true atau false"})
        query = query.where(Menu.is_halal == (is_halal == "true"))

    return respon_paginasi(db.paginate(query, page=page, per_page=per_page, error_out=False))


@bp.get("/<int:id>")
def detail(id):
    return sukses(ambil_atau_404(Menu, id, "Menu").to_dict())


@bp.post("")
@role_required("admin")
def buat():
    data = validasi_atau_error(ambil_json(), ATURAN)
    _cek_relasi(data)
    menu = Menu(**data)
    db.session.add(menu)
    db.session.commit()
    return sukses(menu.to_dict(), "Menu berhasil dibuat", 201)


@bp.route("/<int:id>", methods=["PUT", "PATCH"])
@role_required("admin")
def ubah(id):
    menu = ambil_atau_404(Menu, id, "Menu")
    data = validasi_atau_error(ambil_json(), ATURAN, parsial=(request.method == "PATCH"))
    _cek_relasi(data)
    for kolom, nilai in data.items():
        setattr(menu, kolom, nilai)
    db.session.commit()
    return sukses(menu.to_dict(), "Menu berhasil diperbarui")


@bp.delete("/<int:id>")
@role_required("admin")
def hapus(id):
    menu = ambil_atau_404(Menu, id, "Menu")
    db.session.delete(menu)
    db.session.commit()
    return sukses(message="Menu berhasil dihapus")

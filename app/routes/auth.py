from flask import Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.extensions import db
from app.models.user import User
from app.utils.errors import ApiError
from app.utils.helpers import ambil_atau_404, ambil_json
from app.utils.responses import sukses
from app.utils.validators import validasi_atau_error

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Kita definisikan aturan dari data yang boleh diterima sistem saat menerima request registrasi dari user.
ATURAN_REGISTER = {
    "username": {"tipe": "str", "wajib": True, "panjang_min": 3, "panjang_maks": 50},
    "email": {"tipe": "str", "wajib": True, "panjang_maks": 100},
    "password": {"tipe": "str", "wajib": True, "panjang_min": 8, "panjang_maks": 100},
}
ATURAN_LOGIN = {
    "username": {"tipe": "str", "wajib": True},
    "password": {"tipe": "str", "wajib": True},
}


@bp.post("/register")
def register():
    """Registrasi untuk publik, di mana Role selalu di-set ke 'viewer'"""
    data = validasi_atau_error(ambil_json(), ATURAN_REGISTER)

    # filter validation untuk data email
    if "@" not in data["email"] or "." not in data["email"].split("@")[-1]:
        raise ApiError("Validasi gagal", 422, {"email": "format email tidak valid"})

    # kita cek, apakah akun yang diregistrasikan sudah ada di DB sebelumnya?
    sudah_ada = db.session.scalar(
        db.select(User).where(
            (User.username == data["username"]) | (User.email == data["email"])
        )
    )
    if sudah_ada:
        raise ApiError("Username atau email sudah terdaftar", 409)

    user = User(username=data["username"], email=data["email"], role="viewer")
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return sukses(user.to_dict(), "Registrasi berhasil", 201)


@bp.post("/login")
def login():
    data = validasi_atau_error(ambil_json(), ATURAN_LOGIN)

    user = db.session.scalar(db.select(User).where(User.username == data["username"]))
    if user is None or not user.check_password(data["password"]):
        raise ApiError("Username atau password salah", 401)

    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    return sukses(
        {"access_token": token, "token_type": "Bearer", "user": user.to_dict()},
        "Login berhasil",
    )


@bp.get("/me")
@jwt_required()
def me():
    user = ambil_atau_404(User, int(get_jwt_identity()), "User")
    return sukses(user.to_dict())

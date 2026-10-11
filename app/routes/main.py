from flask import Blueprint

from app.extensions import db
from app.utils.responses import gagal, sukses

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return sukses(message="Selamat Datang di API EMBEGEH")

# Iseng untuk cek koneksi ke database
@bp.get("/db-check")
def check_db():
    try:
        db.session.execute(db.select(1))
        return sukses(message="Terhubung ke database")
    except Exception as e:
        return gagal(str(e), 500)

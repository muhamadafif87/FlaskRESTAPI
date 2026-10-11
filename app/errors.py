from flask import Flask
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from app.extensions import db, jwt
from app.utils.errors import ApiError
from app.utils.responses import gagal


def register_error_handlers(app: Flask):
    @app.errorhandler(ApiError)
    def handle_api_error(e: ApiError):
        return gagal(e.message, e.status, e.errors)

    # Jika terjadi error karena data duplicate
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(e: IntegrityError):
        db.session.rollback()
        return gagal("Data melanggar aturan database (duplikat atau relasi tidak valid)", 409)

    @app.errorhandler(HTTPException)
    def handle_http_error(e: HTTPException):
        return gagal(e.description, e.code)

    @jwt.unauthorized_loader
    def token_tidak_ada(pesan):
        return gagal("Token tidak ditemukan. Silakan login terlebih dahulu", 401)

    @jwt.invalid_token_loader
    def token_tidak_valid(pesan):
        return gagal("Token tidak valid", 401)

    @jwt.expired_token_loader
    def token_kedaluwarsa(jwt_header, jwt_payload):
        return gagal("Token sudah kedaluwarsa. Silakan login ulang", 401)

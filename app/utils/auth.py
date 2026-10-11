from functools import wraps

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.utils.errors import ApiError


def role_required(*roles):
    def dekorator(fn):
        @wraps(fn)
        def pembungkus(*args, **kwargs):
            verify_jwt_in_request()  # otomatis return 401 jika token tidak ada / salah / kedaluwarsa
            if get_jwt().get("role") not in roles:
                raise ApiError("Anda tidak memiliki izin untuk aksi ini", 403)
            return fn(*args, **kwargs)

        return pembungkus

    return dekorator

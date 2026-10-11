from flask import jsonify


def sukses(data=None, message=None, status=200, meta=None):
    body = {"status": "success"}
    if message:
        body["message"] = message
    if data is not None:
        body["data"] = data
    if meta is not None:
        body["meta"] = meta
    return jsonify(body), status


def gagal(message, status=400, errors=None):
    body = {"status": "error", "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status


def respon_paginasi(pagination):
    """Mengubah objek pagination Flask-SQLAlchemy menjadi respons JSON."""
    return sukses(
        data=[item.to_dict() for item in pagination.items],
        meta={
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        },
    )

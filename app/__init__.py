from flask import Flask

from app.config import Config
from app.extensions import db, jwt
from app.errors import register_error_handlers
from app.cli import create_admin
from app.routes import register_routes


def create_app(config_override: dict | None = None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config_override: 
        app.config.update(config_override)

    for kunci in ("SQLALCHEMY_DATABASE_URI", "JWT_SECRET_KEY"):
        if not app.config.get(kunci):
            raise RuntimeError(f"Konfigurasi {kunci} belum diisi. Cek file .env")

    # Menghubungkan extension dengan app Flask
    db.init_app(app)
    jwt.init_app(app)

    register_error_handlers(app)
    register_routes(app)
    app.cli.add_command(create_admin)

    return app

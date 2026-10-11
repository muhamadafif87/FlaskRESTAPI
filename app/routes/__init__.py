from app.routes.main import bp as main_bp
from app.routes.auth import bp as auth_bp
from app.routes.sekolah import bp as sekolah_bp
from app.routes.sppg import bp as sppg_bp
from app.routes.menu import bp as menu_bp
from app.routes.produksi import bp as produksi_bp
from app.routes.data_keracunan import bp as keracunan_bp


def register_routes(app):
    for bp in (main_bp, auth_bp, sekolah_bp, sppg_bp, menu_bp, produksi_bp, keracunan_bp):
        app.register_blueprint(bp)

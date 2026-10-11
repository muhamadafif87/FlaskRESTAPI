# Semua model di-import di sini agar SQLAlchemy mengenali relasi antar tabel
from app.models.user import User
from app.models.sekolah import Sekolah
from app.models.sppg import Sppg
from app.models.menu import Menu
from app.models.produksi import Produksi
from app.models.data_keracunan import DataKeracunan

__all__ = ["User", "Sekolah", "Sppg", "Menu", "Produksi", "DataKeracunan"]

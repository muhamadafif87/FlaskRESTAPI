from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.mixins import BigPK, SerializerMixin, TimestampMixin

JENJANG = ("SD", "SMP", "SMA", "SMK")


class Sekolah(SerializerMixin, TimestampMixin, db.Model):
    __tablename__ = "sekolah"

    id: Mapped[int] = mapped_column(BigPK, primary_key=True)
    nama_sekolah: Mapped[str] = mapped_column(String(150))
    jumlah_siswa: Mapped[int] = mapped_column(Integer)
    alamat_sekolah: Mapped[str] = mapped_column(String(255))
    jenjang: Mapped[str] = mapped_column(
        ENUM(*JENJANG, name="enum_jenjang", create_type=False), server_default="SD"
    )
    email_sekolah: Mapped[Optional[str]] = mapped_column(String(100))
    nomor_telepon: Mapped[Optional[str]] = mapped_column(String(20))

    def __repr__(self) -> str:
        return f"Sekolah(id={self.id!r}, nama_sekolah={self.nama_sekolah!r}, jenjang={self.jenjang!r})"

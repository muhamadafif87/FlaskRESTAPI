from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.mixins import BigPK, SerializerMixin, TimestampMixin

TINGKAT_KEPARAHAN = ("Ringan", "Sedang", "Berat")


class DataKeracunan(SerializerMixin, TimestampMixin, db.Model):
    __tablename__ = "data_keracunan"

    id: Mapped[int] = mapped_column(BigPK, primary_key=True)
    id_sekolah: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sekolah.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    jumlah_siswa: Mapped[int] = mapped_column(Integer)
    id_sppg: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sppg.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    waktu_kejadian: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    tingkat_keparahan: Mapped[Optional[str]] = mapped_column(String(20), server_default="Sedang")
    gejala_dominan: Mapped[Optional[str]] = mapped_column(String(150))
    status_penanganan: Mapped[Optional[str]] = mapped_column(
        String(30), server_default="Dalam Investigasi"
    )
    catatan_medis: Mapped[Optional[str]] = mapped_column(Text)

    def __repr__(self) -> str:
        return f"DataKeracunan(id={self.id!r}, id_sekolah={self.id_sekolah!r})"

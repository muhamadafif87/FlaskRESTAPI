from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.mixins import BigPK, SerializerMixin, TimestampMixin

STATUS_OPERASIONAL = ("Aktif", "Nonaktif", "Dalam Investigasi")


class Sppg(SerializerMixin, TimestampMixin, db.Model):
    __tablename__ = "sppg"

    id: Mapped[int] = mapped_column(BigPK, primary_key=True)
    nama_sppg: Mapped[str] = mapped_column(String(150))
    alamat: Mapped[str] = mapped_column(String(255))
    jumlah_karyawan: Mapped[int] = mapped_column(Integer)
    id_sekolah: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("sekolah.id", ondelete="SET NULL", onupdate="CASCADE")
    )
    kapasitas_produksi_harian: Mapped[Optional[int]] = mapped_column(Integer, server_default="1000")
    nomor_izin_edar: Mapped[Optional[str]] = mapped_column(String(50), unique=True)
    status_operasional: Mapped[Optional[str]] = mapped_column(String(20), server_default="Aktif")
    penanggung_jawab: Mapped[Optional[str]] = mapped_column(String(100))

    def __repr__(self) -> str:
        return f"Sppg(id={self.id!r}, nama_sppg={self.nama_sppg!r})"

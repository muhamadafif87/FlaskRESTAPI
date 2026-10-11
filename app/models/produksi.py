from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.mixins import BigPK, SerializerMixin, TimestampMixin

STATUS_QC = ("Lolos", "Gagal", "Karantina")


class Produksi(SerializerMixin, TimestampMixin, db.Model):
    __tablename__ = "produksi"

    id: Mapped[int] = mapped_column(BigPK, primary_key=True)
    batch_produksi: Mapped[int] = mapped_column(Integer)
    waktu_produksi: Mapped[date] = mapped_column(Date, server_default=func.current_date())
    id_sppg: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sppg.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    id_menu: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("menu.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    jumlah_porsi: Mapped[int] = mapped_column(Integer)
    status_qc: Mapped[str] = mapped_column(
        ENUM(*STATUS_QC, name="enum_status_qc", create_type=False), server_default="Lolos"
    )
    suhu_simpan_celsius: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 1))
    waktu_distribusi: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        return f"Produksi(id={self.id!r}, batch_produksi={self.batch_produksi!r})"

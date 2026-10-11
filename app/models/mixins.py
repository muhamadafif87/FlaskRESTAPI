from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

#variabel ini digunakan untuk column dengan tipe data BIGSERIAL yang tidak ada di sqlalchemy
BigPK = BigInteger().with_variant(Integer, "sqlite")


class SerializerMixin:
    """Memberi method to_dict() agar model bisa diubah menjadi format JSON."""

    _sembunyikan = ()  # digunakan untuk menyembunyikan nama kolom yang tidak boleh ikut ditampilkan

    def to_dict(self):
        hasil = {}
        for kolom in self.__table__.columns:
            if kolom.name in self._sembunyikan:
                continue
            nilai = getattr(self, kolom.key)
            if isinstance(nilai, (datetime, date)):
                nilai = nilai.isoformat()
            elif isinstance(nilai, Decimal):
                nilai = float(nilai)
            hasil[kolom.name] = nilai
        return hasil


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

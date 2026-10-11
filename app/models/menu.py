from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import db
from app.models.mixins import BigPK, SerializerMixin, TimestampMixin

RASA = ("Gurih", "Manis", "Pedas", "Asam", "Netral")


class Menu(SerializerMixin, TimestampMixin, db.Model):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(BigPK, primary_key=True)
    nama_menu: Mapped[str] = mapped_column(String(150))
    rasa: Mapped[str] = mapped_column(
        ENUM(*RASA, name="enum_rasa", create_type=False), server_default="Gurih"
    )
    id_produksi: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey(
            "produksi.id", ondelete="SET NULL", onupdate="CASCADE",
            use_alter=True, name="fk_menu_produksi",
        )
    )
    id_sppg: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sppg.id", ondelete="CASCADE", onupdate="CASCADE")
    )
    kalori_kcal: Mapped[Optional[int]] = mapped_column(Integer)
    biaya_per_porsi: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2))
    is_halal: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text("true"))
    kategori_gizi: Mapped[Optional[str]] = mapped_column(
        String(50), server_default="Kombinasi Seimbang"
    )

    def __repr__(self) -> str:
        return f"Menu(id={self.id!r}, nama_menu={self.nama_menu!r})"

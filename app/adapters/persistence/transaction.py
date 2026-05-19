# adapters/persistence/transaction.py
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.persistence.base import Base
from app.domain.models.repetition import Repetition

if TYPE_CHECKING:
    from app.adapters.persistence.category import CategoryORM


class TransactionORM(Base):
    __tablename__ = "transaction"

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    repetition: Mapped[Optional[Repetition]] = mapped_column(
        Enum(Repetition), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("category.id", ondelete="SET NULL")
    )
    category: Mapped[Optional["CategoryORM"]] = relationship(
        "CategoryORM", back_populates="transactions"
    )

# adapters/persistence/transaction.py
from sqlalchemy import Integer, Text, Numeric, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.adapters.persistence.base import Base
from app.adapters.persistence.category import CategoryORM


class TransactionORM(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    cash_value: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    repetition: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    category_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("category.id", ondelete="cascade")
    )
    category: Mapped[Optional[CategoryORM]] = relationship("CategoryORM", back_populates="transactions")
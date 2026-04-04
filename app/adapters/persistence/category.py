from datetime import datetime
from typing import List

from app.adapters.persistence.base import Base
from sqlalchemy import TIMESTAMP, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.persistence.transaction import TransactionORM

class CategoryORM(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    transactions: Mapped[List[TransactionORM]] = relationship("TransactionORM", back_populates="category", cascade="all, delete-orphan")
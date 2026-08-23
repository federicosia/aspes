from datetime import datetime, timedelta, timezone

from sqlalchemy import TIMESTAMP, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.persistence.base import Base
from app.domain.models.family import Family


class RefreshTokenORM(Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(nullable=False, unique=True)
    family: Mapped[Family] = mapped_column(Enum(Family), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now(timezone.utc) + timedelta(days=15),
    )
    revoked: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("_user.id", ondelete="CASCADE"), nullable=False
    )

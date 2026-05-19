from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.persistence.base import Base
from app.domain.models.role import Role
from app.domain.models.status import Status


class UserORM(Base):
    __tablename__ = "_user"

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status), nullable=False)

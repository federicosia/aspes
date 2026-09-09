from dataclasses import dataclass

from app.domain.models.role import Role
from app.domain.models.status import Status


@dataclass
class User:
    name: str
    surname: str
    username: str
    email: str
    password: str
    role: Role
    id: int | None = None
    status: Status = Status.ENABLED

    def disable(self) -> None:
        self.status = Status.DISABLED

    def enable(self) -> None:
        self.status = Status.ENABLED

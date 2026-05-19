from dataclasses import dataclass

from app.domain.models.role import Role
from app.domain.models.status import Status


@dataclass
class User:
    id: int
    name: str
    surname: str
    username: str
    email: str
    password: str
    role: Role
    status: Status

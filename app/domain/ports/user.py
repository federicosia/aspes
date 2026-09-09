from abc import abstractmethod

from app.domain.models.user import User
from app.domain.ports.repository import AbstractRepository


class AbstractUserRepository(AbstractRepository[User]):
    @abstractmethod
    def get_by_username(self, username: str) -> User | None: ...
    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

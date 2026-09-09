from abc import abstractmethod
from typing import Protocol


class AbstractRefreshTokenRepository(Protocol):
    @abstractmethod
    def create(self, user_id: int, token: str) -> None: ...

from __future__ import annotations

from abc import ABC, abstractmethod
from app.domain.ports.category import AbstractCategoryRepository
from app.domain.ports.transaction import AbstractTransactionRepository
from app.domain.ports.refresh_token import AbstractRefreshTokenRepository
from app.domain.ports.user import AbstractUserRepository


class AbstractCategoryUnitOfWork(ABC):
    categories: AbstractCategoryRepository
    transactions: AbstractTransactionRepository

    @abstractmethod
    def __enter__(
        self,
    ) -> "AbstractCategoryUnitOfWork": ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError("Commit not implemented")

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError("Rollback not implemented")


class AbstractUserUnitOfWork(ABC):
    users: AbstractUserRepository
    refresh_tokens: AbstractRefreshTokenRepository

    @abstractmethod
    def __enter__(
        self,
    ) -> "AbstractUserUnitOfWork": ...

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None: ...

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError("Commit not implemented")

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError("Rollback not implemented")

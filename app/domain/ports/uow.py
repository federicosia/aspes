from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.adapters.repositories.sql.category import CategoryRepository
    from app.adapters.repositories.sql.transaction import TransactionRepository
    from app.adapters.repositories.sql.user import UserRepository


class AbstractCategoryUnitOfWork(ABC):
    categories: CategoryRepository
    transactions: TransactionRepository

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
    users: UserRepository

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

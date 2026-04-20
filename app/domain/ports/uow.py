from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.domain.ports.repository import AbstractRepository

CategoryRepository = TypeVar("CategoryRepository", bound=AbstractRepository)
TransactionRepository = TypeVar("TransactionRepository", bound=AbstractRepository)


class AbstractUnitOfWork(ABC, Generic[CategoryRepository, TransactionRepository]):
    categories: CategoryRepository
    transactions: TransactionRepository

    @abstractmethod
    def __enter__(
        self,
    ) -> "AbstractUnitOfWork[CategoryRepository, TransactionRepository]":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError("Commit not implemented")

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError("Rollback not implemented")

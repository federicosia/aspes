from abc import ABC, abstractmethod

from app.domain.ports.repository import AbstractRepository

class AbstractUnitOfWork(ABC):

    categories: AbstractRepository
    transactions: AbstractRepository

    @abstractmethod
    def __enter__(self) -> "AbstractUnitOfWork":
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
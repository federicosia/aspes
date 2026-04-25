from abc import ABC, abstractmethod


class AbstractUnitOfWork[CategoryRepository, TransactionRepository](ABC):
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

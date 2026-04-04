import abc

class AbstractUnitOfWork(abc.ABC):

    @abc.abstractmethod
    def __enter__(self) -> "AbstractUnitOfWork":
        pass

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abc.abstractmethod
    def commit(self) -> None:
        raise NotImplementedError("Commit not implemented")

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError("Rollback not implemented")
import abc
from typing import Any

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, entity: Any) -> Any:
        pass

    @abc.abstractmethod
    def get_by_id(self, id: int) -> Any | None:
        pass

    @abc.abstractmethod
    def list(self) -> list:
        pass

    def update(self, entity: Any) -> Any | None:
        pass

    @abc.abstractmethod
    def delete(self, id: int) -> bool:
        pass
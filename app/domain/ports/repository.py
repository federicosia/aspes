from abc import ABC, abstractmethod
from typing import List, Optional


class AbstractRepository[T](ABC):
    @abstractmethod
    def add(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        pass

    @abstractmethod
    def list(self, **filters) -> List[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

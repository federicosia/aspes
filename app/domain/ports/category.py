from abc import abstractmethod

from app.domain.models.category import Category
from app.domain.ports.repository import AbstractRepository


class AbstractCategoryRepository(AbstractRepository[Category]):
    @abstractmethod
    def get_by_name(self, name: str) -> Category | None: ...

from abc import abstractmethod
from typing import List

from app.domain.models.transaction import Transaction
from app.domain.ports.repository import AbstractRepository


class AbstractTransactionRepository(AbstractRepository[Transaction]):
    @abstractmethod
    def list_by_category_id(self, category_id: int) -> List[Transaction]: ...

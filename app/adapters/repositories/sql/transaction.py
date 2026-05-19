from typing import List

from sqlalchemy.orm import Session

from app.adapters.persistence.transaction import TransactionORM
from app.adapters.repositories.sql.sql_repository import SqlRepository
from app.domain.models.transaction import Transaction


class TransactionRepository(SqlRepository[Transaction, TransactionORM]):
    def __init__(
        self, session: Session, model_orm: type[TransactionORM] = TransactionORM
    ):
        super().__init__(session, model_orm)

    def to_domain(self, entity: TransactionORM) -> Transaction:
        return Transaction(
            id=entity.id,
            amount=entity.amount,
            category_id=entity.category_id,
            description=entity.description,
            repetition=entity.repetition,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_persistence(self, entity: Transaction) -> TransactionORM:
        return TransactionORM(
            id=entity.id,
            amount=entity.amount,
            category_id=entity.category_id,
            description=entity.description,
            repetition=entity.repetition,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def list_by_category_id(self, transaction_id: int) -> List[Transaction]:
        transactions_orm = (
            self._session.query(TransactionORM)
            .filter_by(category_id=transaction_id)
            .all()
        )
        return [self.to_domain(transaction_orm) for transaction_orm in transactions_orm]

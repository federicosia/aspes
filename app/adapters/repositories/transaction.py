from sqlalchemy.orm import Session
from app.adapters.mappers.transaction import TransactionMapper
from app.adapters.persistence.transaction import TransactionORM
from app.domain.models.transaction import Transaction
from app.domain.ports.repository import AbstractRepository


class TransactionRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: Transaction) -> Transaction:
        transaction_orm = TransactionMapper.to_persistence(entity)
        self.session.add(transaction_orm)
        self.session.flush()
        return TransactionMapper.to_domain(transaction_orm)

    def get_by_id(self, id: int) -> Transaction | None:
        transaction_orm = self.session.query(TransactionORM).filter_by(id=id).first()
        if transaction_orm:
            return TransactionMapper.to_domain(transaction_orm)
        return None

    def list(self) -> list[Transaction]:
        return [
            TransactionMapper.to_domain(transaction_orm)
            for transaction_orm in self.session.query(TransactionORM).all()
        ]

    def update(self, entity: Transaction) -> Transaction | None:
        transaction_orm = (
            self.session.query(TransactionORM).filter_by(id=entity.id).first()
        )
        if transaction_orm:
            transaction_orm.amount = entity.amount
            transaction_orm.category_id = entity.category_id
            transaction_orm.description = entity.description
            transaction_orm.repetition = entity.repetition
            self.session.flush()
            return TransactionMapper.to_domain(transaction_orm)
        return None

    def delete(self, id: int) -> bool:
        transaction_orm = self.get_by_id(id)
        if transaction_orm:
            self.session.delete(transaction_orm)
            self.session.flush()
            return True
        return False

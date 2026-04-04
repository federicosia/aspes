from typing import Any
from sqlalchemy.orm import Session
from app.adapters.mappers.transaction import TransactionMapper
from app.adapters.persistence.transaction import TransactionORM
from app.domain.models.transaction import Transaction
from app.domain.ports.repository import AbstractRepository


class TransactionRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: Transaction) -> Transaction:
        transaction_orm = TransactionORM(**entity.__dict__)
        self.session.add(transaction_orm)
        self.session.commit()
        return TransactionMapper.to_domain(transaction_orm)

    def get_by_id(self, id: int) -> Transaction | None:
        transaction_orm = self.session.query(TransactionORM).filter_by(id=id).first()
        if transaction_orm:
            return TransactionMapper.to_domain(transaction_orm)
        return None

    def list(self) -> list[Transaction]:
        return [TransactionMapper.to_domain(transaction_orm) for transaction_orm in self.session.query(TransactionORM).all()]

    def update(self, entity: Transaction) -> Transaction | None:
        transaction_orm = self.session.query(TransactionORM).filter_by(id=entity.id).first()
        if transaction_orm:
            for key, value in entity.__dict__.items():
                setattr(transaction_orm, key, value)
            self.session.commit()
            return TransactionMapper.to_domain(transaction_orm)
        return None

    def delete(self, id: int) -> bool:
        transaction_orm = self.get_by_id(id)
        if transaction_orm:
            self.session.delete(transaction_orm)
            self.session.commit()
            return True
        return False

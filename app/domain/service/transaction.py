from datetime import datetime

from app.domain.exceptions.category import CategoryNotFound
from app.domain.models.transaction import Transaction
from app.domain.ports.uow import AbstractUnitOfWork
from app.adapters.repositories.category import CategoryRepository
from app.adapters.repositories.transaction import TransactionRepository
from decimal import Decimal


def get_transaction(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository], id: int
):
    with uow:
        return uow.transactions.get_by_id(id)


def create_transaction(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository],
    amount: Decimal,
    description: str | None,
    repetition: datetime | None,
    category_id: int,
):
    with uow:
        category = uow.categories.get_by_id(category_id)
        if category is None:
            raise CategoryNotFound(category_id=category_id)
        transaction = Transaction(
            amount=amount,
            description=description,
            repetition=repetition,
            category_id=category_id,
        )
        transaction = uow.transactions.add(transaction)
        uow.commit()
        return transaction


def delete_transaction(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository], id: int
):
    with uow:
        transaction = uow.transactions.get_by_id(id)
        if transaction and transaction.id:
            uow.transactions.delete(transaction.id)
            uow.commit()

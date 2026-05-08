from decimal import Decimal
from typing import List

from app.adapters.repositories.category import CategoryRepository
from app.adapters.repositories.transaction import TransactionRepository
from app.domain.exceptions.category import CategoryNotFound
from app.domain.models.repetition import Repetition
from app.domain.models.transaction import Transaction
from app.domain.ports.uow import AbstractUnitOfWork


def get_transaction(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository], id: int
):
    with uow:
        return uow.transactions.get_by_id(id)


def create_transaction(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository],
    amount: Decimal,
    description: str | None,
    repetition: Repetition | None,
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


def get_list_transactions_by_category_id(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository], id: int
) -> List[Transaction]:
    with uow:
        return uow.transactions.list_by_category_id(id)


def delete_transaction(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository], id: int
):
    with uow:
        transaction = uow.transactions.get_by_id(id)
        if transaction and transaction.id:
            uow.transactions.delete(transaction.id)
            uow.commit()

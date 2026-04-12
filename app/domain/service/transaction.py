from datetime import datetime

from app.domain.models.transaction import Transaction
from app.domain.ports.uow import AbstractUnitOfWork
from decimal import Decimal


def get_transaction(uow: AbstractUnitOfWork, id: int):
    with uow:
        return uow.transactions.get_by_id(id)


def create_transaction(
    uow: AbstractUnitOfWork,
    amount: Decimal,
    description: str | None,
    repetition: datetime | None,
    category_id: int,
):
    with uow:
        transaction = Transaction(
            amount=amount,
            description=description,
            repetition=repetition,
            category_id=category_id,
        )
        transaction = uow.transactions.add(transaction)
        uow.commit()
        return transaction


def delete_transaction(uow: AbstractUnitOfWork, id: int):
    with uow:
        transaction = uow.transactions.get_by_id(id)
        if transaction:
            uow.transactions.delete(transaction)
            uow.commit()

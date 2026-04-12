from app.domain.models.transaction import Transaction
from adapters.persistence.transaction import TransactionORM
from decimal import Decimal


class TransactionMapper:
    @staticmethod
    def to_domain(transaction_model: TransactionORM) -> Transaction:
        return Transaction(
            id=transaction_model.id,
            amount=transaction_model.cash_value,
            category_id=transaction_model.category_id,
            description=transaction_model.description,
            repetition=transaction_model.repetition,
            created_at=transaction_model.created_at,
            updated_at=transaction_model.updated_at,
        )

    @staticmethod
    def to_persistence(transaction: Transaction) -> TransactionORM:
        return TransactionORM(
            id=transaction.id,
            cash_value=transaction.amount,
            category_id=transaction.category_id,
            description=transaction.description,
            repetition=transaction.repetition,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )

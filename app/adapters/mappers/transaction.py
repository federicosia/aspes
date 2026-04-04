from app.domain.models.transaction import Transaction
from adapters.persistence.transaction import TransactionORM

class TransactionMapper:

    @staticmethod
    def to_domain(transaction_model: TransactionORM) -> Transaction:
        return Transaction(
            id=transaction_model.id,
            cash_value=transaction_model.cash_value,
            description=transaction_model.description,
            repetition=transaction_model.repetition,
            created_at=transaction_model.created_at,
            updated_at=transaction_model.updated_at,
        )
    
    @staticmethod
    def to_persistence(transaction: Transaction) -> TransactionORM:
        return TransactionORM(
            id=transaction.id,
            cash_value=transaction.cash_value,
            description=transaction.description,
            repetition=transaction.repetition,
            created_at=transaction.created_at,
            updated_at=transaction.updated_at,
        )
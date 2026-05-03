from decimal import Decimal

from app.adapters.mappers.transaction import TransactionMapper
from app.domain.models.repetition import Repetition
from app.domain.models.transaction import Transaction
from app.adapters.persistence.transaction import TransactionORM


def test_transaction_orm_mapper():
    transaction_model = Transaction(
        id=1,
        amount=Decimal(100.0),
        category_id=2,
        description="Test Transaction",
        repetition=Repetition.MONTHLY,
    )
    transaction_orm = TransactionMapper.to_persistence(transaction_model)
    assert transaction_orm.id == transaction_model.id
    assert transaction_orm.amount == transaction_model.amount
    assert transaction_orm.category_id == transaction_model.category_id
    assert transaction_orm.description == transaction_model.description
    assert transaction_orm.repetition == transaction_model.repetition
    assert transaction_orm.created_at == transaction_model.created_at
    assert transaction_orm.updated_at == transaction_model.updated_at


def test_transaction_model_mapper():
    transaction_orm = TransactionORM(
        id=1,
        amount=Decimal(100.0),
        category_id=2,
        description="Test Transaction",
        repetition=Repetition.MONTHLY,
    )
    transaction_model = TransactionMapper.to_domain(transaction_orm)
    assert transaction_model.id == transaction_orm.id
    assert transaction_model.amount == transaction_orm.amount
    assert transaction_model.category_id == transaction_orm.category_id
    assert transaction_model.description == transaction_orm.description
    assert transaction_model.repetition == transaction_orm.repetition
    assert transaction_model.created_at == transaction_orm.created_at
    assert transaction_model.updated_at == transaction_orm.updated_at

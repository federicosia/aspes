from decimal import Decimal

from app.domain.models.category import Category
from app.domain.service.transaction import (
    create_transaction,
    delete_transaction,
    get_transaction,
)


def test_create_transaction(fake_uow):
    with fake_uow:
        category = fake_uow.categories.add(
            Category(id=1, name="Test Category", description="A test category")
        )
        transaction = create_transaction(
            fake_uow,
            amount=Decimal(100.00),
            description="Test Transaction",
            repetition=None,
            category_id=category.id,
        )
        assert transaction is not None
        assert transaction.id is not None
        assert transaction.amount == Decimal(100.00)
        assert transaction.description == "Test Transaction"
        assert transaction.category_id == category.id


def test_get_transaction(fake_uow):
    with fake_uow:
        category = fake_uow.categories.add(
            Category(id=1, name="Test Category", description="A test category")
        )
        transaction = create_transaction(
            fake_uow,
            amount=Decimal(100.00),
            description="Test Transaction",
            repetition=None,
            category_id=category.id,
        )
        assert transaction is not None
        assert transaction.id is not None
        transaction_res = get_transaction(fake_uow, transaction.id)
        assert transaction_res is not None
        assert transaction_res.id == transaction.id
        assert transaction_res.amount == Decimal(100.00)
        assert transaction_res.description == "Test Transaction"
        assert transaction_res.category_id == category.id


def test_delete_transaction(fake_uow):
    with fake_uow:
        category = fake_uow.categories.add(
            Category(id=1, name="Test Category", description="A test category")
        )
        transaction = create_transaction(
            fake_uow,
            amount=Decimal(100.00),
            description="Test Transaction",
            repetition=None,
            category_id=category.id,
        )
        assert transaction is not None
        assert transaction.id is not None
        delete_transaction(fake_uow, transaction.id)
        assert get_transaction(fake_uow, transaction.id) is None

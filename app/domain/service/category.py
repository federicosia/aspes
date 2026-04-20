from app.domain.models.category import Category
from app.domain.ports.uow import AbstractUnitOfWork
from app.adapters.repositories.category import CategoryRepository
from app.adapters.repositories.transaction import TransactionRepository


def get_category(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository], id: int
) -> Category | None:
    with uow:
        return uow.categories.get_by_id(id)


def create_category(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository],
    name: str,
    description: str | None = None,
) -> Category:
    with uow:
        category = uow.categories.get_by_name(name)
        if category is not None:
            return category
        category = uow.categories.add(Category(name=name, description=description))
        uow.commit()
        return category


def delete_category(
    uow: AbstractUnitOfWork[CategoryRepository, TransactionRepository], id: int
) -> None:
    with uow:
        uow.categories.delete(id)

from app.domain.models.category import Category
from app.domain.ports.uow import AbstractUnitOfWork


def get_category(uow: AbstractUnitOfWork, id: int) -> Category | None:
    with uow:
        return uow.categories.get_by_id(id)


def create_category(
    uow: AbstractUnitOfWork, name: str, description: str | None = None
) -> Category:
    with uow:
        category = uow.categories.add(Category(name=name, description=description))
        uow.commit()
        return category


def delete_category(uow: AbstractUnitOfWork, id: int) -> None:
    with uow:
        uow.categories.delete(id)

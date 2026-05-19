from app.domain.models.category import Category
from app.domain.ports.uow import AbstractCategoryUnitOfWork


def get_category(uow: AbstractCategoryUnitOfWork, id: int) -> Category | None:
    with uow:
        return uow.categories.get_by_id(id)


def create_category(
    uow: AbstractCategoryUnitOfWork,
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


def delete_category(uow: AbstractCategoryUnitOfWork, id: int) -> None:
    with uow:
        uow.categories.delete(id)

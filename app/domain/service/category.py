from app.domain.models.category import Category
from app.domain.ports.uow import AbstractUnitOfWork


def get_category(uow: AbstractUnitOfWork, id: int) -> Category | None:
    with uow:
        return uow.categories.get(id)
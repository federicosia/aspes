from app.adapters.uow.sql_uow import (
    SQLAchemyUserUnitOfWork,
    SQLAlchemyCategoryUnitOfWork,
)
from app.domain.ports.uow import AbstractCategoryUnitOfWork, AbstractUserUnitOfWork


def get_category_uow() -> AbstractCategoryUnitOfWork:
    return SQLAlchemyCategoryUnitOfWork()


def get_auth_uow() -> AbstractUserUnitOfWork:
    return SQLAchemyUserUnitOfWork()

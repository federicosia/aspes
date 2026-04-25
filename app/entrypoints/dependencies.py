from app.domain.ports.uow import AbstractUnitOfWork
from app.adapters.uow.sql_uow import SQLAlchemyUnitOfWork
from app.adapters.repositories.category import CategoryRepository
from app.adapters.repositories.transaction import TransactionRepository


def get_uow() -> AbstractUnitOfWork[CategoryRepository, TransactionRepository]:
    return SQLAlchemyUnitOfWork()

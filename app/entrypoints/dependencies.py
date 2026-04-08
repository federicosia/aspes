from app.domain.ports.uow import AbstractUnitOfWork
from app.adapters.uow.sql_uow import SQLAlchemyUnitOfWork

def get_uow() -> AbstractUnitOfWork:
    return SQLAlchemyUnitOfWork()
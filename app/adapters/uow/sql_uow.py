from app.adapters.repositories.category import CategoryRepository
from app.adapters.repositories.transaction import TransactionRepository
from app.db.session import DEFAULT_SESSION_FACTORY
from app.domain.ports.uow import AbstractUnitOfWork


class SQLAlchemyUnitOfWork(AbstractUnitOfWork[CategoryRepository, TransactionRepository]):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.categories = CategoryRepository(self.session)
        self.transactions = TransactionRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

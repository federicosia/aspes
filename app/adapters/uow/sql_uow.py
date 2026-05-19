from app.adapters.persistence.category import CategoryORM
from app.adapters.persistence.transaction import TransactionORM
from app.adapters.repositories.sql.category import CategoryRepository
from app.adapters.repositories.sql.transaction import TransactionRepository
from app.adapters.repositories.sql.user import UserRepository
from app.db.session import DEFAULT_SESSION_FACTORY
from app.domain.ports.uow import AbstractCategoryUnitOfWork, AbstractUserUnitOfWork


class SQLAlchemyCategoryUnitOfWork(AbstractCategoryUnitOfWork):
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


class SQLAchemyUserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)
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

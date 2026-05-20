import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.adapters.persistence.base import Base
from app.adapters.repositories.sql.category import CategoryRepository
from app.adapters.repositories.sql.transaction import TransactionRepository
from app.adapters.repositories.sql.user import UserRepository
from app.domain.ports.uow import AbstractCategoryUnitOfWork
from app.entrypoints.dependencies import get_auth_uow, get_category_uow
from main import app


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:18-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture
def fake_uow(session):
    class FakeUnitOfWork(AbstractCategoryUnitOfWork):
        def __init__(self, categories, transactions, users):
            self.categories = categories
            self.transactions = transactions
            self.users = users

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def commit(self) -> None:
            pass

        def rollback(self) -> None:
            pass

    return FakeUnitOfWork(
        CategoryRepository(session),
        TransactionRepository(session),
        UserRepository(session),
    )


@pytest.fixture()
def test_client(fake_uow):
    app.dependency_overrides[get_category_uow] = lambda: fake_uow
    app.dependency_overrides[get_auth_uow] = lambda: fake_uow
    yield TestClient(app)
    app.dependency_overrides.clear()

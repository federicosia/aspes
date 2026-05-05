import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.adapters.persistence.base import Base
from app.domain.ports.repository import AbstractRepository
from app.domain.ports.uow import AbstractUnitOfWork
from app.entrypoints.dependencies import get_uow
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
    transaction.rollback()
    connection.close()


class FakeRepository(AbstractRepository):
    def __init__(self, items):
        self._items = list(items)
        self._next_id = max((item.id for item in self._items if item.id), default=0) + 1

    def add(self, entity):
        if entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        self._items.append(entity)
        return entity

    def get_by_id(self, id):
        for item in self._items:
            if item.id == id:
                return item
        return None

    def list(self):
        return list(self._items)

    def get_by_name(self, name):
        for item in self._items:
            if item.name == name:
                return item
        return None

    def delete(self, id) -> bool:
        initial_count = len(self._items)
        self._items = [item for item in self._items if item.id != id]
        return len(self._items) != initial_count


class FakeUnitOfWork(AbstractUnitOfWork[FakeRepository, FakeRepository]):
    def __init__(self, categories, transactions):
        self.categories = FakeRepository(categories)
        self.transactions = FakeRepository(transactions)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass


@pytest.fixture
def fake_uow():
    return FakeUnitOfWork({}, {})


@pytest.fixture
def fake_repository():
    return FakeRepository([])


@pytest.fixture
def client(fake_uow):
    app.dependency_overrides[get_uow] = lambda: fake_uow
    yield TestClient(app)
    app.dependency_overrides.clear()

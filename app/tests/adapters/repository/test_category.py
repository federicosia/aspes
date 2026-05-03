import pytest

from app.adapters.repositories.category import CategoryRepository
from app.domain.models.category import Category


@pytest.fixture
def repository(session):
    return CategoryRepository(session)


@pytest.fixture
def persisted_category(repository):
    category = Category(name="Test Category", description="A category for testing")
    return repository.add(category)


def test_list_categories(repository, persisted_category):
    categories = repository.list()
    assert len(categories) == 1
    assert categories[0].name == persisted_category.name
    assert categories[0].description == persisted_category.description


def test_get_category_by_id(repository, persisted_category):
    category = repository.get_by_id(persisted_category.id)
    assert category is not None
    assert category.name == persisted_category.name
    assert category.description == persisted_category.description


def test_get_category_by_name(repository, persisted_category):
    category = repository.get_by_name(persisted_category.name)
    assert category is not None
    assert category.id == persisted_category.id
    assert category.description == persisted_category.description


def test_get_category_by_id_not_found(repository):
    category = repository.get_by_id(999)
    assert category is None


def test_update_modifies_persisted_data(repository, persisted_category):
    persisted_category.name = "Updated description"
    repository.update(persisted_category)

    # rileggi dal db per essere sicuro
    fetched = repository.get_by_id(persisted_category.id)
    assert fetched.name == "Updated description"


def test_delete_persisted_category(repository, persisted_category):
    result = repository.delete(persisted_category.id)
    assert result is True

    # verifica che non esista più
    category = repository.get_by_id(persisted_category.id)
    assert category is None

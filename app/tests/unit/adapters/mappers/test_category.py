from app.adapters.mappers.category import CategoryMapper
from app.domain.models.category import Category
from app.adapters.persistence.category import CategoryORM


def test_category_orm_mapper():
    category_model = Category(id=1, name="Test Category")
    category_orm = CategoryMapper.to_persistence(category_model)
    assert category_orm.id == category_model.id
    assert category_orm.name == category_model.name
    assert category_orm.transactions == category_model.transactions
    assert category_orm.created_at == category_model.created_at
    assert category_orm.updated_at == category_model.updated_at
    assert category_orm.description == category_model.description


def test_category_model_mapper():
    category_orm: CategoryORM = CategoryORM(id=1, name="Test Category")
    category_model: Category = CategoryMapper.to_domain(category_orm)
    assert category_model.id == category_orm.id
    assert category_model.name == category_orm.name
    assert category_model.transactions == category_orm.transactions
    assert category_model.created_at == category_orm.created_at
    assert category_model.updated_at == category_orm.updated_at
    assert category_model.description == category_orm.description

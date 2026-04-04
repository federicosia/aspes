# adapters/persistence/mappers/category_mapper.py
from app.domain.models.category import Category
from adapters.persistence.category import CategoryORM


class CategoryMapper:

    @staticmethod
    def to_domain(model: CategoryORM) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_persistence(category: Category) -> CategoryORM:
        return CategoryORM(
            id=category.id,
            name=category.name,
            description=category.description,
            created_at=category.created_at,
            updated_at=category.updated_at,
        )
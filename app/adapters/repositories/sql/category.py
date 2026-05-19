from typing import Optional

from sqlalchemy.orm import Session

from app.adapters.persistence.category import CategoryORM
from app.adapters.repositories.sql.sql_repository import SqlRepository
from app.domain.models.category import Category


class CategoryRepository(SqlRepository[Category, CategoryORM]):
    def __init__(self, session: Session, model_orm: type[CategoryORM] = CategoryORM):
        super().__init__(session, model_orm)

    def to_domain(self, entity: CategoryORM) -> Category:
        return Category(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_persistence(self, entity: Category) -> CategoryORM:
        return CategoryORM(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def get_by_name(self, name: str) -> Optional[Category]:
        category_orm = self._session.query(CategoryORM).filter_by(name=name).first()
        if category_orm:
            return self.to_domain(category_orm)
        return None

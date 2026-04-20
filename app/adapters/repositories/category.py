from sqlalchemy.orm import Session

from app.adapters.mappers.category import CategoryMapper
from app.adapters.persistence.category import CategoryORM
from app.domain.models.category import Category
from app.domain.ports.repository import AbstractRepository


class CategoryRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def list(self) -> list[Category]:
        return [
            CategoryMapper.to_domain(category_orm)
            for category_orm in self.session.query(CategoryORM).all()
        ]

    def get_by_id(self, id: int) -> Category | None:
        category_orm = self.session.query(CategoryORM).filter_by(id=id).first()
        if category_orm:
            return CategoryMapper.to_domain(category_orm)
        return None

    def get_by_name(self, name: str) -> Category | None:
        category_orm = self.session.query(CategoryORM).filter_by(name=name).first()
        if category_orm:
            return CategoryMapper.to_domain(category_orm)
        return None

    def add(self, entity: Category) -> Category:
        new_category = CategoryORM(
            name=entity.name,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
        self.session.add(new_category)
        self.session.flush()
        return CategoryMapper.to_domain(new_category)

    def update(self, entity: Category) -> Category | None:
        category_orm = self.session.query(CategoryORM).filter_by(id=entity.id).first()
        if category_orm:
            category_orm.name = entity.name
            if entity.description:
                category_orm.description = entity.description
            self.session.flush()
            return CategoryMapper.to_domain(category_orm)
        return None

    def delete(self, id: int) -> bool:
        category_orm = self.get_by_id(id)
        if category_orm:
            self.session.delete(category_orm)
            self.session.flush()
            return True
        return False

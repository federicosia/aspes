from abc import abstractmethod
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.adapters.persistence.base import Base
from app.domain.ports.repository import AbstractRepository


class SqlRepository[Domain, ORM: Base](AbstractRepository[Domain]):
    def __init__(self, session: Session, model_orm: type[ORM]) -> None:
        self._session = session
        self._model_orm = model_orm

    @abstractmethod
    def to_persistence(self, entity: Domain) -> ORM:
        pass

    @abstractmethod
    def to_domain(self, entity: ORM) -> Domain:
        pass

    def get_by_id(self, id: int) -> Optional[Domain]:
        result = self._session.execute(
            select(self._model_orm).where(self._model_orm.id == id)
        ).scalar_one_or_none()
        return self.to_domain(result) if result is not None else None

    def list(self, **filters) -> List[Domain]:
        persistence_entities = (
            self._session.execute(select(self._model_orm).filter_by(**filters))
            .scalars()
            .all()
        )
        return [self.to_domain(pe) for pe in persistence_entities]

    def add(self, entity: Domain) -> Domain:
        orm = self.to_persistence(entity)
        self._session.add(orm)
        self._session.flush()
        return self.to_domain(orm)

    def update(self, entity: Domain) -> Domain:
        orm = self.to_persistence(entity)
        orm = self._session.merge(orm)
        self._session.flush()
        self._session.refresh(orm)
        return self.to_domain(orm)

    def delete(self, id: int) -> bool:
        record = self._session.execute(
            select(self._model_orm).where(self._model_orm.id == id)
        ).scalar_one_or_none()
        if record is not None:
            self._session.delete(record)
            self._session.flush()
            return True
        return False

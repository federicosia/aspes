from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import Select, select
from sqlalchemy.orm import Session
from sqlalchemy.sql import and_

from app.adapters.persistence.base import Base
from app.domain.ports.repository import AbstractRepository


class SqlRepository[Domain, ORM: Base](AbstractRepository[Domain], ABC):
    def __init__(self, session: Session, model_orm: type[ORM]) -> None:
        self._session = session
        self._model_orm = model_orm

    @abstractmethod
    def to_persistence(self, entity: Domain) -> ORM:
        pass

    @abstractmethod
    def to_domain(self, entity: ORM) -> Domain:
        pass

    def _get_stmnt(self, id: int) -> Select[tuple[ORM]]:
        return select(self._model_orm).where(self._model_orm.id == id)

    def get_by_id(self, id: int) -> Optional[Domain]:
        result = self._session.execute(self._get_stmnt(id)).scalar_one_or_none()
        if result:
            return self.to_domain(result)
        return None

    def _construct_list_stmnt(self, **filters) -> Select[tuple[ORM]]:
        stmnt = select(self._model_orm)
        where_clauses = []
        for k, v in filters.items():
            if not hasattr(self._model_orm, k):
                raise ValueError(f"Invalid column type {k}")
            where_clauses.append(getattr(self._model_orm, k) == v)
        if len(where_clauses) == 1:
            stmnt = stmnt.where(where_clauses[0])
        elif len(where_clauses) > 1:
            stmnt = stmnt.where(and_(*where_clauses))
        return stmnt

    def list(self, **filters) -> List[Domain]:
        persitence_entities = list(
            (
                self._session.execute(self._construct_list_stmnt(**filters))
                .scalars()
                .all()
            )
        )
        domain_entities = []
        for pe in persitence_entities:
            domain_entities.append(self.to_domain(pe))
        return domain_entities

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
        record = self._session.execute(self._get_stmnt(id)).scalar_one_or_none()
        if record is not None:
            self._session.delete(record)
            self._session.flush()
            return True
        return False

from sqlalchemy.orm import Session

from app.adapters.persistence.user import UserORM
from app.adapters.repositories.sql.sql_repository import SqlRepository
from app.domain.models.user import User


class UserRepository(SqlRepository[User, UserORM]):
    def __init__(self, session: Session, model_orm: type[UserORM] = UserORM):
        super().__init__(session, model_orm)

    def to_domain(self, entity: UserORM) -> User:
        return User(
            id=entity.id,
            name=entity.name,
            surname=entity.surname,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            role=entity.role,
            status=entity.status,
        )

    def to_persistence(self, entity: User) -> UserORM:
        return UserORM(
            id=entity.id,
            name=entity.name,
            surname=entity.surname,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            role=entity.role,
            status=entity.status,
        )

    def get_by_username(self, username: str) -> User | None:
        user_orm = self._session.query(UserORM).filter_by(username=username).first()
        return self.to_domain(user_orm) if user_orm else None

    def get_by_email(self, email: str) -> User | None:
        user_orm = self._session.query(UserORM).filter_by(email=email).first()
        return self.to_domain(user_orm) if user_orm else None

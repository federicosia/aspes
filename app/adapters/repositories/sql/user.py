import logging

from sqlalchemy.orm import Session

from app.adapters.persistence.user import UserORM
from app.adapters.repositories.sql.sql_repository import SqlRepository
from app.domain.models.user import User

logger = logging.getLogger(__name__)


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

    def get_by_username_and_email(self, username: str, email: str) -> User | None:
        user_orm = (
            self._session.query(UserORM)
            .filter_by(username=username, email=email)
            .first()
        )
        if user_orm:
            return self.to_domain(user_orm)
        return None

    def get_by_username(self, username: str) -> User | None:
        user_orm = self._session.query(UserORM).filter_by(username=username).first()
        if user_orm:
            return self.to_domain(user_orm)
        return None

    def create(
        self,
        name: str,
        surname: str,
        username: str,
        email: str,
        password: str,
        role: str,
    ) -> bool:
        user = self.get_by_username_and_email(username, email)
        if not user:
            user_orm = UserORM(
                name=name,
                surname=surname,
                username=username,
                email=email,
                password=password,
                role=role,
                status="ENABLED",
            )
            self._session.add(user_orm)
            return True
        return False

    def get_by_credentials(self, username: str, password: str) -> User | None:
        logger.info(
            f"Fetching user by credentials: {username} with provided password: {password}"
        )
        user_orm = (
            self._session.query(UserORM)
            .filter_by(username=username, password=password)
            .first()
        )
        if user_orm:
            return self.to_domain(user_orm)
        return None

    def change_status(self, entity: User) -> User | None:
        user_orm = self._session.query(UserORM).filter_by(id=entity.id).first()
        if user_orm:
            user_orm.status = entity.status
            self._session.flush()
            return self.to_domain(user_orm)
        return None

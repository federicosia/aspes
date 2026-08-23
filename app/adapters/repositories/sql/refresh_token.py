from datetime import datetime, timedelta, timezone

from app.adapters.persistence.refresh_token import RefreshTokenORM
from app.adapters.repositories.sql.sql_repository import SqlRepository
from app.domain.models.family import Family
from app.domain.models.refresh_token import RefreshToken


class RefreshTokenRepository(SqlRepository[RefreshToken, RefreshTokenORM]):
    def __init__(self, session, model_orm: type[RefreshTokenORM] = RefreshTokenORM):
        self.session = session
        self.model_orm = model_orm

    def to_persistence(self, entity: RefreshToken) -> RefreshTokenORM:
        return RefreshTokenORM(
            id=entity.id,
            token=entity.token,
            user_id=entity.user_id,
            expires_at=entity.expires_at,
            family=entity.family,
        )

    def to_domain(self, entity: RefreshTokenORM) -> RefreshToken:
        return RefreshToken(
            id=entity.id,
            token=entity.token,
            user_id=entity.user_id,
            expires_at=entity.expires_at,
            family=entity.family,
        )

    def create(self, user_id: int, token: str) -> None:
        refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=datetime.now(tz=timezone.utc) + timedelta(days=7),
            family=Family.DESKTOP,
        )
        self.session.add(self.to_persistence(refresh_token))

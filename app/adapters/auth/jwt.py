from datetime import datetime, timedelta

import jwt

from app.config.settings import settings
from app.domain.exceptions.domain import DomainException
from app.domain.ports.token import TokenService
from app.domain.vobjects.token import TokenData


class JwtTokenService(TokenService):
    @staticmethod
    def create_access_token(data: TokenData) -> str:
        data.expire = str(
            datetime.now() + timedelta(minutes=settings.jwt_expire_minutes)
        )
        return jwt.encode(
            data.to_dict(), settings.private_key, algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def verify_token(token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, settings.private_key, algorithms=settings.jwt_algorithm
            )
            return TokenData(**payload)
        except jwt.ExpiredSignatureError:
            raise DomainException("Token expired")
        except jwt.InvalidTokenError:
            raise DomainException("Invalid token")

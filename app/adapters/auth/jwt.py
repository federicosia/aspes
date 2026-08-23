from datetime import datetime, timedelta, timezone
from typing import Annotated
import logging
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError
from app.config.settings import settings
from app.domain.ports.token import TokenService
from app.domain.vobjects.token import AccessTokenData, RefreshTokenData, TokenType

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger(__name__)


class JwtTokenService(TokenService):
    @staticmethod
    def create_access_token(data: AccessTokenData) -> str:
        data.exp = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.jwt_expire_minutes
        )
        logger.debug(f"Creating JWT token with data: {data}")
        return jwt.encode(
            data.to_dict(),
            settings.private_key.encode("utf-8"),
            algorithm=settings.jwt_algorithm,
        )

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        data = RefreshTokenData(
            user_id=user_id,
            type=TokenType.REFRESH,
            exp=datetime.now(tz=timezone.utc) + timedelta(days=7),
        )
        logger.debug(f"Creating JWT refresh token with data: {data}")
        return jwt.encode(
            data.to_dict(),
            settings.private_key.encode("utf-8"),
            algorithm=settings.jwt_algorithm,
        )

    @staticmethod
    def verify_access_token(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> AccessTokenData:
        try:
            payload = jwt.decode(
                token,
                settings.public_key.encode("utf-8"),
                algorithms=[settings.jwt_algorithm],
            )
            logger.debug(f"Verifying JWT token with payload: {payload}")
            return AccessTokenData(**payload)
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token expired")
        except InvalidSignatureError:
            raise InvalidSignatureError("Invalid token signature")
        except InvalidTokenError:
            raise InvalidTokenError("Invalid token")

    @staticmethod
    def verify_refresh_token(token: str) -> RefreshTokenData:
        try:
            payload = jwt.decode(
                token,
                settings.public_key.encode("utf-8"),
                algorithms=[settings.jwt_algorithm],
            )
            logger.debug(f"Verifying JWT refresh token with payload: {payload}")
            return RefreshTokenData(**payload)
        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token expired")
        except InvalidSignatureError:
            raise InvalidSignatureError("Invalid token signature")
        except InvalidTokenError:
            raise InvalidTokenError("Invalid token")

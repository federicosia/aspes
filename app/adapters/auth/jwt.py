from datetime import datetime, timedelta
from typing import Annotated
import logging
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.config.settings import settings
from app.domain.exceptions.domain import DomainException
from app.domain.ports.token import TokenService
from app.domain.vobjects.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

logger = logging.getLogger(__name__)


class JwtTokenService(TokenService):
    @staticmethod
    def create_access_token(data: TokenData) -> str:
        data.exp = datetime.now() + timedelta(minutes=settings.jwt_expire_minutes)
        logger.debug(f"Creating JWT token with data: {data}")
        return jwt.encode(
            data.to_dict(), settings.private_key, algorithm=settings.jwt_algorithm
        )

    @staticmethod
    def verify_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
        try:
            payload = jwt.decode(
                token, settings.private_key, algorithms=[settings.jwt_algorithm]
            )
            logger.debug(f"Verifying JWT token with payload: {payload}")
            return TokenData(**payload)
        except jwt.ExpiredSignatureError:
            raise DomainException("Token expired")
        except jwt.InvalidSignatureError:
            raise DomainException("Invalid token signature")
        except jwt.InvalidTokenError:
            raise DomainException("Invalid token")

from app.domain.models.status import Status
from app.domain.models.user import User
from app.domain.ports.uow import AbstractUserUnitOfWork
from pwdlib import PasswordHash
import logging

from app.domain.vobjects.token import RefreshTokenData, TokenType

password_hash = PasswordHash.recommended()
logger = logging.getLogger(__name__)


def create_user(
    uow: AbstractUserUnitOfWork,
    name: str,
    surname: str,
    username: str,
    email: str,
    password: str,
    role: str,
) -> bool:
    with uow:
        result = uow.users.create(
            name=name,
            surname=surname,
            username=username,
            email=email,
            password=password_hash.hash(password),
            role=role,
        )
        return result


def authenticate_user(
    uow: AbstractUserUnitOfWork, username: str, password: str
) -> User | None:
    logger.info(f"Authenticating user: {username} with provided password: {password}")
    with uow:
        user_in_db = uow.users.get_by_username(
            username=username,
        )
        if user_in_db and password_hash.verify(password, user_in_db.password):
            logger.info(f"User {username} authenticated successfully")
            return user_in_db
        else:
            logger.warning(f"Failed to authenticate user: {username}")
            return None


def check_access_token(
    uow: AbstractUserUnitOfWork, decoded_token: RefreshTokenData
) -> User | None:
    if decoded_token and decoded_token.type == TokenType.REFRESH:
        user = uow.users.get_by_id(decoded_token.user_id)
        if user and user.status == Status.DISABLED:
            return user


def store_refresh_token(uow: AbstractUserUnitOfWork, user_id: int, token: str) -> None:
    with uow:
        uow.refresh_tokens.create(user_id=user_id, token=token)

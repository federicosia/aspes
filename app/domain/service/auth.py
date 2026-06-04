from app.domain.models.user import User
from app.domain.ports.uow import AbstractUserUnitOfWork
from pwdlib import PasswordHash
import logging

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

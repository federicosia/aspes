from app.domain.models.user import User
from app.domain.ports.uow import AbstractUserUnitOfWork
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


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
    with uow:
        return uow.users.get_by_credentials(
            username=username,
            password=password_hash.hash(password),
        )

from app.domain.exceptions.user import UserAlreadyExistsException, UserNotFoundException
from app.domain.models.role import Role
from app.domain.models.user import User
from app.domain.ports.uow import AbstractUserUnitOfWork
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def register(
    uow: AbstractUserUnitOfWork,
    name: str,
    surname: str,
    username: str,
    email: str,
    password: str,
    role: Role,
) -> User:
    with uow:
        if uow.users.get_by_username(username) is not None:
            raise UserAlreadyExistsException(field="username", value=username)
        if uow.users.get_by_email(email) is not None:
            raise UserAlreadyExistsException(field="email", value=email)
        user = User(
            name=name,
            surname=surname,
            username=username,
            email=email,
            password=password_hash.hash(password),
            role=role,
        )
        uow.users.add(user)
        uow.commit()
        return user


def enable(uow: AbstractUserUnitOfWork, user_id: int) -> User | None:
    with uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id=user_id)
        user.enable()
        uow.users.update(user)
        uow.commit()
        return user


def disable(uow: AbstractUserUnitOfWork, user_id: int) -> User | None:
    with uow:
        user = uow.users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(user_id=user_id)
        user.disable()
        uow.users.update(user)
        uow.commit()
        return user

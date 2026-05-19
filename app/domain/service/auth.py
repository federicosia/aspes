from app.domain.models.user import User
from app.domain.ports.uow import AbstractUserUnitOfWork


def authenticate_user(
    uow: AbstractUserUnitOfWork, username: str, password: str
) -> User | None:
    with uow:
        return uow.users.get_by_credentials(username=username, password=password)

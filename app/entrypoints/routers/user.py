import logging

from fastapi import APIRouter, Depends

from app.domain.ports.uow import AbstractUserUnitOfWork
from app.entrypoints.dependencies import get_auth_uow
from app.entrypoints.schemas.auth import CreateUserRequest, CreateUserResponse
from app.domain.service.user import register

router = APIRouter(prefix="/user")
logger = logging.getLogger(__name__)


@router.post("/register")
def register_user(
    body: CreateUserRequest,
    uow: AbstractUserUnitOfWork = Depends(get_auth_uow),
):
    result = register(
        uow,
        body.name,
        body.surname,
        body.username,
        body.email,
        body.password,
        body.role,
    )
    return CreateUserResponse(success=True if result else False)

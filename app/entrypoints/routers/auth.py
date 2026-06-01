from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.adapters.auth.jwt import JwtTokenService
from app.config.settings import settings
from app.domain.models.status import Status
from app.domain.ports.uow import AbstractUserUnitOfWork
from app.domain.service.auth import authenticate_user, create_user
from app.domain.vobjects.token import TokenData
from app.entrypoints.dependencies import get_auth_uow
from app.entrypoints.schemas.auth import CreateUserRequest, CreateUserResponse

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(
    body: CreateUserRequest,
    uow: AbstractUserUnitOfWork = Depends(get_auth_uow),
):
    result = create_user(
        uow,
        body.name,
        body.surname,
        body.username,
        body.email,
        body.password,
        body.role,
    )
    return CreateUserResponse(success=result)


@router.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: AbstractUserUnitOfWork = Depends(get_auth_uow),
):
    user = authenticate_user(uow, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return JwtTokenService.create_access_token(
        TokenData(
            user_id=user.id,
            disabled=user.status == Status.DISABLED,
            role=user.role,
            username=form_data.username,
            exp=(
                datetime.now(tz=timezone.utc)
                + timedelta(minutes=settings.jwt_expire_minutes)
            ),
        )
    )

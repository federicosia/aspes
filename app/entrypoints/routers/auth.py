from datetime import datetime, timedelta
import logging
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.adapters.auth.jwt import JwtTokenService
from app.domain.models.status import Status
from app.domain.ports.uow import AbstractUserUnitOfWork
from app.domain.service.auth import (
    authenticate_user,
    check_access_token,
    store_refresh_token,
)
from app.domain.vobjects.token import AccessTokenData, TokenType
from app.entrypoints.dependencies import get_auth_uow
from app.entrypoints.schemas.auth import (
    LoginResponse,
)

router = APIRouter(prefix="/auth")
logger = logging.getLogger(__name__)


@router.get("/token", response_model=LoginResponse)
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: AbstractUserUnitOfWork = Depends(get_auth_uow),
) -> LoginResponse:
    logger.info(f"Login attempt for user: {form_data.username}")
    user = authenticate_user(uow, form_data.username, form_data.password)
    if user is None or user.id is None:
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = JwtTokenService.create_access_token(
        AccessTokenData(
            user_id=user.id,
            disabled=user.status == Status.DISABLED,
            role=user.role,
            type=TokenType.ACCESS,
            username=form_data.username,
            exp=datetime.now() + timedelta(minutes=15),
        )
    )
    refresh_token = JwtTokenService.create_refresh_token(user_id=user.id)
    store_refresh_token(uow, user.id, refresh_token)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/refresh", response_model=LoginResponse)
async def refresh(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
    uow: AbstractUserUnitOfWork = Depends(get_auth_uow),
) -> LoginResponse:
    if not refresh_token:
        logger.warning("Refresh token not provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not provided",
        )
    decoded_token = JwtTokenService.verify_refresh_token(refresh_token)
    if user := check_access_token(uow, decoded_token):
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7 * 24 * 3600,
        )
        return LoginResponse(
            access_token=JwtTokenService.create_access_token(
                AccessTokenData(
                    user_id=decoded_token.user_id,
                    disabled=user.status == Status.DISABLED,
                    role=user.role,
                    type=TokenType.ACCESS,
                    username=user.username,
                    exp=datetime.now() + timedelta(minutes=15),
                )
            ),
            token_type="bearer",
        )
    else:
        logger.warning("Invalid refresh token")
        response.delete_cookie(key="refresh_token", httponly=True, secure=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token provided",
        )

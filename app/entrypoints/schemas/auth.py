from pydantic import BaseModel

from app.domain.models.role import Role


class CreateUserRequest(BaseModel):
    name: str
    surname: str
    username: str
    email: str
    password: str
    role: Role


class CreateUserResponse(BaseModel):
    success: bool


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

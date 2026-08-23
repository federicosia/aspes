from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    surname: str
    username: str
    email: str
    password: str
    role: str


class CreateUserResponse(BaseModel):
    success: bool


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

from abc import ABC, abstractmethod

from app.domain.vobjects.token import AccessTokenData


class TokenService(ABC):
    @staticmethod
    @abstractmethod
    def create_access_token(data: AccessTokenData) -> str: ...

    @staticmethod
    @abstractmethod
    def verify_access_token(token: str) -> AccessTokenData: ...

from abc import ABC, abstractmethod

from app.domain.vobjects.token import TokenData


class TokenService(ABC):
    @staticmethod
    @abstractmethod
    def create_access_token(data: TokenData) -> str: ...

    @staticmethod
    @abstractmethod
    def verify_token(token: str) -> TokenData: ...

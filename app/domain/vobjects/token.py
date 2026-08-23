from dataclasses import asdict, dataclass
from datetime import datetime
from enum import StrEnum


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


@dataclass
class AccessTokenData:
    user_id: int
    username: str
    role: str
    type: TokenType
    disabled: bool
    exp: datetime | None = None

    def to_dict(self):
        return asdict(self)


@dataclass
class RefreshTokenData:
    user_id: int
    type: TokenType
    exp: datetime | None = None

    def to_dict(self):
        return asdict(self)

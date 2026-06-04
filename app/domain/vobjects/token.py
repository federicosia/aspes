from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass(frozen=True)
class Token:
    access_token: str
    token_type: str


@dataclass
class TokenData:
    user_id: int
    username: str
    role: str
    disabled: bool
    exp: datetime | None = None

    def to_dict(self):
        return asdict(self)

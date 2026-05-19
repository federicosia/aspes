from dataclasses import asdict, dataclass


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
    expire: str

    def to_dict(self):
        return asdict(self)

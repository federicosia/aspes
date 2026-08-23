from dataclasses import dataclass
from datetime import datetime

from app.domain.models.family import Family


@dataclass
class RefreshToken:
    token: str
    user_id: int
    expires_at: datetime
    family: Family
    id: int | None = None

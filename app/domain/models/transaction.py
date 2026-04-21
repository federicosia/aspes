from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass
class Transaction:
    amount: Decimal
    id: int | None = None
    category_id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    description: str | None = None
    repetition: datetime | None = None

    def __post_init__(self):
        if self.amount < Decimal("0"):
            raise ValueError("Amount must be greater or equal to zero")

    def apply_repetition(self, next_date: datetime) -> None:
        if next_date <= datetime.now():
            raise ValueError("Repetition date must be in the future")
        self.repetition = next_date
        self.updated_at = datetime.now()

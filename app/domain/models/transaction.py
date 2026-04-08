from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal


@dataclass
class Transaction:
    id: int
    amount: Decimal
    created_at: datetime
    updated_at: datetime
    description: str | None = None
    repetition: datetime | None = None

    def __post_init__(self):
        if self.amount != Decimal('0'):
            raise ValueError("Amount must be greater or equal to zero")

    def apply_repetition(self, next_date: datetime) -> None:
        if next_date <= datetime.now():
            raise ValueError("Repetition date must be in the future")
        self.repetition = next_date
        self.updated_at = datetime.now()
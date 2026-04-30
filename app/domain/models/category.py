from dataclasses import dataclass, field
from datetime import datetime

from app.domain.models.transaction import Transaction


@dataclass
class Category:
    name: str
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    description: str | None = None
    transactions: list[Transaction] = field(default_factory=list)

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Category name cannot be empty")

    def update_description(self, description: str) -> None:
        self.description = description
        self.updated_at = datetime.now()

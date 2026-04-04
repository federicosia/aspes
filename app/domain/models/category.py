from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Category:
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Category name cannot be empty")

    def update_description(self, description: str) -> None:
        self.description = description
        self.updated_at = datetime.now()
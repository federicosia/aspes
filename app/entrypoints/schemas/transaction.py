from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class CreateTransactionRequest(BaseModel):
    amount: Decimal
    description: str | None
    repetition: datetime | None
    category_id: int


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    description: str | None = None
    category_id: int

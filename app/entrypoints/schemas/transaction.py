from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.domain.models.repetition import Repetition


class CreateTransactionRequest(BaseModel):
    amount: Decimal
    description: str | None
    repetition: Repetition | None
    category_id: int


class TransactionResponse(BaseModel):
    id: int
    amount: Decimal
    description: str | None = None
    repetition: Repetition | None = None
    category_id: int

    model_config = ConfigDict(from_attributes=True)


class TransactionsListResponse(BaseModel):
    transactions: list[TransactionResponse]

    model_config = ConfigDict(from_attributes=True)

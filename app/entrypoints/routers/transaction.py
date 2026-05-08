from fastapi import APIRouter, Depends, HTTPException, status

from app.domain.ports.uow import AbstractUnitOfWork
from app.domain.service import transaction as transaction_service
from app.entrypoints.dependencies import get_uow
from app.entrypoints.schemas.transaction import (
    CreateTransactionRequest,
    TransactionResponse,
    TransactionsListResponse,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, uow: AbstractUnitOfWork = Depends(get_uow)):
    transaction = transaction_service.get_transaction(uow, id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return TransactionResponse.model_validate(transaction)


@router.post(
    "", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED
)
def create_transaction(
    body: CreateTransactionRequest, uow: AbstractUnitOfWork = Depends(get_uow)
):
    transaction = transaction_service.create_transaction(
        uow,
        amount=body.amount,
        repetition=body.repetition,
        description=body.description,
        category_id=body.category_id,
    )
    return TransactionResponse.model_validate(transaction)


@router.get(
    "/list/{category_id}",
    response_model=TransactionsListResponse,
    status_code=status.HTTP_200_OK,
)
def list_transactions_by_category(
    category_id: int, uow: AbstractUnitOfWork = Depends(get_uow)
):
    transactions = transaction_service.get_list_transactions_by_category_id(
        uow, category_id
    )
    return TransactionsListResponse(
        transactions=[
            TransactionResponse.model_validate(transaction)
            for transaction in transactions
        ]
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, uow: AbstractUnitOfWork = Depends(get_uow)):
    transaction_service.delete_transaction(uow, id=transaction_id)

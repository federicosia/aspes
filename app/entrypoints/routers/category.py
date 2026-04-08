# entrypoints/routers/category.py
from fastapi import APIRouter, Depends, HTTPException, status
from domain.service import category as category_service
from domain.ports.uow import AbstractUnitOfWork
from entrypoints.schemas.category import CreateCategoryRequest, CategoryResponse
from entrypoints.dependencies import get_uow

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    category = category_service.get_category(uow, id=category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return CategoryResponse.model_validate(category)

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    body: CreateCategoryRequest,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    category = category_service.create_category(uow, name=body.name)
    return CategoryResponse.model_validate(category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    uow: AbstractUnitOfWork = Depends(get_uow),
):
    category_service.delete_category(uow, id=category_id)
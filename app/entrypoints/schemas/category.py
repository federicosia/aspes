from pydantic import BaseModel, ConfigDict


class CreateCategoryRequest(BaseModel):
    name: str
    description: str | None


class CategoryResponse(BaseModel):
    id: int | None
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)

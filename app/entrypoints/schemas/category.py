from pydantic import BaseModel

class CreateCategoryRequest(BaseModel):
    name: str
    description: str | None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
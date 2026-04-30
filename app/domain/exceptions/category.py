class CategoryNotFound(Exception):
    def __init__(self, category_id: int):
        super().__init__(f"Category with id {category_id} not found")


class DuplicateCategoryName(Exception):
    def __init__(self, name: str):
        super().__init__(f"Category with name '{name}' already exists")

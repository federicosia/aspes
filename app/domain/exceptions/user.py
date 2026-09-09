class UserAlreadyExistsException(Exception):
    def __init__(self, field: str, value: str):
        super().__init__(f"User with {field} '{value}' already exists")


class UserNotFoundException(Exception):
    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found")

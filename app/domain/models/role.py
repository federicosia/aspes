from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    LOGGED = "logged"
    GUEST = "guest"

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/listit"

    app_name: str = "listit"
    debug: bool = False
    environment: str = "dev"

settings = Settings()
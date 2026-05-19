from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str | None = None
    private_key: str | None = None
    public_key: str | None = None
    app_name: str | None = None
    debug: bool | None = None
    environment: str | None = None
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: float = 15


settings = Settings()

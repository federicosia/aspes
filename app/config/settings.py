from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    private_key: str
    public_key: str
    app_name: str = "Aspes"
    debug: bool = False
    environment: str = "dev"
    jwt_algorithm: str = "RS256"
    jwt_expire_minutes: float = 15


try:
    settings = Settings()  # type: ignore
except Exception as e:
    print(e)
    raise e

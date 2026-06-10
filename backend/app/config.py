from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    LINK_TTL_DAYS: int = 2


settings = Settings()

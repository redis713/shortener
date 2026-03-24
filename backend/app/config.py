from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str

    # на будущее
    LINK_TTL_DAYS: int = 2

    class Config:
        env_file = ".env"


settings = Settings()

import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    LOG_LEVEL: int = logging.INFO

    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_HOST: str = "localhost"
    DB_NAME: str = "aps"

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"

    class Config:
        case_insensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        extra = 'ignore'

def load_config():
    if os.environ.get("DOCKER_ENV") == "true":
        load_dotenv(".env.docker")
    else:
        load_dotenv(".env.local")

    return Settings()

settings = load_config()

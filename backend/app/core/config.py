from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

target_env = '.env.local'

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str

    @property
    def DATABASE_URL_asyncpg(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = target_env
        extra = 'ignore'

def load_config():
    global target_env
    if os.environ.get("DOCKER_ENV") == "true":
        target_env = '.env.docker'

    load_dotenv(target_env)
    
    return Settings()

settings = load_config()

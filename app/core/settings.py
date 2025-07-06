import os
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    #database configuration
    DB_URL:str = os.getenv("DB_URL")

settings = Settings()
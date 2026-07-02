import os 
from pydantic_settings import BaseSettings,SettingsConfigDict
from functools import lru_cache



class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    VERSION: str = "0.1.0"
    DATABASE_HOST: str
    DATABASE_PORT: int 
    DATABASE_NAME: str
    DATABASE_USER: str 
    DATABASE_PASSWORD: str
    ENVIRONMENT: str = "development"
    AWS_BUCKET_NAME: str
    AWS_DEFAULT_FOLDER: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    S3_RAW_ROOT_FOLDER: str
    S3_PROCESSED_ROOT_FOLDER: str
    LLAMA_CLOUD_API_KEY: str
    GLINER2_MODEL: str
    GLINER2_MODEL_THRESHOLD: float


# @lru_cache()
def get_config():
    try:
        settings = Config()
        os.environ["AWS_ACCESS_KEY_ID"] = settings.AWS_ACCESS_KEY_ID
        os.environ["AWS_SECRET_ACCESS_KEY"] = settings.AWS_SECRET_ACCESS_KEY
        os.environ["AWS_REGION"] = settings.AWS_REGION
        return settings
    except Exception as e:
        raise Exception(f"Error loading settings: {e}")
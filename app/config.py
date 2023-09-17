from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    DB_HOSTNAME: str 
    DB_PORT: str 
    DB_PASSWORD: str 
    DB_NAME:str 
    DB_USERNAME: str 

    SECRET_KEY:str
    ALGO:str
    ACCESS_TOKEN_EXPIRE:int 

    model_config = SettingsConfigDict(env_file="../.env")
    
settings = Settings()
from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    TOKEN_WEATHER: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

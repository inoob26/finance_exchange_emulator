from pydantic import BaseSettings


class Settings(BaseSettings):
    LOGLEVEL: str = "INFO"
    TICKERS_COUNT: int = 100

    # DB
    DB_HOST: str = "localhost"
    DB_PORT: int = 27017
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str = "mydb"
    DB_COLLECTION: str = "tickers"


settings = Settings()

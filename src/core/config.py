import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "FastAPI Starter"
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app_db")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_SIGNING_ALGORITHM = os.getenv("JWT_SIGNING_ALGORITHM")
    JWT_EXPIRATION_MINUTES = int(os.getenv("JWT_EXPIRATION_MINUTES"))

    STEAM_API_KEY = os.getenv("STEAM_API_KEY")

    MAIL_USERNAME=os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
    MAIL_FROM=os.getenv("MAIL_FROM")
    MAIL_SERVER=os.getenv("MAIL_SERVER")

settings = Settings()

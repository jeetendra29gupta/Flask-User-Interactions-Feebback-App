import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration with default settings."""

    APP_ENV: str = os.getenv("APP_ENV")
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    SECRET_KEY: str = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    HOST: str = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT"))

    LOG_DIR: Path = BASE_DIR / os.getenv("LOG_DIR")
    LOG_FILE: Path = LOG_DIR / os.getenv("LOG_FILE")
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = (
        "%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s"
    )
    MAX_BYTES: int = 1_000_000
    BACKUP_COUNT: int = 5

    DEBUG: bool = False
    TESTING: bool = False

    @classmethod
    def pre_check(cls):
        """
        Pre-check routine to create necessary directories if they don't exist.
        This should be called before app initialization.
        """
        # Create log directory
        if not cls.LOG_DIR.exists():
            cls.LOG_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.WARNING


class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}

current_config = config.get(Config.APP_ENV, Config)

# Run pre_check early in app lifecycle
current_config.pre_check()

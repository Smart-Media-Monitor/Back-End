import os
from pathlib import Path
import json

DB_USER = "hassan"
DB_PASSWORD = "mhp78692"
DB_HOST = "localhost"
DB_NAME = "smart_media_monitor"

DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"


# Global configuration
GLOBAL_CONFIG = {"VERSION": 0.1, "db_uri": DB_URI}


# Environment specific config, or overwrite of GLOBAL_CONFIG
ENV_CONFIG = {
    "development": {"DEBUG": True},
    "staging": {"DEBUG": True},
    "production": {"DEBUG": False},
}

env_path = Path(".") / ".env"


class Settings:
    """
    Configuration settings for the application.
    """

    PROJECT_NAME: str = "Smart Media Monior"
    PROJECT_VERSION: str = "0.0.1"

    # JWT settings
    SECRET_KEY: str = "f2faa57612263037040e91cb038d49673178d407c6371883490b9c98d1b377b3"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30  # in minutes


settings = Settings()


def get_config() -> dict:
    """
    Get configuration based on the execution environment.

    Returns:
        dict: Configuration dictionary.
    """
    # Determine the running environment
    ENV = os.environ["EXEC_ENV"] if "EXEC_ENV" in os.environ else "development"
    ENV = ENV or "development"

    # Raise an error if the environment is not expected
    if ENV not in ENV_CONFIG:
        raise EnvironmentError(f"Config for environment {ENV} not found")

    config = GLOBAL_CONFIG.copy()
    config.update(ENV_CONFIG[ENV])

    config["ENV"] = ENV

    return config


# Load config for import
CONFIG = get_config()

if __name__ == "__main__":
    # For debugging
    print(json.dumps(CONFIG, indent=4))

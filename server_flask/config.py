"""Configuration."""

import secrets
from configparser import ConfigParser
from pathlib import Path

setting = ConfigParser()
settings_ini = Path(__file__).parent.resolve().joinpath("settings.ini")
setting.read(settings_ini, encoding="utf-8")


class Config:
    """Configuration."""

    AUTH = setting.getboolean("Options", "login")
    BASE_PATH = setting.get("Options", "path")
    DATABASE_URI = Path(BASE_PATH, "database.db")
    ACCESS_SECRET_KEY = secrets.token_hex()
    REFRESH_SECRET_KEY = secrets.token_hex()
    ACCESS_SECRET_KEY_LIVE = 15
    REFRESH_SECRET_KEY_LIVE = 60 * 30 * 365

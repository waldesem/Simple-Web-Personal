"""Configuration."""

import secrets
from configparser import ConfigParser
from pathlib import Path

setting = ConfigParser()
setting.read(Path(__file__).parent.resolve().joinpath("settings.ini"), encoding="utf-8")


class Config:
    """Configuration class."""

    SECRET_KEY = secrets.token_hex(16)
    BASE_PATH = Path(setting["Destination"].get("path"))
    DATABASE_URI = BASE_PATH.joinpath("database.db")

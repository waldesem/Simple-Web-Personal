"""Configuration."""

import secrets
from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
current_dir = Path(__file__).parent.resolve()
ini = current_dir.joinpath("settings.ini")

if ini.is_file():
    config.read(ini, encoding="utf-8")
else:
    config["Options"] = {}
    config["Options"]["login"] = "false"
    config["Options"]["path"] = str(current_dir)
    config["Options"]["password"] = "88888888"  # noqa: S105
    with ini.open("w") as configfile:
        config.write(configfile)


class Config:
    """Configuration."""

    AUTH = config.getboolean("Options", "login")
    BASE_PATH = config.get("Options", "path")
    DEFAULT_PASSWORD = config.get("Options", "password")
    DATABASE_URI = Path(BASE_PATH, "database.db")
    ACCESS_SECRET_KEY = secrets.token_hex()
    REFRESH_SECRET_KEY = secrets.token_hex()
    ACCESS_SECRET_KEY_LIVE = 15
    REFRESH_SECRET_KEY_LIVE = 60 * 30 * 365

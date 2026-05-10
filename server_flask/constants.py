"""Configuration."""

from configparser import ConfigParser
from pathlib import Path

setting = ConfigParser()
settings_ini = Path(__file__).parent.resolve().joinpath("settings.ini")
setting.read(settings_ini, encoding="utf-8")

BASE_PATH = setting.get("Destination", "path")
DATABASE_URI = Path(BASE_PATH, "database.db")

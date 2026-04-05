"""Configuration."""

from configparser import ConfigParser
from pathlib import Path

setting = ConfigParser()
setting.read(Path(__file__).parent.resolve().joinpath("settings.ini"), encoding="utf-8")

BASE_PATH = (
    Path(path)
    if (path := setting.get("Destination", "path"))
    else Path(
        __file__,
    )
    .parent.resolve()
    .joinpath("Persons")
)
DATABASE_URI = BASE_PATH.joinpath("database.db")

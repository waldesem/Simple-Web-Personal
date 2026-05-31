"""Data classes."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Actions(Enum):
    """Actions."""

    delete = "delete"
    block = "block"
    reset = "reset"


class Roles(Enum):
    """Roles."""

    admin = "admin"
    api = "api"
    user = "user"
    guest = "guest"


class Conclusions(Enum):
    """Conclusions."""

    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    cancel = "СНЯТ С ПРОВЕРКИ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"


class Decisions(Enum):
    """Decisions."""

    agreed = "БЕЗ ЗАМЕЧАНИЙ"
    comments = "С КОММЕНТАРИЯМИ"
    cancel = "ОТКАЗ ОТ ПРОВЕРКИ"
    denied = "НЕГАТИВ"


@dataclass
class User:
    """User."""

    id: int
    fullname: str
    username: str
    email: str
    role: Roles
    created: datetime
    passhash: str
    pswd_create: str
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int

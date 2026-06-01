"""Data classes."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Roles(Enum):
    """Roles."""

    admin = "admin"
    api = "api"
    user = "user"
    guest = "guest"


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
    pswd_create: datetime
    change_pswd: bool
    blocked: bool
    deleted: bool
    attempt: int

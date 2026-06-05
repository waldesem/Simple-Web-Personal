"""PyDantic models."""

from __future__ import annotations

import re
from datetime import date, datetime  # noqa: TC003
from enum import Enum
from typing import Annotated, Literal

from pydantic import BaseModel, Field, validator

from app.utilities.utils import validate_inn, validate_snils


class Roles(Enum):
    """Users roles."""

    admin = "admin"
    api = "api"
    user = "user"
    guest = "guest"


class Conclusions(Enum):
    """Checks conclusions."""

    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    cancel = "СНЯТ С ПРОВЕРКИ"


class Decisions(Enum):
    """Poligrafs decisions."""

    agreed = "БЕЗ ЗАМЕЧАНИЙ"
    comments = "С КОММЕНТАРИЯМИ"
    cancel = "ОТКАЗ ОТ ПРОВЕРКИ"
    denied = "НЕГАТИВ"


type ItemType = Literal[
    "addresses",
    "affilations",
    "checks",
    "contacts",
    "documents",
    "educations",
    "inquiries",
    "investigations",
    "previous",
    "poligrafs",
    "staffs",
    "workplaces",
]


class User(BaseModel):
    """Pydantic model for user form."""

    fullname: str
    username: Annotated[str, Field(default_factory=lambda v: v.lower())]
    email: str
    role: Annotated[Roles | None, Field(Roles.guest.value)]

    class Config:
        """Config class."""

        use_enum_values = True
        anystr_strip_whitespace = True
        max_anystr_length = 255


class Action(BaseModel):
    """Pydantic model for user action."""

    action: Literal["block", "reset", "delete"]


class Session(User):
    """Pydantic model for session."""

    id: int
    blocked: bool
    deleted: bool


class Query(BaseModel):
    """Query model."""

    search: str | None
    limit: int = 10
    page: int


class Candidates(BaseModel):
    """Pydantic model for candidates."""

    id: int
    surname: str
    firstname: str
    patronymic: str | None
    birthday: date
    created: datetime
    username: str


class Person(BaseModel):
    """Pydantic model form schema."""

    surname: Annotated[str, Field(max_length=255)]
    firstname: Annotated[str, Field(max_length=255)]
    patronymic: Annotated[str | None, Field(default=None, max_length=255)]
    birthday: date
    birthplace: Annotated[str | None, Field(None, max_length=255)]
    citizenship: Annotated[str | None, Field(default=None, max_length=255)]
    dual: Annotated[str | None, Field(default=None, max_length=255)]
    snils: str | None = None
    inn: str | None = None
    marital: Annotated[str | None, Field(default=None, max_length=255)]
    addition: str | None = None
    editable: bool = False

    class Config:
        """Config class."""

        anystr_strip_whitespace = True

    @validator("surname", "firstname", "patronymic")
    @classmethod
    def normalize_name(cls, v: str | None) -> str | None:
        """Normalize name."""
        return v.upper() if v and re.match(r"^[А-яЁёIV\-\s\.\,\'\(\)]*$", v) else None

    @validator("inn")
    @classmethod
    def check_inn(cls, inn: str | None) -> str | None:
        """Check inn."""
        return validate_inn(inn)

    @validator("snils")
    @classmethod
    def check_snils(cls, snils: str | None) -> str | None:
        """Check snils."""
        return validate_snils(snils)


class ItemModel(BaseModel):
    """Date Id Model schema."""

    class Config:
        """Config class."""

        use_enum_values = True
        anystr_strip_whitespace = True


class Prev(ItemModel):
    """Previous in schema."""

    surname: str = Field(max_length=255)
    firstname: Annotated[str | None, Field(default=None, max_length=255)]
    patronymic: Annotated[str | None, Field(default=None, max_length=255)]
    changed: Annotated[str | None, Field(default=None, max_length=4)]
    reason: str | None = None
    item: Literal["previous"]


class Education(ItemModel):
    """Education in schema."""

    view: Annotated[str | None, Field(default=None, max_length=255)]
    institution: Annotated[str, Field(max_length=255)]
    finished: Annotated[str | None, Field(default=None, max_length=4)]
    specialty: str | None = None
    item: Literal["educations"]


class Staff(ItemModel):
    """Staffs schema."""

    position: Annotated[str, Field(max_length=255)]
    department: Annotated[str | None, Field(default=None, max_length=255)]
    item: Literal["staffs"]


class Document(ItemModel):
    """Document in schema."""

    view: str | None = "Паспорт"
    series: str | None = None
    digits: Annotated[str, Field(max_length=12)]
    agency: Annotated[str | None, Field(default=None, max_length=255)]
    issue: date | None = None
    item: Literal["documents"]


class Address(ItemModel):
    """Address in schema."""

    view: Annotated[str, Field(max_length=255)]
    address: Annotated[str, Field(max_length=255)]
    item: Literal["addresses"]


class Contact(ItemModel):
    """Contacts in schema."""

    view: Annotated[str, Field(max_length=255)]
    contact: Annotated[str, Field(max_length=255)]
    item: Literal["contacts"]


class Workplace(ItemModel):
    """Workplaces in schema."""

    now_work: bool | None
    starts: date | None = None
    finished: date | None | str
    workplace: Annotated[str, Field(max_length=255)]
    address: Annotated[str | None, Field(None, max_length=255)]
    position: Annotated[str, Field(max_length=255)]
    reason: str | None = None
    item: Literal["workplaces"]


class Affilation(ItemModel):
    """Affilation in schema."""

    view: Annotated[str, Field(max_length=255)]
    organization: Annotated[str, Field(max_length=255)]
    inn: Annotated[str | None, Field(None, max_length=12)]
    activity: str | None = None
    item: Literal["affilations"]


class Check(ItemModel):
    """Check in schema."""

    workplace: str | None = None
    document: str | None = None
    inn: str | None = None
    debt: str | None = None
    bankruptcy: str | None = None
    bki: str | None = None
    courts: str | None = None
    affilation: str | None = None
    terrorist: str | None = None
    mvd: str | None = None
    internet: str | None = None
    cronos: str | None = None
    cros: str | None = None
    addition: str | None = None
    comment: str | None = None
    conclusion: Conclusions
    item: Literal["checks"]


class Poligraf(ItemModel):
    """Poligraf in schema."""

    theme: Annotated[str, Field(max_length=255)]
    results: str
    conclusion: Decisions
    item: Literal["poligrafs"]


class Investigation(ItemModel):
    """Investigations in schema."""

    theme: Annotated[str, Field(max_length=255)]
    info: str
    item: Literal["investigations"]


class Inquiry(ItemModel):
    """Inquiries in schema."""

    info: str
    initiator: Annotated[str, Field(max_length=255)]
    item: Literal["inquiries"]


ItemType = Annotated[
    Address
    | Affilation
    | Check
    | Contact
    | Document
    | Education
    | Inquiry
    | Investigation
    | Prev
    | Poligraf
    | Staff
    | Workplace,
    Field(discriminator="item"),
]


class ItemModel(BaseModel):
    """Validation class."""

    __root__ = ItemType

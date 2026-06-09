"""PyDantic models."""

from __future__ import annotations

import re
from datetime import date  # noqa: TC003
from typing import Literal

from pydantic import BaseModel, Field, validator

from app.classes.enums import Conclusions, Decisions, Roles
from app.utilities.utils import validate_inn, validate_snils

tables = [
    "addresses",
    "affilations",
    "checks",
    "contacts",
    "documents",
    "educations",
    "inquiries",
    "investigations",
    "poligrafs",
    "previous",
    "staffs",
    "workplaces",
]

ItemType = Literal[
    "addresses",
    "affilations",
    "checks",
    "contacts",
    "documents",
    "educations",
    "inquiries",
    "investigations",
    "poligrafs",
    "previous",
    "staffs",
    "workplaces",
]


class TableModel(BaseModel):
    """Pydantic model for tables name."""

    __root__: ItemType


class User(BaseModel):
    """Pydantic model for user form."""

    fullname: str
    username: str
    email: str
    role: Roles = Field(Roles.guest.value)

    class Config:
        use_enum_values = True
        anystr_strip_whitespace = True
        max_anystr_length = 255

    @validator("username")
    @classmethod
    def check_username(cls, username: str) -> str:
        """Check username."""
        return username.lower()


class Action(BaseModel):
    """Pydantic model for user action."""

    action: Literal["block", "reset", "delete"]


class Query(BaseModel):
    """Query model."""

    search: str | None
    limit: int = 10
    page: int


class Person(BaseModel):
    """Pydantic model form schema."""

    surname: str = Field(max_length=255)
    firstname: str = Field(max_length=255)
    patronymic: str | None = Field(default=None, max_length=255)
    birthday: date
    birthplace: str | None = Field(None, max_length=255)
    citizenship: str | None = Field(default=None, max_length=255)
    dual: str | None = Field(default=None, max_length=255)
    snils: str | None = None
    inn: str | None = None
    marital: str | None = Field(default=None, max_length=255)
    addition: str | None = None
    editable: bool = False

    class Config:
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


class Prev(BaseModel):
    """Previous in schema."""

    surname: str = Field(max_length=255)
    firstname: str | None = Field(default=None, max_length=255)
    patronymic: str | None = Field(default=None, max_length=255)
    changed: str | None = Field(default=None, max_length=4)
    reason: str | None = None
    item: Literal["previous"]

    class Config:
        anystr_strip_whitespace = True


class Education(BaseModel):
    """Education in schema."""

    view: str | None = Field(default=None, max_length=255)
    institution: str = Field(max_length=255)
    finished: str | None = Field(default=None, max_length=4)
    specialty: str | None = None
    item: Literal["educations"]

    class Config:
        anystr_strip_whitespace = True


class Staff(BaseModel):
    """Staffs schema."""

    position: str
    department: str | None
    item: Literal["staffs"]

    class Config:
        anystr_strip_whitespace = True
        max_anystr_length = 255


class Document(BaseModel):
    """Document in schema."""

    view: str | None = "Паспорт"
    series: str | None = None
    digits: str = Field(max_length=12)
    agency: str | None = Field(default=None, max_length=255)
    issue: date | None = None
    item: Literal["documents"]

    class Config:
        anystr_strip_whitespace = True


class Address(BaseModel):
    """Address in schema."""

    view: str
    address: str
    item: Literal["addresses"]

    class Config:
        anystr_strip_whitespace = True
        max_anystr_length = 255


class Contact(BaseModel):
    """Contacts in schema."""

    view: str
    contact: str
    item: Literal["contacts"]

    class Config:
        anystr_strip_whitespace = True
        max_anystr_length = 255


class Workplace(BaseModel):
    """Workplaces in schema."""

    now_work: bool | None
    starts: date | None = None
    finished: date | None | str
    workplace: str = Field(max_length=255)
    address: str | None = Field(None, max_length=255)
    position: str = Field(max_length=255)
    reason: str | None = None
    item: Literal["workplaces"]

    class Config:
        anystr_strip_whitespace = True


class Affilation(BaseModel):
    """Affilation in schema."""

    view: str = Field(max_length=255)
    organization: str = Field(max_length=255)
    inn: str | None = Field(None, max_length=12)
    activity: str | None = None
    item: Literal["affilations"]

    class Config:
        anystr_strip_whitespace = True


class Check(BaseModel):
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

    class Config:
        use_enum_values = True
        anystr_strip_whitespace = True


class Poligraf(BaseModel):
    """Poligraf in schema."""

    theme: str = Field(max_length=255)
    results: str
    conclusion: Decisions
    item: Literal["poligrafs"]

    class Config:
        use_enum_values = True
        anystr_strip_whitespace = True


class Investigation(BaseModel):
    """Investigations in schema."""

    theme: str = Field(max_length=255)
    info: str
    item: Literal["investigations"]

    class Config:
        anystr_strip_whitespace = True


class Inquiry(BaseModel):
    """Inquiries in schema."""

    info: str
    initiator: str = Field(max_length=255)
    item: Literal["inquiries"]

    class Config:
        anystr_strip_whitespace = True


class ItemsModels(BaseModel):
    """Items schemas."""

    __root__: (
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
        | Workplace
    ) = Field(..., discriminator="item")

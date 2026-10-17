"""Utils."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import jwt
from flask import g

from app.classes.enums import Conclusions
from app.models.model import Person, Registry


def create_token(identity: str, config: dict, item: str = "ACCESS") -> str:
    """Create token."""
    return jwt.encode(
        {
            "identity": identity,
            "exp": datetime.now(UTC)
            + timedelta(minutes=config[f"{item}_SECRET_KEY_LIVE"]),
        },
        config[f"{item}_SECRET_KEY"],
        algorithm="HS256",
    )


def decode_token(token: str, config: dict, *, refresh: bool = False) -> dict | None:
    """Decode JWT token and return payload."""
    try:
        return jwt.decode(
            token,
            config[f"{'REFRESH' if refresh else 'ACCESS'}_SECRET_KEY"],
            algorithms=["HS256"],
            options={"verify_exp": config["AUTH"]},
        )
    except jwt.exceptions.InvalidTokenError:
        return None


def add_person(peerson_data: Person, config: dict) -> int | None:
    """Add a record in persons table."""
    cur = g.db.cursor()
    person = cur.execute(
        "SELECT id FROM persons WHERE\
            surname=? AND firstname=? AND patronymic=? AND birthday=?",
        (
            peerson_data.surname,
            peerson_data.firstname,
            peerson_data.patronymic,
            peerson_data.birthday,
        ),
    ).fetchone()

    cand_id = person[0] if person else None
    if cand_id:
        return None

    data_dict = peerson_data.dict()
    data_dict["user_id"] = g.current_user["id"]
    data_dict["created"] = datetime.now(UTC)
    stmt = "INSERT INTO persons ({}) VALUES ({})".format(  # noqa: S608
        ",".join(data_dict.keys()),
        ",".join(["?"] * len(data_dict)),
    )
    cand_id = cur.execute(stmt, tuple(data_dict.values())).lastrowid

    if cand_id:
        destination = Path(
            config["BASE_PATH"],
            "Главный офис",
            peerson_data.surname[0],
            "{}-{} {} {}".format(
                cand_id,
                peerson_data.surname,
                peerson_data.firstname,
                peerson_data.patronymic or "",
            ).rstrip(),
        )
        destination.mkdir(parents=True, exist_ok=True)
        stmt = "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
            ",".join(f"{k}=?" for k in data_dict),
        )
        cur.execute(stmt, (*data_dict.values(), cand_id))
        g.db.commit()
    return cand_id


def add_registry(json_data: Registry, cand_id: int) -> None:
    """Add a record in registry table."""
    data_dict = json_data.dict()
    data_dict["officer"] = g.current_user["id"]
    data_dict["incomes"] = datetime.now(UTC)
    data_dict["results"] = Conclusions.checks.value
    data_dict["person_id"] = cand_id
    stmt = "INSERT INTO registry ({}) VALUES ({})".format(  # noqa: S608
        ",".join(data_dict.keys()),
        ",".join(["?"] * len(data_dict)),
    )
    cur = g.db.cursor()
    cur.execute(stmt, tuple(data_dict.values()))
    g.db.commit()

"""Utils."""

from datetime import UTC, datetime, timedelta
from pathlib import Path

import jwt
from flask import g

from app.classes.enums import Conclusions
from app.models.model import Person, Registry


def validate_inn(inn: str | None) -> str | None:
    """Check inn."""
    if not inn:
        return None
    inn = inn.replace("-", "").replace(" ", "")
    if len(inn) != 12 or not inn.isdigit():
        return None
    c1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0, 0]
    c2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
    check1 = sum(int(inn[i]) * c1[i] for i in range(12)) % 11 % 10
    check2 = sum(int(inn[i]) * c2[i] for i in range(12)) % 11 % 10
    if check1 == int(inn[10]) and check2 == int(inn[11]):
        return inn
    return None


def validate_snils(snils: str | None) -> str | None:
    """Check snils."""
    if not snils:
        return None
    # Получаем первые 9 цифр и контрольное число (последние 2)
    snils = snils.replace("-", "").replace(" ", "")
    if len(snils) != 11 or not snils.isdigit():
        return None
    digits = [int(d) for d in snils]
    main_part = digits[:9]
    check_sum = int(snils[9:])

    # Вычисляем контрольную сумму
    sum_prod = sum(main_part[i] * (9 - i) for i in range(9))

    # Алгоритм проверки контрольного числа
    calculated_sum = 0
    if sum_prod < 100:
        calculated_sum = sum_prod
    elif sum_prod in {100, 101}:
        calculated_sum = 0
    else:
        remainder = sum_prod % 101
        calculated_sum = 0 if remainder == 100 else remainder
    if calculated_sum == check_sum:
        return snils
    return None


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

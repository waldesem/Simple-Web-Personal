"""Utils."""

from datetime import UTC, datetime, timedelta

import jwt
from flask import current_app


def validate_inn(inn: str | None) -> str | None:
    """Check inn."""
    if not inn:
        return None
    inn = inn.replace("-", "").replace(" ", "")
    if len(inn) != 12 and not inn.isdigit():
        return "CORRUPTED!"
    c1 = [7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0, 0]
    c2 = [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8, 0]
    check1 = sum([int(inn[i]) * c1[i] for i in range(12)]) % 11 % 10
    check2 = sum([int(inn[i]) * c2[i] for i in range(12)]) % 11 % 10
    if check1 == int(inn[10]) and check2 == int(inn[11]):
        return inn
    return "CORRUPTED!"


def validate_snils(snils: str | None) -> str | None:
    """Check snils."""
    if not snils:
        return None
    # Получаем первые 9 цифр и контрольное число (последние 2)
    snils = snils.replace("-", "").replace(" ", "")
    if len(snils) != 11 and not snils.isdigit():
        return "CORRUPTED!"
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
    return "CORRUPTED!"


def create_token(user_id: int, item: str = "ACCESS") -> str:
    """Create token."""
    return jwt.encode(
        {
            "id": user_id,
            "exp": datetime.now(UTC)
            + timedelta(minutes=current_app.config[f"{item}_SECRET_KEY_LIVE"]),
        },
        current_app.config[f"{item}_SECRET_KEY"],
        algorithm="HS256",
    )


def decode_token(token: str, *, refresh: bool = False) -> dict | None:
    """Decode JWT token and return payload."""
    try:
        return jwt.decode(
            token,
            current_app.config[f"{'REFRESH' if refresh else 'ACCESS'}_SECRET_KEY"],
            algorithms=["HS256"],
            options={"verify_exp": True},
        )
    except (jwt.exceptions.InvalidTokenError, IndexError, AttributeError):
        return None

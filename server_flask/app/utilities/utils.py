"""Utils."""

from sqlite3 import Cursor


def insert_into_db(cur: Cursor, table: str, data: dict) -> int | None:
    """Insert data into db."""
    stmt = "INSERT INTO {} ({}) VALUES ({})".format(  # noqa: S608
        table,
        ",".join(data.keys()),
        ",".join(["?"] * len(data)),
    )
    return cur.execute(stmt, tuple(data.values())).lastrowid


def update_db(cur: Cursor, table: str, data: dict, item_id: int) -> None:
    """Update data in db."""
    stmt = "UPDATE {} SET {} WHERE id = ?".format(  # noqa: S608
        table,
        ",".join(f"{k}=?" for k in data),
    )
    cur.execute(stmt, (*data.values(), item_id))


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

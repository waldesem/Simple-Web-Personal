"""DB quiries."""

from sqlite3 import Cursor


def select_from_db(cur: Cursor, table: str, person_id: int) -> list[dict]:
    """Select items from databse."""
    return [
        dict(item)
        for item in cur.execute(
            f"SELECT * FROM {table} WHERE person_id = ?",  # noqa: S608
            (person_id,),
        ).fetchall()
    ]


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

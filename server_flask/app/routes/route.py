"""Routes."""

import getpass
import sqlite3
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Literal

from flask import Blueprint, Response, g, jsonify, request

from constants import BASE_PATH, DATABASE_URI

bp = Blueprint("routes", __name__, url_prefix="/routes")


@lru_cache
def get_user_id(cur: sqlite3.Cursor) -> int | None:
    """Retrieve the current user."""
    username = getpass.getuser()
    user = cur.execute(
        "SELECT id FROM users WHERE username = ?",
        (username.lower(),),
    ).fetchone()
    return user[0] if user else None


@bp.before_request
def _load_connection() -> None:
    db = sqlite3.connect(DATABASE_URI)
    db.row_factory = sqlite3.Row
    g.db = db


@bp.teardown_app_request  # ty:ignore[invalid-argument-type]
def _close_connection(_exception: Exception) -> None:
    if db := g.pop("db", None):
        db.close()


@bp.get("/candidates")
def get_candidates(per_page: int = 10) -> tuple[Response, Literal[200]]:
    """Retrieve a paginated list of persons from the database."""
    query = request.args
    params = []
    stmt = "SELECT id, surname, firstname, patronymic, birthday, created FROM persons"
    if query.get("search"):
        search = query["search"].upper().split(maxsplit=3)
        stmt += " WHERE surname = ?"
        params.append(search[0])
        if len(search) > 1:
            stmt += " AND firstname = ?"
            params.append(search[1])
            if len(search) > 2:
                stmt += " AND patronymic = ?"
                params.append(search[2])
    stmt += " ORDER BY id DESC LIMIT ? OFFSET ?"

    # Пагинация списка кандидатов
    cur: sqlite3.Cursor = g.db.cursor()
    candidates = cur.execute(
        stmt,
        (*params, per_page + 1, int(query["page"]) * per_page),
    ).fetchall()
    has_next = len(candidates) > per_page
    return jsonify(
        {
            "has_next": has_next,
            "candidates": [
                dict(cand) for cand in (candidates[:-1] if has_next else candidates)
            ],
        },
    ), 200


@bp.get("/persons/<int:person_id>")
def get_person(person_id: int) -> tuple[Response, Literal[200]]:
    """Retrieve an item from the database based on the provided item ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    return jsonify(
        dict(
            cur.execute("SELECT * FROM persons WHERE id = ?", (person_id,)).fetchone(),
        ),
    ), 200


@bp.post("/persons")
def post_person() -> tuple[Response, Literal[201]]:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cur: sqlite3.Cursor = g.db.cursor()
    resume: dict = request.get_json()
    person = cur.execute(
        """
        SELECT id FROM persons WHERE
        surname=? AND firstname=? AND patronymic=? AND birthday=DATE(?)
        """,
        (
            resume["surname"],
            resume["firstname"],
            resume.get("patronymic", ""),
            resume["birthday"],
        ),
    ).fetchone()

    if not (cand_id := person[0] if person else None):
        resume["editable"] = False
        resume["user_id"] = get_user_id(cur)
        resume["created"] = datetime.now().isoformat()
        cand_id = cur.execute(
            "INSERT INTO persons ({}) VALUES ({})".format(  # noqa: S608
                ",".join(resume.keys()),
                ",".join(["?"] * len(resume)),
            ),
            tuple(resume.values()),
        ).lastrowid

        destination = Path(
            BASE_PATH,
            "Главный офис",
            resume["surname"][0],
            "{}-{} {} {}".format(
                cand_id,
                resume["surname"],
                resume["firstname"],
                resume.get("patronymic", ""),
            ).rstrip(),
        )
        destination.mkdir(parents=True, exist_ok=True)

        cur.execute(
            "UPDATE persons SET destination = ? WHERE id = ?",
            (str(destination), cand_id),
        )
        g.db.commit()
    return jsonify({"person_id": cand_id}), 201


@bp.patch("/persons/<int:person_id>")
def patch_person(person_id: int) -> tuple[Literal[""], Literal[200]]:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cur: sqlite3.Cursor = g.db.cursor()
    resume: dict = request.get_json()
    resume["user_id"] = get_user_id(cur)
    cur.execute(
        "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
            ",".join(f"{k}=?" for k in resume),
        ),
        (*resume.values(), person_id),
    )
    g.db.commit()
    return "", 200


@bp.get("/<item>/<int:person_id>")
def get_item(item: str, person_id: int) -> tuple[Response, Literal[200]]:
    """Get an item based on the provided item."""
    cur: sqlite3.Cursor = g.db.cursor()
    items = cur.execute(
        f"SELECT * FROM {item} WHERE person_id = ?",  # noqa: S608
        (person_id,),
    ).fetchall()
    return jsonify([dict(itm) for itm in items]), 200


@bp.post("/<item>/<int:person_id>")
def post_item(item: str, person_id: int) -> tuple[Literal[""], Literal[201]]:
    """Insert or replaces a record in the specified table."""
    json_dict: dict = request.get_json()
    json_dict.update({"person_id": person_id, "created": datetime.now().isoformat()})

    # Проверяем, есть ли ключ "id" в словаре json_dict
    cur: sqlite3.Cursor = g.db.cursor()
    if item_id := json_dict.pop("id", None):
        # Если есть, создаем запрос на обновление записи с указанным id
        stmt = "UPDATE {} SET {} WHERE id = ?".format(  # noqa: S608
            item,
            ",".join(f"{k}=?" for k in json_dict),
        )
        cur.execute(stmt, (*json_dict.values(), item_id))
    else:
        # Если нет, создаем запрос на вставку новой записи
        stmt = "INSERT INTO {} ({}) VALUES ({})".format(  # noqa: S608
            item,
            ",".join(json_dict.keys()),
            ",".join(["?"] * len(json_dict)),
        )
        cur.execute(stmt, tuple(json_dict.values()))
    g.db.commit()
    return "", 201


@bp.delete("/<item>/<int:item_id>")
def delete_item(item: str, item_id: int) -> tuple[Literal[""], Literal[204]]:
    """Delete an item from the database with provided item name and item ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    cur.execute(
        f"DELETE FROM {item} WHERE id = ?",  # noqa: S608
        (item_id,),
    )
    g.db.commit()
    return "", 204

"""Routes."""

import sqlite3
from datetime import datetime

from flask import Blueprint, Response, abort, current_app, g, jsonify, request

from app.depends.depend import (
    Item,
    create_dest,
    create_query,
    get_user_id,
    make_dicts,
)

bp = Blueprint("routes", __name__, url_prefix="/routes")


@bp.before_request
def _load_connection() -> None:
    db = sqlite3.connect(current_app.config["DATABASE_URI"])
    db.row_factory = make_dicts
    g.db = db


@bp.teardown_app_request
def _close_connection(_exception: Exception) -> None:
    if db := g.pop("db", None):
        db.close()


@bp.get("/candidates/<int:page>")
def get_candidates(page: int, per_page: int = 10) -> Response:
    """Retrieve a paginated list of persons from the database."""
    query = request.args
    stmt, params = create_query(query)
    # Пагинация списка кандидатов
    cur: sqlite3.Cursor = g.db.cursor()
    candidates = cur.execute(stmt, (*params, per_page + 1, page * per_page)).fetchall()
    has_next = len(candidates) > per_page
    return jsonify(
        {
            "has_next": has_next,
            "candidates": candidates[:-1] if has_next else candidates,
        },
    ), 200


@bp.get("/persons/<int:person_id>")
def get_person(person_id: int) -> Response:
    """Retrieve an item from the database based on the provided item ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    return jsonify(
        cur.execute("SELECT * FROM persons WHERE id = ?", (person_id,)).fetchone(),
    ), 200


@bp.post("/persons")
def post_person() -> Response:
    """Replace a record in persons table."""
    # Загружаем резюме, получаем id кандидата, а также был ли он ранее загружен
    cur: sqlite3.Cursor = g.db.cursor()
    user_id = get_user_id(cur)
    resume: dict = request.get_json()
    resume["user_id"] = user_id

    if not (cand_id := resume.pop("id", None)):
        person = cur.execute(
            """
                SELECT * FROM persons WHERE
                surname=? AND firstname=? AND patronymic=? AND birthday=DATE(?)
            """,
            (
                resume["surname"],
                resume["firstname"],
                resume.get("patronymic", ""),
                resume["birthday"],
            ),
        ).fetchone()

        if not person:
            cand_id = cur.execute(
                "INSERT INTO persons ({}) VALUES ({})".format(  # noqa: S608
                    ",".join(resume.keys()),
                    ",".join(["?"] * len(resume)),
                ),
                tuple(resume.values()),
            ).lastrowid

            destination = create_dest(resume | {"id": cand_id})
            cur.execute(
                "UPDATE persons SET destination = ? WHERE id = ?",
                (destination, cand_id),
            )
            g.db.commit()
            return jsonify({"person_id": cand_id, "exists": False}), 201

    cur.execute(
        "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
            ",".join(f"{k}=?" for k in resume),
        ),
        (*resume.values(), cand_id),
    )
    g.db.commit()
    return jsonify({"person_id": cand_id, "exists": True}), 201


@bp.delete("/persons/<int:person_id>")
def delete_person(person_id: int) -> Response:
    """Delete person from the database based on ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    for table in Item:
        cur.execute(
            f"DELETE FROM {table.value} WHERE person_id = ?",  # noqa: S608
            (person_id,),
        )
    cur.execute("DELETE FROM persons WHERE id = ?", (person_id,))
    g.db.commit()
    return "", 204


@bp.get("/<item>/<int:person_id>")
def get_item(item: Item, person_id: int) -> Response:
    """Get an item based on the provided item."""
    cur: sqlite3.Cursor = g.db.cursor()
    return jsonify(
        cur.execute(
            f"SELECT * FROM {item} WHERE person_id = ?",  # noqa: S608
            (person_id,),
        ).fetchall()
    ), 200


@bp.post("/<item>/<int:person_id>")
def post_item(item: Item, person_id: int) -> Response:
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
def delete_item(item: Item, item_id: int) -> Response:
    """Delete an item from the database with provided item name and item ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    cur.execute(
        f"DELETE FROM {item} WHERE id = ?",  # noqa: S608
        (item_id,),
    )
    g.db.commit()
    return "", 204

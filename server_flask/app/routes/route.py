"""Routes."""

from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import validize
from app.models.model import Query

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("route", __name__)


@bp.get("/candidates/<text_search>")
@validize()
def get_candidates(text_search: str, json_query: Query) -> Response:
    """Retrieve a paginated list of persons from the database."""
    params = []
    stmt = "SELECT "
    if json_query.search:
        if text_search == "fts":
            stmt += "rowid as id,surname,firstname,patronymic,birthday,created \
                FROM persons_fts WHERE persons_fts MATCH ? ORDER BY rowid DESC"
            params.append(json_query.search)
        else:
            stmt += "id, surname, firstname, patronymic, birthday, created FROM persons"
            search = json_query.search.upper().split(maxsplit=3)
            stmt += " WHERE surname = ?"
            params.append(search[0])
            if len(search) > 1:
                stmt += " AND firstname = ?"
                params.append(search[1])
                if len(search) > 2:
                    stmt += " AND patronymic = ?"
                    params.append(search[2])
            stmt += " ORDER BY id DESC"
    else:
        stmt += "id, surname, firstname, patronymic, birthday, created \
            FROM persons  ORDER BY id DESC"
    # Пагинация списка кандидатов
    cur: sqlite3.Cursor = g.db.cursor()
    candidates = cur.execute(
        stmt + " LIMIT ? OFFSET ?",
        (*params, json_query.limit + 1, json_query.page * json_query.limit),
    ).fetchall()
    return jsonify([dict(cand) for cand in candidates])

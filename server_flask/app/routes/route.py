"""Routes."""

from typing import TYPE_CHECKING, Literal

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import validize
from app.models.model import Query

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("route", __name__)


@bp.get("/candidates")
@validize()
def get_candidates(json_query: Query) -> tuple[Response, Literal[200]]:
    """Retrieve a paginated list of persons from the database."""
    params = []
    stmt = "SELECT id, surname, firstname, patronymic, birthday, created FROM persons"
    if json_query.search:
        search = json_query.search.upper().split(maxsplit=3)
        stmt += " WHERE surname = ?"
        params.append(search[0])
        if len(search) > 1:
            stmt += " AND firstname = ?"
            params.append(search[1])
            if len(search) > 2:
                stmt += " AND patronymic = ?"
                params.append(search[2])
    # Пагинация списка кандидатов
    cur: sqlite3.Cursor = g.db.cursor()
    candidates = cur.execute(
        stmt + " ORDER BY id DESC LIMIT ? OFFSET ?",
        (*params, json_query.limit + 1, json_query.page * json_query.limit),
    ).fetchall()
    return jsonify([dict(cand) for cand in candidates]), 200

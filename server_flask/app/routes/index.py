"""Routes."""

from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify, request

from app.depends.depend import validize
from app.models.model import Query

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("index", __name__)


@bp.get("/index/")
@validize()
def get_candidates(json_query: Query) -> Response:
    """Retrieve a paginated list of persons from the database."""
    params = []
    stmt = "SELECT rowid as id, surname, firstname, patronymic, birthday, created \
        FROM persons_fts"
    if json_query.search:
        params.append(json_query.search)
        stmt += " WHERE persons_fts MATCH ?"
    # Пагинация списка кандидатов
    cur = g.db.cursor()
    candidates = cur.execute(
        stmt + " ORDER BY id DESC LIMIT ? OFFSET ?",
        (*params, json_query.limit + 1, json_query.page * json_query.limit),
    ).fetchall()
    return jsonify([dict(cand) for cand in candidates])


@bp.get("/index/history/")
def get_history() -> Response:
    """Retrieve a persons from the database based on the provided ID."""
    if ids := request.args.get("ids"):
        cur: sqlite3.Cursor = g.db.cursor()
        persons = cur.execute(
            f"SELECT id, surname, firstname, patronymic, birthday, created\
                FROM persons WHERE id IN ({ids})",  # noqa: S608
        ).fetchall()
        return jsonify([dict(cand) for cand in persons])
    return jsonify([])

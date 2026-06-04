"""Routes."""

from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify, request

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("route", __name__)


@bp.get("/candidates")
def get_candidates() -> Response:
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
    # Пагинация списка кандидатов
    cur: sqlite3.Cursor = g.db.cursor()
    candidates = cur.execute(
        stmt + " ORDER BY id DESC LIMIT ? OFFSET ?",
        (*params, int(query["limit"]) + 1, int(query["page"]) * int(query["limit"])),
    ).fetchall()
    return jsonify([dict(cand) for cand in candidates]), 200

"""Routes."""

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import validize
from app.models.model import Query

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

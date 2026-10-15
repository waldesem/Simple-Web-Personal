"""Routes."""

from flask import Blueprint, Response, g, jsonify

from app.classes.enums import Roles
from app.depends.depend import authorize, validize
from app.models.model import Query

bp = Blueprint("index", __name__)


@bp.get("/index/")
@validize()
def get_search(json_query: Query) -> Response:
    """Retrieve a paginated list of persons from the database."""
    stmt = "SELECT id, surname, firstname, patronymic, birthday, created FROM persons"
    # Пагинация списка кандидатов
    params = []
    if json_query.search:
        names = json_query.search.split()
        params.append(names[0])
        stmt += " WHERE surname=?"
        if len(names) > 1:
            params.append(names[1])
            stmt += " AND firstname=?"
            if len(names) > 2:
                params.append(names[2])
                stmt += " AND patronymic=?"
    cur = g.db.cursor()
    candidates = cur.execute(
        stmt + " ORDER BY id DESC LIMIT ? OFFSET ?",
        (*params, json_query.limit + 1, json_query.page * json_query.limit),
    ).fetchall()
    return jsonify([dict(cand) for cand in candidates])


@bp.get("/registry")
def get_registry(json_query: Query) -> Response:
    """Retrieve a registry from the database."""
    cur = g.db.cursor()
    registry = cur.execute(
        "SELECT * FROM registry ORDER BY id DESC ORDER BY id DESC LIMIT ? OFFSET ?",
        (json_query.limit + 1, json_query.page * json_query.limit),
    ).fetchall()
    return jsonify([dict(reg) for reg in registry])


@bp.delete("/registry/<int:reg_id>")
@authorize(Roles.user)
def del_registry(reg_id: int) -> Response:
    """Delete a row from registry."""
    cur = g.db.cursor()
    cur.execute("DELETE FROM registry WHERE id = ?", (reg_id,))
    g.db.commit()
    return jsonify({"message": "success"})

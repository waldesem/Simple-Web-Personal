"""Routes."""

from datetime import UTC, datetime

from flask import Blueprint, Response, current_app, g, jsonify

from app.classes.enums import Conclusions, Roles
from app.depends.depend import authorize, validize
from app.models.model import Person, Query, RegExt, Registry
from app.shared.share import add_person, add_registry

bp = Blueprint("registry", __name__, url_prefix="/registry")


@bp.get("/")
def get_registry(json_query: Query) -> Response:
    """Retrieve a registry from the database."""
    cur = g.db.cursor()
    registry = cur.execute(
        "SELECT * FROM registry ORDER BY id DESC ORDER BY id DESC LIMIT ? OFFSET ?",
        (json_query.limit + 1, json_query.page * json_query.limit),
    ).fetchall()
    return jsonify([dict(reg) for reg in registry])


@bp.post("/")
@validize()
@authorize(Roles.user)
def post_registry(json_data: Registry) -> Response:
    """Add a record in registry table."""
    names = json_data.fullname.split()
    person = Person(
        surname=names[0],
        firstname=names[1],
        patronymic=names[2] if len(names) > 2 else "",
        birthday=json_data.birthday,
    )
    if cand_id := add_person(person, current_app.config):
        add_registry(json_data, cand_id)
    return jsonify({"person_id": cand_id})


@bp.patch("/<int:reg_id>")
@validize()
@authorize(Roles.user)
def patch_registry(reg_id: int, json_data: RegExt) -> Response:
    """Edit a record in registry table."""
    data_dict = json_data.dict()
    data_dict["officer"] = g.current_user["id"]
    if json_data.results != Conclusions.checks.value:
        data_dict["finished"] = datetime.now(UTC)
    stmt = "UPDATE registry SET {} WHERE id = ?".format(  # noqa: S608
        ",".join(f"{k}=?" for k in data_dict),
    )
    cur = g.db.cursor()
    cur.execute(stmt, (*data_dict.values(), reg_id))
    g.db.commit()
    return jsonify({"message": "success"})


@bp.delete("/<int:reg_id>")
@authorize(Roles.user)
def del_registry(reg_id: int) -> Response:
    """Delete a row from registry."""
    cur = g.db.cursor()
    cur.execute("DELETE FROM registry WHERE id = ?", (reg_id,))
    g.db.commit()
    return jsonify({"message": "success"})

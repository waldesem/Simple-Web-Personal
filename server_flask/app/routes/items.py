"""Routes."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flask import Blueprint, Response, g, jsonify

from app.classes.enums import Roles
from app.depends.depend import authorize, validize
from app.models.model import ItemsModels, TableModel

if TYPE_CHECKING:
    from sqlite3 import Cursor

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("/<table>/<int:person_id>")
@validize()
def get_items(table: TableModel, person_id: int) -> Response:
    """Get an item based on the provided tables."""
    cur: Cursor = g.db.cursor()
    items = cur.execute(
        f"SELECT * FROM {table.__root__} WHERE person_id = ?",  # noqa: S608
        (person_id,),
    ).fetchall()
    return jsonify([dict(item) for item in items])


@bp.post("/<table>/<int:person_id>")
@validize()
@authorize(Roles.user)
def post(table: TableModel, person_id: int, json_data: ItemsModels) -> Response:
    """Insert a record in the specified table."""
    data = json_data.__root__.dict(exclude={"comparator"})
    data["person_id"] = person_id
    data["created"] = datetime.now(UTC)
    cur: Cursor = g.db.cursor()
    stmt = "INSERT INTO {} ({}) VALUES ({})".format(  # noqa: S608
        table.__root__,
        ",".join(data.keys()),
        ",".join(["?"] * len(data)),
    )
    cur.execute(stmt, tuple(data.values()))
    g.db.commit()
    return jsonify({"message": "success"})


@bp.patch("/<table>/<int:person_id>/<int:item_id>")
@validize()
@authorize(Roles.user)
def patch(
    table: TableModel,
    person_id: int,
    item_id: int,
    json_data: ItemsModels,
) -> Response:
    """Update a record in the specified table."""
    data = json_data.__root__.dict(exclude={"comparator"})
    data["person_id"] = person_id
    data["created"] = datetime.now(UTC)
    cur: Cursor = g.db.cursor()
    stmt = "UPDATE {} SET {} WHERE id = ?".format(  # noqa: S608
        table.__root__,
        ",".join(f"{k}=?" for k in data),
    )
    cur.execute(stmt, (*data.values(), item_id))
    g.db.commit()
    return jsonify({"message": "success"})


@bp.delete("/<table>/<int:item_id>")
@validize()
@authorize(Roles.user)
def delete(table: TableModel, item_id: int) -> Response:
    """Delete an item from the database with provided table name and item ID."""
    cur: Cursor = g.db.cursor()
    cur.execute(f"DELETE FROM {table.__root__} WHERE id = ?", (item_id,))  # noqa: S608
    g.db.commit()
    return jsonify({"message": "success"})

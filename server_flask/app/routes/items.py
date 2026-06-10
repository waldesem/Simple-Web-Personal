"""Routes."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import validize
from app.models.model import ItemsModels, TableModel
from app.utilities.queries import insert_into_db, select_from_db, update_db

if TYPE_CHECKING:
    from sqlite3 import Cursor

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("/<table>/<int:person_id>")
@validize()
def get_items(table: TableModel, person_id: int) -> tuple[Response, Literal[200]]:
    """Get an item based on the provided tables."""
    cur: Cursor = g.db.cursor()
    return jsonify(select_from_db(cur, table.__root__, person_id)), 200


@bp.post("/<table>/<int:person_id>")
@validize()
def post(
    table: TableModel,
    person_id: int,
    json_data: ItemsModels,
) -> tuple[Literal[""], Literal[201]]:
    """Insert a record in the specified table."""
    data = json_data.__root__.dict(exclude={"item"})
    data["person_id"] = person_id
    data["created"] = datetime.now(UTC)
    cur: Cursor = g.db.cursor()
    insert_into_db(cur, table.__root__, data)
    g.db.commit()
    return "", 201


@bp.patch("/<table>/<int:person_id>/<int:item_id>")
@validize()
def patch(
    table: TableModel,
    person_id: int,
    item_id: int,
    json_data: ItemsModels,
) -> tuple[Literal[""], Literal[200]]:
    """Update a record in the specified table."""
    data = json_data.__root__.dict()
    data["person_id"] = person_id
    data["created"] = datetime.now(UTC)
    cur: Cursor = g.db.cursor()
    update_db(cur, table.__root__, data, item_id)
    g.db.commit()
    return "", 200


@bp.delete("/<table>/<int:item_id>")
@validize()
def delete(table: TableModel, item_id: int) -> tuple[Literal[""], Literal[204]]:
    """Delete an item from the database with provided table name and item ID."""
    cur: Cursor = g.db.cursor()
    cur.execute(f"DELETE FROM {table.__root__} WHERE id = ?", (item_id,))  # noqa: S608
    g.db.commit()
    return "", 204

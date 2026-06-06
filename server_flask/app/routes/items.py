"""Routes."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from flask import Blueprint, Response, g, jsonify

from app.depends.depend import validize
from app.models.model import ItemsModels, ItemType

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("items", __name__, url_prefix="/items")


@bp.get("/<item>/<int:person_id>")
def get_item(item: ItemType, person_id: int) -> tuple[Response, Literal[200]]:
    """Get an item based on the provided item."""
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = f"SELECT * FROM {item} WHERE person_id = ?"  # noqa: S608
    items = cur.execute(stmt, (person_id,)).fetchall()
    return jsonify([dict(itm) for itm in items]), 200


@bp.post("/<item>/<int:person_id>")
@validize()
def post_item(
    item: ItemType,
    person_id: int,
    json_data: ItemsModels,
) -> tuple[Literal[""], Literal[201]]:
    """Insert a record in the specified table."""
    data = json_data.__root__.dict(exclude={"item"})
    data["person_id"] = person_id
    data["created"] = datetime.now(UTC)
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "INSERT INTO {} ({}) VALUES ({})".format(  # noqa: S608
        item,
        ",".join(data.keys()),
        ",".join(["?"] * len(data)),
    )
    cur.execute(stmt, tuple(data.values()))
    g.db.commit()
    return "", 201


@bp.patch("/<item>/<int:person_id>/<int:item_id>")
@validize()
def patch_item(
    item: ItemType,
    person_id: int,
    item_id: int,
    json_data: ItemsModels,
) -> tuple[Literal[""], Literal[200]]:
    """Update a record in the specified table."""
    data = json_data.__root__.dict()
    data["person_id"] = person_id
    data["created"] = datetime.now(UTC)
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "UPDATE {} SET {} WHERE id = ?".format(  # noqa: S608
        item,
        ",".join(f"{k}=?" for k in data),
    )
    cur.execute(stmt, (*data.values(), item_id))
    g.db.commit()
    return "", 200


@bp.delete("/<item>/<int:item_id>")
def delete_item(item: ItemType, item_id: int) -> tuple[Literal[""], Literal[204]]:
    """Delete an item from the database with provided item name and item ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    cur.execute(f"DELETE FROM {item} WHERE id = ?", (item_id,))  # noqa: S608
    g.db.commit()
    return "", 204

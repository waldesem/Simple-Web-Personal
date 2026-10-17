"""Routes."""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from flask import Blueprint, Response, current_app, g, jsonify

from app.classes.enums import Roles
from app.depends.depend import authorize, validize
from app.models.model import Anketa, Person, Query, Registry
from app.shared.share import add_person, add_registry

if TYPE_CHECKING:
    import sqlite3

bp = Blueprint("persons", __name__, url_prefix="/persons")


@bp.get("/")
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


@bp.get("/<int:person_id>")
def get_person(person_id: int) -> Response:
    """Retrieve a person from the database based on the provided ID."""
    cur: sqlite3.Cursor = g.db.cursor()
    person = cur.execute("SELECT * FROM persons WHERE id = ?", (person_id,)).fetchone()
    return jsonify(dict(person))


@bp.post("/")
@validize()
@authorize(Roles.user)
def post_person(json_data: Person) -> Response:
    """Add a record in persons table."""
    cand_id = add_person(json_data, current_app.config)
    return jsonify({"person_id": cand_id})


@bp.post("/json")
@validize()
@authorize(Roles.user)
def post_json_file(json_data: Anketa) -> Response:
    """Create a new person or updates an existing person from json."""
    cur: sqlite3.Cursor = g.db.cursor()

    cand_id = add_person(cur, Person.parse_obj(json_data))
    if cand_id:
        add_registry(
            Registry(
                fullname=f"{json_data.surname} {json_data.firstname} {json_data.patronymic}",
                birthday=json_data.birthday,
                staff=f"{json_data.position} / {json_data.department}",
            ),
            cand_id,
        )
        # Сохранение дополнительной информации о кандидате в БД
        items: dict[str, list[dict[str, Any]]] = {
            "documents": [
                {
                    "digits": json_data.digits,
                    "series": json_data.series,
                    "issue": json_data.issue,
                    "agency": json_data.agency,
                },
            ],
            "contacts": [
                {
                    "view": "Телефон",
                    "contact": json_data.contact_phone,
                },
                {
                    "view": "Электронная почта",
                    "contact": json_data.email,
                },
                {
                    "view": "Адрес проживания",
                    "address": json_data.valid_address,
                },
                {
                    "view": "Адрес регистрации",
                    "address": json_data.reg_address,
                },
            ],
            "educations": [
                education.dict(exclude={"comparator"})
                for education in json_data.education
                if json_data.education
            ],
            "workplaces": [
                workplace.dict(exclude={"comparator"})
                for workplace in json_data.experience
                if json_data.experience
            ],
            "previous": [
                prev.dict() for prev in json_data.previous if json_data.previous
            ],
            "affilations": [
                affilation.dict(exclude={"comparator"})
                for affilation in json_data.organizations
                if json_data.organizations
            ],
        }

        for table, contents in items.items():
            args = []
            for content in contents:
                content["person_id"] = cand_id
                content["created"] = datetime.now(UTC)
                args.append(tuple(content.values()))
            if params := contents[0].keys() if len(contents) else None:
                stmt = "INSERT INTO {} ({}) VALUES ({})".format(  # noqa: S608
                    table,
                    ",".join(params),
                    ",".join(["?"] * len(params)),
                )
                cur.executemany(stmt, args)
        g.db.commit()

    return jsonify({"person_id": cand_id})


@bp.patch("/<int:person_id>")
@validize()
@authorize(Roles.user)
def patch_person(person_id: int, json_data: Person) -> Response:
    """Replace a record in persons table."""
    data = json_data.dict()
    data["user_id"] = g.current_user["id"]
    data["created"] = datetime.now(UTC)
    cur: sqlite3.Cursor = g.db.cursor()
    stmt = "UPDATE persons SET {} WHERE id = ?".format(  # noqa: S608
        ",".join(f"{k}=?" for k in data),
    )
    cur.execute(stmt, (*data.values(), person_id))
    g.db.commit()
    return jsonify({"message": "success"})

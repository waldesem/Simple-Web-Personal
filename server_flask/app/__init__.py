"""Initialize the Flask application."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

from flask import Flask, Response, g, request
from werkzeug.exceptions import HTTPException

from config import Config

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response as WerkzeugResponse


def create_app(config: type[Config] = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    from app.routes import bp

    app.config.from_object(config)

    app.register_blueprint(bp)  # Register the routes

    @app.get("/")
    @app.get("/<path:path>")
    def static_file(path: str = "index.html") -> Response:
        return app.send_static_file(path)

    @app.before_request
    def _load_connection() -> None | Response:
        if request.path.startswith("/api"):
            db = sqlite3.connect(config.DATABASE_URI)
            db.row_factory = sqlite3.Row
            g.db = db

    @app.teardown_appcontext
    def close_connection(_exception: BaseException | None) -> None:
        g.current_user = None
        if db := g.pop("db", None):
            db.close()

    @app.errorhandler(404)
    def handle_404(error: HTTPException) -> WerkzeugResponse:  # noqa: ARG001
        return app.redirect("/")

    @app.errorhandler(HTTPException)
    def handle_exception(error: HTTPException) -> HTTPException:
        return error

    return app

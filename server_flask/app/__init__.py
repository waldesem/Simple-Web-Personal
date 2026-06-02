"""Initialize the Flask application."""

from __future__ import annotations

import sqlite3

from flask import Flask, Response, g
from werkzeug.exceptions import HTTPException

from constants import DATABASE_URI


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    from app.routes import bp

    app.register_blueprint(bp)  # Register the routes

    @app.get("/")
    @app.get("/<path:path>")
    def static_file(path: str = "index.html") -> Response:
        return app.send_static_file(path)

    @app.before_request
    def _load_connection() -> None | Response:
        if DATABASE_URI is None:
            msg = "DATABASE_URI is not set, check your settings.ini."
            raise RuntimeError(msg)
        db = sqlite3.connect(DATABASE_URI)
        db.row_factory = sqlite3.Row
        g.db = db

    @app.teardown_appcontext
    def _close_connection(_exception: Exception) -> None:
        g.current_user = None
        if db := g.pop("db", None):
            db.close()

    @app.errorhandler(404)
    def handle_404(error: HTTPException) -> Response:  # noqa: ARG001
        return app.redirect("/")

    @app.errorhandler(HTTPException)
    def handle_exception(error: HTTPException) -> HTTPException:
        return error

    return app

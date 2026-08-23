"""Initialize the Flask application."""

from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

from flask import Flask, Response, g, render_template, request
from werkzeug.exceptions import HTTPException

from config import Config

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response as WerkzeugResponse


def create_app(config: type[Config] = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    from app.routes import bp

    app.register_blueprint(bp)  # Register the routes

    @app.get("/")
    @app.get("/<path:path>")
    def static_file(path: str = "index.html") -> Response:
        return app.send_static_file(path)

    @app.before_request
    def load_connection() -> None:
        """Load connection."""
        db = sqlite3.connect(config.DATABASE_URI)
        if request.path.startswith("/api"):
            db.row_factory = sqlite3.Row
            g.db = db

    @app.after_request
    def close_connection(response: Response) -> Response:
        """Clean up resources when the app context pops."""
        g.current_user = None
        if db := g.pop("db", None):
            db.close()
        return response

    @app.errorhandler(sqlite3.Error)
    def handle_sqlite_error(error: sqlite3.Error) -> str:
        """Handle SQLite errors gracefully."""
        app.logger.exception("SQLite error occurred: %s", str(error))
        if db := g.pop("db", None):
            db.rollback()
        return render_template(
            "error.html",
            error={
                "code": 501,
                "name": "Internal Server Error",
                "description": f"{error!s}",
            },
        )

    @app.errorhandler(HTTPException)
    def handle_exception(error: HTTPException) -> WerkzeugResponse:
        if isinstance(error, int):
            app.logger.error("Request finished with error %s", error)
        else:
            app.logger.error(error)
        return app.redirect("/")

    return app

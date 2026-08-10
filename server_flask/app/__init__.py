"""Initialize the Flask application."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flask import Flask, Response
from werkzeug.exceptions import HTTPException

from app.extensions.db import Database
from app.extensions.fts import FullTextSearch
from config import Config

if TYPE_CHECKING:
    from werkzeug.wrappers.response import Response as WerkzeugResponse


def create_app(config: type[Config] = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config)

    db = Database()
    db.init_app(app)

    fts = FullTextSearch()
    fts.init_app(app)

    from app.routes import bp

    app.register_blueprint(bp)  # Register the routes

    @app.get("/")
    @app.get("/<path:path>")
    def static_file(path: str = "index.html") -> Response:
        return app.send_static_file(path)

    @app.errorhandler(HTTPException)
    def handle_exception(error: HTTPException | int) -> WerkzeugResponse:
        if isinstance(error, int):
            app.logger.error("Request finished with error %.", error)
        else:
            app.logger.error(error)
        return app.redirect("/")

    return app

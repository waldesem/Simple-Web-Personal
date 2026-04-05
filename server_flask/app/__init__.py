"""Initialize the Flask application."""

from __future__ import annotations

from flask import Flask, Response
from werkzeug.exceptions import HTTPException


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)

    from app.routes.route import bp as route_bp

    app.register_blueprint(route_bp)  # Register the routes

    @app.get("/")
    @app.get("/<path:path>")
    def static_file(path: str = "index.html") -> Response:
        return app.send_static_file(path)

    @app.errorhandler(404)
    def handle_404(error: HTTPException) -> Response:  # noqa: ARG001
        return app.redirect("/")  # ty:ignore[invalid-return-type]

    @app.errorhandler(HTTPException)
    def handle_exception(error: HTTPException) -> HTTPException:
        return error

    return app

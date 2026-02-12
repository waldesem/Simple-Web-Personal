"""Initialize the Flask application."""

from __future__ import annotations

from flask import Flask, Response
from werkzeug.exceptions import HTTPException

from config import Config


def create_app(config_class: type[Config] = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes.route import bp as route_bp

    app.register_blueprint(route_bp)  # Register the routes

    @app.get("/")
    def main() -> Response:
        return app.send_static_file("index.html")

    @app.get("/<path:path>")
    def static_file(path: str) -> Response:
        return app.send_static_file(path)

    @app.errorhandler(404)
    def handle_404(error: HTTPException) -> Response:  # noqa: ARG001
        return app.redirect("/")

    @app.errorhandler(HTTPException)
    def handle_exception(error: HTTPException) -> HTTPException:
        return error

    return app

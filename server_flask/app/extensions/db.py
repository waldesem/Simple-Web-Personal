"""Full-text search module."""

import sqlite3

from flask import Flask, g, request


class Database:
    """Full-text search extension."""

    def __init__(self) -> None:
        """Init."""

    def init_app(self, app: Flask) -> None:
        """Initialize the app with extension defaults."""
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["db"] = self
        self.uri: str = app.config["DATABASE_URI"]

        app.before_request(self.load_connection)
        app.teardown_appcontext(self.close_connection)

    def load_connection(self) -> None:
        """Load connection."""
        self.db = sqlite3.connect(self.uri)
        if request.path.startswith("/api"):
            self.db.row_factory = sqlite3.Row
            g.db = self.db

    def close_connection(self, _exception: BaseException | None) -> None:
        """Clean up resources when the app context pops."""
        g.current_user = None
        if db := g.pop("db", None):
            db.close()

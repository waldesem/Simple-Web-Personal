"""Initialize the Flask Blueprints."""

from flask import Blueprint

bp = Blueprint("api", __name__, url_prefix="/api")

from .auth import bp as auth_bp  # noqa: E402
from .items import bp as items_bp  # noqa: E402
from .persons import bp as persons_bp  # noqa: E402
from .route import bp as route_bp  # noqa: E402
from .users import bp as users_bp  # noqa: E402

bp.register_blueprint(auth_bp)
bp.register_blueprint(items_bp)
bp.register_blueprint(persons_bp)
bp.register_blueprint(route_bp)
bp.register_blueprint(users_bp)

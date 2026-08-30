"""Initialize the Flask Blueprints."""

from flask import Blueprint

from .auth import bp as auth_bp
from .index import bp as index_bp
from .items import bp as items_bp
from .persons import bp as persons_bp
from .users import bp as users_bp

bp = Blueprint("api", __name__, url_prefix="/api")

bp.register_blueprint(auth_bp)
bp.register_blueprint(index_bp)
bp.register_blueprint(items_bp)
bp.register_blueprint(persons_bp)
bp.register_blueprint(users_bp)

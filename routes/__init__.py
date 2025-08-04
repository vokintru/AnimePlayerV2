from .auth import auth_bp
from .shiki_link import shiki_auth_bp
from .pages import main_bp
from .api import api_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(shiki_auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

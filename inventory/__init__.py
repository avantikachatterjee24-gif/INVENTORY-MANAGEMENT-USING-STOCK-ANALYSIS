from flask import Flask

from inventory.routes import main_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.register_blueprint(main_bp)
    return app

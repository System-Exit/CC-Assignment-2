from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, current_user, login_user, logout_user
from config import Config
from service_interfaces import UserServiceInterface, MessageServiceInterface

# Initialise Flask plugins
bootstrap = Bootstrap()
login_manager = LoginManager()
# Initialise microservice interfaces
usi = DatabaseInterface()
msi = MessageServiceInterface()


def create_app(config_class=Config):
    """
    Construct the core application.

    """
    # Load app and config
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise plugins
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # Import paths of our application
    from app.main import bp as main_bp

    # Register Blueprints
    app.register_blueprint(main_bp)

    # Return the app
    return app

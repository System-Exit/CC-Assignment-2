from flask import Flask
from config import Config
from database_interface import DatabaseInterface

# Initialise database interface class
dbi = DatabaseInterface()


def create_app(config_class=Config):
    """
    Construct the core application.

    """
    # Load app and config
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Import paths of our application
    from app.routes import bp

    # Register Blueprints
    app.register_blueprint(bp)

    # Return the app
    return app

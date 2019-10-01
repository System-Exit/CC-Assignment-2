from flask import Flask
from config import Config
import firebase_admin
from firebase_admin import credentials, firestore

# Load service credentials
if Config.CLOUD_ENV:
    cred = credentials.ApplicationDefault()
else:
    cred = credentials.Certificate(
        ('C:/Users/rocky/Documents/RMIT Work/Year 3 Semester 2'
         '/CC/Assignment 2/service-account-file.json'))
# Initialise firebase app
firebase_admin.initialize_app(cred)
# Define datbase interface
db = firestore.client()


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

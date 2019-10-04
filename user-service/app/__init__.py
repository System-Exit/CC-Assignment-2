from flask import Flask
from config import Config
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage
import os

# Load credentials depending on environment
if Config.CLOUD_ENV:
    # Since we are in cloud, this has already been defined
    pass
else:
    # Set google credential environment variable explicitly
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        'C:/Users/rocky/Documents/RMIT Work/Year 3 Semester 2'
        '/CC/Assignment 2/service-account-file.json'
    )
# Initialise firebase interface
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)
db = firestore.client()
# Initialise google storage interface
sc = storage.Client()


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

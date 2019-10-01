import os


class Config:
    """
    Class for application configuration.

    """
    SECRET_KEY = os.getenv('SECRET_KEY') or "SECRETSOFTHECLOUD"
    CLOUD_ENV = os.getenv('CLOUD_ENV') or False

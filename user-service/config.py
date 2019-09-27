import os


class Config:
    """
    Class for application configuration.

    """
    SECRET_KEY = os.getenv('SECRET_KEY') or "SECRETSOFTHECLOUD"

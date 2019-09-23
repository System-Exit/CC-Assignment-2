import os


class Config:
    """
    Class for application configuration.

    """
    DB_USERNAME = os.getenv('DB_USERNAME') or 'root'
    DB_PASSWORD = os.getenv('DB_PASSWORD') or 'toor'
    DB_HOST = os.getenv('DB_HOST') or '127.0.0.1'
    DB_DATABASE = os.getenv('DB_DATABASE') or 'database'
    DB_QUERY = os.getenv('DB_QUERY') or ''

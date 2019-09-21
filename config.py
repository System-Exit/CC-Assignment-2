import os


class Config:
    """
    Class for application configuration.

    """
    SECRET_KEY = os.getenv('SECRET_KEY') or 'PLACEHOLDERSECRETKEY'
    GDB_USERNAME = os.getenv('GDB_USERNAME') or 'root'
    GDB_PASSWORD = os.getenv('GDB_PASSWORD') or 'toor'
    GDB_HOST = os.getenv('GDB_HOST') or '127.0.0.1'
    GDB_DATABASE = os.getenv('GDB_DATABASE') or 'database'
    GDB_QUERY = os.getenv('GDB_QUERY') or ''

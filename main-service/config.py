import os


class Config:
    """
    Class for application configuration.

    """
    SECRET_KEY = os.getenv('SECRET_KEY') or 'PLACEHOLDERSECRETKEY'
    USER_SERVICE_ADDRESS = os.getenv('USER_SERVICE_ADDRESS') or (
        "https://user-dot-lustrous-oasis-253108.appspot.com")
    MESSAGE_SERVICE_ADDRESS = os.getenv('MESSAGE_SERVICE_ADDRESS') or (
        "https://message-dot-lustrous-oasis-253108.appspot.com")

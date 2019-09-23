import os


class Config:
    """
    Class for application configuration.

    """
    SECRET_KEY = os.getenv('SECRET_KEY') or 'PLACEHOLDERSECRETKEY'
    DBI_ADDRESS = os.getenv('DBI_ADDRESS') or ("https://database-dot-lustrous"
                                               "-oasis-253108.appspot.com")

import os


class Config:
    """
    Class for application configuration.

    """
    SECRET_KEY = os.getenv('SECRET_KEY') or "SECRETSOFTHECLOUD"
    CLOUD_ENV = os.getenv('CLOUD_ENV') or False
    ROUTES_API_KEY = os.getenv('ROUTES_API_KEY') or (
        "AIzaSyCd4mRC2IuplYvR6O4U8XRr2VHsnk8LGNI")
    SERVICE_ACCOUNT_FILE = (
        'C:/Users/rocky/Documents/RMIT Work/Year 3 Semester 2'
        '/CC/Assignment 2/service-account-file.json'
    )

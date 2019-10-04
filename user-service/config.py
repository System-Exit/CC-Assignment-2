import os


class Config:
    """
    Class for application configuration.

    """
    SECRET_KEY = os.getenv('SECRET_KEY') or "SECRETSOFTHECLOUD"
    CLOUD_ENV = os.getenv('CLOUD_ENV') or False
    BUCKET_NAME = os.getenv('BUCKET_NAME') or "s3661720-app-bucket"
    PROFILE_IMAGES_PATH = os.getenv('PROFILE_IMAGES_PATH') or (
        "profile-images")

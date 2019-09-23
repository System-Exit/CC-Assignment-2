import json
import requests
from models import User


class DatabaseInterface:
    """
    Interface class for interactions with the database

    """
    def __init__(self, config_class=Config):
        # Initialise address
        self.api_address = Config.DBI_ADDRESS

    def getuser(self, userid=None):
        """
        Get a user object based on parameters.

        Args:
            userid (str): ID of user to get. Defaults to None.
        Returns:
            The specified user.
            None if no such user exists.

        """
        # Contruct parameters
        params = {}
        if userid:
            params['userid'] = userid
        # Request user details
        response = requests.get(f"{self.api_address}/getuser", params=params)
        data = response.json()
        # Check if user was returned
        if not data['userid']:
            # Return None
            return None
        else:
            # Create user object
            userid = data['userid']
            username = data['username']
            user = User(userid, username)
            # Return user
            return user

    def createuser(self, username, password):
        """
        Add new user to user database table.

        Args:
            username (str): Username for new user.
            password (str): Password for new user.
        Returns:
            bool: Whether or not the user was added.
        """
        # Send data for user creation
        data = {"username": username, "password": password}
        response = requests.get(f"{self.api_address}/createuser", data=data)
        # Get data from repsonse
        data = response.json()
        # Check if successful
        if data['success']:
            return True
        else:
            return False

    def validateuser(self, username, password):
        """
        Verifies if the user with the given username and password exists.

        Args:
            username (str): Username of user to verify.
            password (str): Password of user to verify.
        Retruns:
            True if the user exists and the password is valid, False otherwise.
            User ID if the user exists and password is valid, None otherwise.

        """
        # Send data for user validation
        data = {"username": username, "password": password}
        response = requests.get(f"{self.api_address}/validateuser", data=data)
        # Get data from repsonse
        data = response.json()
        # Check if validation was successful
        if data['success']:
            return True, data['userid']
        else:
            return False, None

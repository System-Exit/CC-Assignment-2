import json
import requests
from models import User
from config import Config


class UserServiceInterface:
    """
    Interface class for interactions with users

    """
    def __init__(self, config_class=Config):
        # Initialise address
        self.api_address = Config.USER_SERVICE_ADDRESS

    def getuser(self, userid=None, username=None):
        """
        Get a user object based on parameters.

        Args:
            userid (str): ID of user to get. Defaults to None.
            username (str): Username of the user to get. Defaults to None.
        Returns:
            The specified user.
            None if no such user exists.

        """
        # Contruct parameters
        senddata = {}
        if userid:
            senddata['id'] = userid
        if username:
            senddata['username'] = username
        # Request user details
        response = requests.post(f"{self.api_address}/getuser", json=senddata)
        recvdata = response.json()
        # Check if user was returned
        if not recvdata.get('id'):
            # Return None
            return None
        else:
            # Create user object
            userid = recvdata.get('id')
            username = recvdata.get('username')
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
        response = requests.post(f"{self.api_address}/createuser", json=data)
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

        """
        # Send data for user validation
        data = {"username": username, "password": password}
        response = requests.post(f"{self.api_address}/validateuser", json=data)
        # Get data from repsonse
        data = response.json()
        # Return whether validation was successful along with userid
        return data['success']


class MessageServiceInterface:
    """
    Interface class for interactions with messages

    """
    def __init__(self):
        """


        """
        pass
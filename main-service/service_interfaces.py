import json
import requests
from datetime import datetime
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
        # Return whether validation was successful along with user id
        return data.get('success'), data.get('id')

    def adduserimage(self, id, file):
        """
        Sends image to user service to assign as new profile image.

        Args:
            id (str): User ID of user to set profile image for.
            file: Image file that will be the user's new profile image.

        """
        # Define files
        files = {'file': (f"{id}.png", file)}
        # Send file and get response
        response = requests.post(
            f"{self.api_address}/adduserimage", files=files)
        data = response.json()
        # Return success of the request
        return data.get('success')

    def getuserimagelink(self, id):
        """
        Gets the link for the given user's profile image.

        Args:
            id (str): User ID of the user to get image of.
        Returns:
            The string url for the image.

        """
        # Define data
        data = {'id': id}
        # Send file and get response
        response = requests.post(
            f"{self.api_address}/getuserimagelink", json=data)
        data = response.json()
        # Return image link
        return data.get('url')


class EventServiceInterface:
    """
    Interface class for interactions with messages.

    """
    def __init__(self):
        # Initialise address
        self.api_address = Config.EVENT_SERVICE_ADDRESS

    def addevent(self, title=None, description=None, user_id=None,
                 address=None, time=None, travel_method=None):
        """
        Creates event for user.

        """
        # Ensure that required attributes are given
        if not title or not user_id or not time:
            return False
        # Send data for user creation
        data = {
            "title": str(title),
            "description": str(description),
            "user_id": str(user_id),
            "address": str(address),
            "time": time.isoformat(),
            "travel_method": str(travel_method),
        }
        response = requests.post(
            f"{self.api_address}/addevent", json=data)
        # Get data from repsonse
        data = response.json()
        # Return whether validation was successful
        return data.get('success')

    def getuserevents(self, user_id):
        """
        Returns the events for a given user.

        """
        # Send data for user creation
        data = {"user_id": user_id}
        response = requests.post(
            f"{self.api_address}/getuserevents", json=data)
        # Get data from repsonse
        data = response.json()
        # Parse event into a dictionary
        events = data.get('events')
        # Return events
        return events

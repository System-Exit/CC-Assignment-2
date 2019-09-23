from flask_login import UserMixin


class User(UserMixin):
    """
    Model for users.

    """
    def __init__(userid, username):
        self.__userid = userid
        self.__username = username

    def get_id(self):
        return self.__userid

    def get_username(self):
        return self.__username

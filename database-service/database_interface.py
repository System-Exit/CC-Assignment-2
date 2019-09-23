from models import User, Base
from config import Config
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from contextlib import contextmanager
import json
import requests
import math


class DatabaseInterface:
    """
    Interface class for interactions with the database

    """
    def __init__(self, config_class=Config):
        # Define SQL connection parameters
        drivername = 'mysql+pymysql'
        username = config_class.DB_USERNAME
        password = config_class.DB_PASSWORD
        host = config_class.DB_HOST
        database = config_class.DB_DATABASE
        query = config_class.DB_QUERY
        # Create engine
        self.engine = create_engine("%s://%s:%s@%s/%s%s" % (
            drivername, username, password, host, database, query))
        # Define session maker
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def sessionmanager(self):
        """
        Context manager for handling sessions.
        Can often used

        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # def createtables(self):
    #     """
    #     Creates all tables in the database.

    #     """
    #     # Create all tables in the database
    #     Base.metadata.create_all(self.engine)

    # def droptables(self):
    #     """
    #     Drops all tables in the database. DO NOT USE LIGHTLY.

    #     """
    #     # Drop all tables in the database
    #     Base.metadata.drop_all(self.engine)

    def getuser(self, userid=None, username=None):
        """
        Get a detached user object based on user's ID.

        Args:
            userid (str): ID of user to get. Defaults to None.
            username (str): Username of user to get. Defaults to None.
        Returns:
            User object detached from any session.
            None if no such user exists.

        """
        # Initialse session
        with self.sessionmanager() as session:
            # If both parameters are false, return None
            if not userid and not username:
                return None
            # Query for user based on parameters
            if userid:
                query = session.query(User).filter(User.userid == userid)
            if username:
                query = session.query(User).filter(User.username == username)
            # Get user
            user = query.first()
            # Check if a user was returned
            if user is None:
                return None
            # Deteach user from session
            session.expunge(user)
        # Return user
        return user

    def createuser(self, username, password):
        """
        Add new user to user database table.
        Also handles hashing and salting of given password.

        Args:
            username (str): Username for new user.
            password (str): Password for new user.
        Returns:
            bool: Whether or not the user was added.
        """
        # Initialse session
        with self.sessionmanager() as session:
            # Check that username is available. If not, return false.
            user = session.query(User).filter(
                   User.username == username).first()
            if(user is not None):
                return False
            # Hash password
            passhash = PasswordHasher().hash(password)
            # Create user
            user = User(
                username=str(username),
                passhash=str(passhash)
            )
            # Add user to database
            session.add(user)
        # Return success
        return True

    def validateuser(self, username, password):
        """
        Verifies if the user with the given username and password exists.

        Args:
            username (str): Username of user to verify.
            password (str): Password of user to verify.
        Retruns:
            True if the user exists and the password is valid, False otherwise.

        """
        # Initialse session
        with self.sessionmanager() as session:
            # Initialise password hasher
            ph = PasswordHasher()
            # Query if user exists
            user = session.query(User).filter(
                User.username == username).first()
            # Check if query returns a user
            if user is not None:
                # Verify whether the password is valid or not
                try:
                    ph.verify(user.passhash, password)
                except VerifyMismatchError:
                    # Password does not match, return false
                    return False, None
                # Check if password needs to be rehashed
                if ph.check_needs_rehash(user.passhash):
                    # Generate new hash
                    rehash = ph.hash(userpass)
                    # Update user record to include new hash
                    user.userpass = rehash
                # Since user exists and password is valid, return true
                return True
            else:
                # User doesn't exist, return false
                return False

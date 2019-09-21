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
        username = config_class.GDB_USERNAME
        password = config_class.GDB_PASSWORD
        host = config_class.GDB_HOST
        database = config_class.GDB_DATABASE
        query = config_class.GDB_QUERY
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

    def createtables(self):
        """
        Creates all tables in the database.

        """
        # Create all tables in the database
        Base.metadata.create_all(self.engine)

    def droptables(self):
        """
        Drops all tables in the database. DO NOT USE LIGHTLY.

        """
        # Drop all tables in the database
        Base.metadata.drop_all(self.engine)

    def getuserbyid(self, userid):
        """
        Get a detached user object based on user's ID.

        Args:
            userid (str): ID of user to get.
        Returns:
            User object detached from any session.
            None if no such user exists.

        """
        # Initialse session
        with self.sessionmanager() as session:
            # Get user
            user = session.query(User).filter(User.userid == userid).first()
            # Check if a user was returned
            if user is None:
                return None
            # Deteach user from session
            session.expunge(user)
        # Return user
        return user

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


class User(Base, UserMixin):
    """
    Model for user accounts.

    """
    # Table name
    __tablename__ = 'USER'
    # Table Columns
    userid = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    passhash = Column(String(200), unique=False, nullable=False)

    def get_id(self):
        return self.userid

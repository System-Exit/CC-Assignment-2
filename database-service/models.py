from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    Model for user accounts.

    """
    # Table name
    __tablename__ = 'USER'
    # Table Columns
    userid = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    passhash = Column(String(200), unique=False, nullable=False)

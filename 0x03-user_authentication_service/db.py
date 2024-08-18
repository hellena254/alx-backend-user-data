#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB Class for interacting with the database."""
    self._engine = create_engine("sqlite:///a.db", echo=True)
    Base.metadata.drop_all(self._engine)
    Base.metadata.create_all(self._engine)
    self.__session = None

    @property
    def _session(self) -> Session:
        """The session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
    """Add a new user to the database
    Args:
         email
         hashed_password
    Returns:
        User, the created user
    """
    new_user = User(email=email, hashed_password=hashed_password)
    self._session.add(new_user)
    self._session.commit()
    return new_user

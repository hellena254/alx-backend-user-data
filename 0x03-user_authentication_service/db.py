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

    def find_user_by(self, **kwargs) -> User:
        """Find a user by specific attributes.

        Args:
            **kwargs: Attributes to filter by (e.g., email, id).

        Returns:
            User: The found User object.

        Raises:
            InvalidRequestError: If no filtering attributes are provided.
            NoResultFound: If no user matches the provided attributes.
        """
        if not kwargs:
            raise InvalidRequestError("No attributes provided for filtering.")

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("No user found with the provided criteria.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user details based on user ID.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Attributes to update with their new values.

        Raises:
            ValueError: If an invalid attribute is provided.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)

        self._session.commit()
        return None

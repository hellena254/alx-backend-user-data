#!/usr/bin/env python3
"""
Auth module for managing user authentication, session handling, and password reset.
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt.
    
    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new UUID.

    Returns:
        str: The generated UUID.
    """
    return str(uuid4())


class Auth:
    """
    Auth class to interact with the authentication database for user management.
    """

    def __init__(self):
        """
        Initializes the Auth instance with a database connection.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """
        Registers a new user with the provided email and password.
        
        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            Union[None, User]: Returns the created User if successful, or None if the user already exists.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
        except NoResultFound:
            # Add new user to the database
            return self._db.add_user(email, _hash_password(password))
        else:
            # User already exists
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the login credentials for the user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        try:
            # Retrieve user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        # Check if the provided password matches the stored hashed password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creates a new session for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            Union[str, None]: The session ID if successful, None if user not found.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        else:
            user.session_id = _generate_uuid()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Retrieves the user associated with the given session ID.

        Args:
            session_id (str): The session ID of the user.

        Returns:
            Union[User, None]: The user if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys the session for the user by setting the session ID to None.

        Args:
            user_id (int): The ID of the user.
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return
        else:
            user.session_id = None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates and returns a reset token for the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If no user is found with the provided email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")
        else:
            user.reset_token = _generate_uuid()
            return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the password for the user identified by the reset token.

        Args:
            reset_token (str): The reset token for the user.
            password (str): The new password for the user.

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")
        else:
            user.hashed_password = _hash_password(password)
            user.reset_token = None

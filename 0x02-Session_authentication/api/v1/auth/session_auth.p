#!/usr/bin/env python3
"""Module for Session Authentication management."""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Handles session-based authentication."""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Generates a new session ID for a given user ID and stores it.

        Args:
            user_id (str): The ID of the user for whom the session is being created.

        Returns:
            str: The generated session ID, or None if the user_id is invalid.
        """
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID associated with the session ID, or None if not found.
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Returns the User instance associated with the current session.

        Args:
            request: The request object containing the session cookie.

        Returns:
            User: The User instance corresponding to the session ID, or None if not found.
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Invalidates and removes the session associated with the current request.

        Args:
            request: The request object containing the session cookie.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except KeyError:
            return False

        return True

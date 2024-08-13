#!/usr/bin/env python3
"""
Module for handling authentication mechanisms.
"""

from typing import List, TypeVar
from flask import request
import os


class Auth:
    """
    Manages authentication processes, including path exclusion,
    authorization headers, and session cookies.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the given path requires authentication.

        Args:
            path (str): The path to be checked.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith("*") and path.startswith(excluded_path[:-1]):
                return False
            if path == excluded_path or path.startswith(excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the 'Authorization' header from the given request.

        Args:
            request (optional): The request object from which to extract the header.

        Returns:
            str: The value of the 'Authorization' header, or None if not present.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method to return the current user. To be implemented by subclasses.

        Args:
            request (optional): The request object for retrieving user information.

        Returns:
            User: The current user, if identified; None otherwise.
        """
        return None

    def session_cookie(self, request=None):
        """
        Retrieves the session cookie from the request.

        Args:
            request (optional): The request object from which to extract the session cookie.

        Returns:
            The session cookie value, or None if not present.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)

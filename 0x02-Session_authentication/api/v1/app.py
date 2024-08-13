#!/usr/bin/env python3
"""
Module for managing API authentication
"""

from flask import request
from typing import List, TypeVar
from os import getenv
import fnmatch


class Auth:
    """Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication
        """
        if path is None:
            return True
        if not excluded_paths or not isinstance(excluded_paths, list):
            return True

        # Standardize path to include a trailing slash
        path = path.rstrip('/') + '/'

        for exc_path in excluded_paths:
            # Adjust excluded paths to include a trailing slash unless it ends with '*'
            if not exc_path.endswith('*'):
                exc_path = exc_path.rstrip('/') + '/'
            if fnmatch.fnmatch(path, exc_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the Authorization header from the request
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def session_cookie(self, request=None) -> str:
        """
        Extracts the session cookie from the request
        """
        if request is None:
            return None

        # Get the session name from environment variables
        session_name = getenv('SESSION_NAME')
        if not session_name:
            return None

        # Return the cookie value associated with session_name
        return request.cookies.get(session_name)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Placeholder method to be overridden for retrieving the current user
        """
        return None

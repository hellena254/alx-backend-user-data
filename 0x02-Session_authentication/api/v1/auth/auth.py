#!/usr/bin/env python3
"""
An Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication"""
        if path is None:
            return True
        if not excluded_paths or not isinstance(excluded_paths, list):
            return True

        # Normalize the path to always have a trailing slash
        path = path.rstrip('/') + '/'

        for excl_path in excluded_paths:
            # Normalize excluded path to have a trailing slash if it doesn't have *
            excl_path = excl_path.rstrip('/') + '/' if not excl_path.endswith('*') else excl_path
            if fnmatch.fnmatch(path, excl_path):
                return False

        return True


    def authorization_header(self, request=None) -> str:
        """ Get the authorization header from the request """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user from the request """
        return None

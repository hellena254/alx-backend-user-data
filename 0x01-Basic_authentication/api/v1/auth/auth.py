#!/usr/bin/env python3
"""
An Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if the path requires authentication """
        if path is None:
            return True
        if not excluded_paths or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/') + '/'
        for ex_path in excluded_paths:
            if ex_path.rstrip('/') + '/' == path:
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

#!/usr/bin/env python3

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """BasicAuth class for managing basic authentication"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header for Basic Authentication"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]


    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes the Base64 string to return the decoded value"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header).decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))


    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        
        # Search for the user by email
        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]  # Assume email is unique, so take the first result
        if not user.is_valid_password(user_pwd):
            return None

        return user


    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None
        
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None
        
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None
        
        return self.user_object_from_credentials(user_email, user_pwd)


    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
    """Extracts the user email and password from the Base64 decoded value"""
    if decoded_base64_authorization_header is None:
        return None, None
    if not isinstance(decoded_base64_authorization_header, str):
        return None, None
    if ':' not in decoded_base64_authorization_header:
        return None, None

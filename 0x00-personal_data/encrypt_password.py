#!/usr/bin/env python3
"""
Module for hashing passwords with bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Implement a hash_password
    one string argument name password
    returns a salted, hashed password, which is a byte string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

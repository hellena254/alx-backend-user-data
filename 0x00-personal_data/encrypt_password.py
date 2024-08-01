#!/usr/bin/env python3
"""
Module for hashing passwords with bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Implement a hash_password
    Args: one string argument name password
    Returns a salted, hashed password, which is a byte string
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Implement an is_valid function
    Expects 2 arguments and returns a boolean
    Use bcrypt to validate that the provided password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

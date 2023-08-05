#!/usr/bin/env python3
""" Password-based encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hash_password: bytes, password: str) -> bool:
    """ expects 2 arguments and returns a boolean.
    """
    return bcrypt.checkpw(password.encode(), hash_password)

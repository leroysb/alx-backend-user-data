#!/usr/bin/env python3
""" Password-based encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Encrypts a password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hash_password: bytes, password: str) -> bool:
    """ Checks if a password is valid
    """
    return bcrypt.checkpw(password.encode(), hash_password)

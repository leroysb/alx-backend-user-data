#!/usr/bin/env python3
""" Password-based encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Encrypts a password
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def is_valid(hash_password: bytes, password: str) -> bool:
    """ Checks if a password is valid
    """
    if not hash_password or not password:
        return False
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except ValueError:
        return False

#!/usr/bin/env python3
""" Password-based encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Encrypts a password
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hash_password: bytes, password: str) -> bool:
    """ Checks if a password is valid
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    except Exception:
        return False

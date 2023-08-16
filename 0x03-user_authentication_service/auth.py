#!/usr/bin/env python3
""" auth module """
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ hash password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a user instance
        """
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError('User {} already exists'.format(email))
        else:
            self._db.add_user(email, _hash_password(password))
            return self._db.find_user_by(email=email)

    def valid_login(self, email: str, password: str) -> bool:
        """ valid login """
        user = self._db.find_user_by(email=email)
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        else:
            return False

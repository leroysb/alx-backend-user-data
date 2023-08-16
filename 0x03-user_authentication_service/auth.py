#!/usr/bin/env python3
""" auth module """
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """ hash password """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """ generate uuid """
    return str(uuid.uuid4())


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
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        else:
            return False

    def create_session(self, email: str) -> str:
        """ create session """
        user = self._db.find_user_by(email=email)
        if user:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        else:
            return None
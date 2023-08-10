#!/usr/bin/env python3
""" Module of API authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """ Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        Args:
            - path: path to check
            - excluded_paths: list of paths to check
        Return:
            - True if path is not in excluded_paths
            - False otherwise
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        # `*` at the end of a path means that it's a prefix
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*' and \
             path.startswith(excluded_path[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        # if request is None:
        #     return None
        # # Get the session ID from the cookie
        # session_id = self.session_cookie(request)
        # if session_id is None:
        #     return None

        # # Get the user ID associated with the session ID
        # user_id = self.user_id_for_session_id(session_id)
        # if user_id is None:
        #     return None

        # # Retrieve the User object based on the user ID
        # user = User.get(user_id)
        # return user
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request
        """
        if request is None:
            return None
        # return request.cookies.get('my_session_id')
        return request.cookies.get(getenv('SESSION_NAME'))

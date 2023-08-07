#!/usr/bin/env python3
""" Module of API authentication
"""
from flask import request
from typing import List, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64


class BasicAuth(Auth):
    """ BasicAuth class
    """
    def extract_base64_authorization_header(
     self, authorization_header: str) -> str:
        """ Extract base64 authorization header
        """
        if authorization_header is None or \
                type(authorization_header) is not str or \
                not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
     self, base64_authorization_header: str) -> str:
        """ Decode base64 authorization header
        """
        if base64_authorization_header is None or \
                type(base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
             base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
     self, decoded_base64_authorization_header: str) -> (str, str):
        """ Extract user credentials
        """
        if decoded_base64_authorization_header is None or \
                type(decoded_base64_authorization_header) is not str or \
                ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':', 1))

#!/usr/bin/env python3
""" Expiration
"""
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class
    """
    def __init__(self):
        """ Constructor
        """
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id=None):
        """ Create a session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        #
        session_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return user_id from session_id
        """
        if session_id is None:
            return None
        #
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        #
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        #
        created_at = session_dict.get("created_at")
        if created_at is None:
            return None
        #
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None
        #
        return session_dict.get("user_id")

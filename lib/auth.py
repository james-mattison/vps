from .db import DB
import os
import crypt

"""
auth.py: methods to validate usernames and passwords.
         This module is used with Flask to determine if a user is a valid user.
"""

SALT_FILE = os.environ['VPS_SALT_FILE']


class Auth(DB):
    """
    Class that compares an entered username and password combination
    to the hash stored in the database.
    """

    def __init__(self):
        super().__init__("config")
        with open(SALT_FILE, "r") as _o:
            self.salt = _o.read()

    def validate_login(self,
                       username: str,
                       password: str) -> bool:
        """
        Validatate <username> and <password> against the hash found in the database.
        Uses crypt to do so.

        Not terribly secure, but better than nothing.
        """
        hashed = self.select_where("portal_users", "password", username = username)['password']
        valid = crypt.crypt(password, self.salt)
        if valid == hashed:
            return True
        else:
            return False

    def valid_user(self,
                   username: str) -> bool:
        """
        Is <username> a valid user? If so, return True, else False
        """
        ret = self.select_where("portal_users", username = username, multi = False)
        if not ret:
            return False
        else:
            return True

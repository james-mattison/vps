from .db import DB
from flask_login import UserMixin
import os
import crypt


SALT_FILE = os.environ['VPS_SALT_FILE']

class User(UserMixin):

    def get(self, username):
        db = Auth()
        if not db.valid_user(username):
            return None
        else:
            return username


class Auth(DB):

    def __init__(self):
        super().__init__("config")
        with open(SALT_FILE, "r") as _o:
            self.salt = _o.read()

    def validate_login(self, username, password):
        hashed = self.select_where("portal_users", "password", username = username)['password']
        valid = crypt.crypt(password, self.salt)
        if valid == hashed:
            return True
        else:
            return False

    def valid_user(self, username):
        ret = self.select_where("portal_users", username = username, multi = False)
        if not ret:
            return False
        else:
            return True
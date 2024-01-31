from .db import DB
from flask_login import UserMixin

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

    def validate_login(self, username, password):
        ret = self.select_where("portal_users", email = username, password = password, multi = False)
        if not ret:
            return False
        else:
            return True

    def valid_user(self, username):
        ret = self.select_where("portal_users", email = username, multi = False)
        if not ret:
            return False
        else:
            return True
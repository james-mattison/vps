from .db import DB

class EmployeeDB(DB):

    def __init__(self):
        super().__init__("employees")
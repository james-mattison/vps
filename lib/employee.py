import logging

from .db import DB

class EmployeeDB(DB):

    def __init__(self):
        super().__init__("employees")
        logging.debug("Connected to `employees` database.")
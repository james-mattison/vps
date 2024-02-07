import logging

from .db import DB


class EmployeeDB(DB):
    """
    Class to deal with employee information for a vendor.
    """

    def __init__(self):
        super().__init__("employees")
        logging.debug("Connected to `employees` database.")

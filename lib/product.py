from .db import DB
import logging

logging.getLogger(__name__)


class ProductDB(DB):

    def __init__(self):
        super().__init__("products")
        logging.debug("Connected to `employees` database.")

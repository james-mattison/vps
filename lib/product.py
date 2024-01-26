from .db import DB

class ProductDB(DB):

    def __init__(self):
        super().__init__("employees")
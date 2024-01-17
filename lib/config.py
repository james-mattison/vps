from .db import DB

class ConfigDB(DB):

    def __init__(self):
        super().__init__("customer_config")

    def load_config(self):
        license = self.query("SELECT * FROM license")

class Config:

    def __init__(self):
        self.db = DB()

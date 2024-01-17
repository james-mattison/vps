from .db import DB


#
#insert into vendor values (69, "VPS Dev Test", "james.mattison7@gmail.com", "8185125437", "2771 Broad St", "James MAttison", 12341234, 0.0, 0.0);

class ConfigDB(DB):

    def __init__(self):
        super().__init__("config")

    def load_config(self):
        license = self.query("SELECT * FROM license")

class Config:
    def __init__(self):
        self.db = DB()

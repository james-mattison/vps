from .db import DB
import logging

logging.getLogger(__name__)

#
#insert into vendor values (69, "VPS Dev Test", "james.mattison7@gmail.com", "8185125437", "2771 Broad St", "James MAttison", 12341234, 0.0, 0.0);

class ConfigDB(DB):

    def __init__(self):
        super().__init__("config", host = "0.0.0.0")
        logging.debug("Connected to config DB")

    def load_config(self):
        license = self.query("SELECT * FROM license")

    def get_all_moduels(self):
        modules = self.query("SELECT * FROM modules;")
        return modules

    def get_enabled_modules(self):
        all_modules = self.get_all_moduels()
        enabled = []
        for item in all_modules:
            if item.get('enabled'):
                enabled.append(item)
        return enabled

    def get_vendor_name(self):
        name = self.select_where("vendor_info", "name", multi = False)
        return name

    def get_modules(self):
        modules = self.select_all("modules")
        return modules


class VPSConfig:
    def __init__(self):
        self.db = ConfigDB()
        ret = self.db.query("SELECT * FROM backend_config")
        for cfg_item in ret:
            if cfg_item['value'].isnumeric():
                if cfg_item['value'] == '0':
                    cfg_item['value'] = False
                elif cfg_item['value'] == '1':
                    cfg_item['value'] = True
                else:
                    cfg_item['value'] = int(cfg_item['value'])
            setattr(self, cfg_item['name'], cfg_item['value'])

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)



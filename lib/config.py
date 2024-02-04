from .db import DB
import logging


logging.getLogger(__name__)

#
#insert into vendor values (69, "VPS Dev Test", "james.mattison7@gmail.com", "8185125437", "2771 Broad St", "James MAttison", 12341234, 0.0, 0.0);

class ConfigDB(DB):
    """
    Methods specific to the config db.

    """
    def __init__(self):
        super().__init__("config")
        logging.debug("Connected to config DB")

    def get_license(self):
        license = self.query("SELECT * FROM license")
        return license

    def get_all_modules(self):
        """
        Return all modules available to this vendor
        """
        modules = self.query("SELECT * FROM modules;")
        return modules

    def get_enabled_modules(self):
        """
        Return only enabled modules
        """
        all_modules = self.get_all_modules()
        enabled = []
        for item in all_modules:
            if item.get('enabled'):
                enabled.append(item)
        return enabled

    def get_module_info(self, module_name: str):
        """
        Return module information gathered from the additional_info database.
        """
        module_id = None
        module_table = self.query("SELECT * FROM config.modules")
        for module in module_table:
            if module['name'] == module_name:
                module_id = module['module_id']
                break
        else:
            raise Exception(f"Searching for module: {module_name} did not return a relevant module ID!")

        module = {}
        module_info = self.query(f"SELECT * FROM additional_info.module_info where module_id = {module_id};")
        for ob in module_info:
            module['id'] = ob['module_id']
            key = ob['info_key']
            val = ob['info_value']
            module[key] = val
        return module

    def get_module_id_by_name(self, module_name):
        sql = f"SELECT module_id FROM config.modules WHERE name = '{module_name}'"
        ret = self.query(sql)
        return ret[0]['module_id']

    def module_enabled(self, module_name):
        sql = f"SELECT enabled FROM config.modules WHERE name = '{module_name}'"
        ret = self.query(sql)
        if ret[0]['enabled'] == 1:
            return True
        else:
            return False

    def disable_module(self, module_name):
        sql = f"UPDATE config.modules SET enabled = 0 WHERE name = '{module_name}'"
        self.query(sql, results = False)
        return True

    def enable_module(self, module_name):
        sql = f"UPDATE config.modules SET enabled = 1 WHERE name = '{module_name}'"
        self.query(sql, results = False)
        return True

    def get_vendor_name(self):
        """
        Get vendor name. Returns as a dict like {"name": <name>}
        """
        name = self.select_where("vendor_info", "name", multi = False)
        return name

    def get_portal_page_config(self, key_name):
        ob = self.select_where("additional_info.portal_config", target = key_name)
        return ob['value']


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



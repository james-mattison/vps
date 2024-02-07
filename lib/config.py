from .db import DB
import logging

"""
config.py:  Methods to manage the ConfigDB as well as the system config (VPSConfig)
"""

logging.getLogger(__name__)


class ConfigDB(DB):
    """
    Methods specific to the config db.
    """

    def __init__(self):
        super().__init__("config")
        logging.debug("Connected to config DB")

    def get_license(self) -> dict:
        """
        Retrieve the license information for this VPS deployment.
        """
        license = self.query("SELECT * FROM license")[0]
        return license

    def get_all_modules(self) -> list:
        """
        Return all modules available to this vendor
        """
        modules = self.query("SELECT * FROM modules;")
        return modules

    def get_enabled_modules(self) -> list:
        """
        Return only enabled modules
        """
        all_modules = self.get_all_modules()
        enabled = []
        for item in all_modules:
            if item.get('enabled'):
                enabled.append(item)
        return enabled

    def get_module_info(self,
                        module_name: str) -> dict:
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

    def get_module_id_by_name(self,
                              module_name: str) -> int:
        """
        Return the `module_id` of a given <name>'d module.
        """
        sql = f"SELECT module_id FROM config.modules WHERE name = '{module_name}'"
        ret = self.query(sql)
        return ret[0]['module_id']


    def get_module_name_by_id(self,
                              module_id: int) -> dict:
        sql = f"SELECT name FROM config.modules WHERE module_id = '{module_id}'"
        ret = self.query(sql)
        return ret[0]['name']

    def module_enabled(self,
                       module_name: str) -> bool:
        """
        Return a boolean: True if the module is enabled, and False if it is not.
        """
        sql = f"SELECT enabled FROM config.modules WHERE name = '{module_name}'"
        ret = self.query(sql)
        if ret[0]['enabled'] == 1:
            return True
        else:
            return False

    def disable_module(self,
                       module_name):
        """
        Disable a module specified by <module_name>

        Makes changes to two tables:
         - config.modules, setting enabled to 0
         - additional_info.module_info, where info_key is 'portal_tab' and the module id matches. Sets portal_tab to 0,
           removing it from the portal interface
        """
        sql = f"UPDATE config.modules SET enabled = 0 WHERE name = '{module_name}'"
        self.query(sql, results = False)

        id = self.get_module_id_by_name(module_name)

        sql = f"UPDATE additional_info.module_info SET info_value = false where info_key = 'portal_tab' AND module_id = '{id}'"
        self.query(sql, results = False)
        return True

    def enable_module(self,
                      module_name: str) -> bool:
        """
        Enable the module specified by <module_name>
        Makes changes to two tables:
        - config.modules, setting enabled to 1
        - additional_info.module_info, setting the `portal_tab` column to 1 for the specific
        __module name. This allows it to be displayed again on the portal as a tab.
        """
        sql = f"UPDATE config.modules SET enabled = 1 WHERE name = '{module_name}'"
        self.query(sql, results = False)

        id = self.get_module_id_by_name(module_name)

        sql = f"UPDATE additional_info.module_info SET info_value = true WHERE info_key = 'portal_tab' AND module_id = '{id}'"
        self.query(sql, results = False)
        return True

    def get_vendor_name(self) -> dict:
        """
        Get vendor name. Returns as a dict like {"name": <name>}
        """
        name = self.select_where("vendor_info", "name", multi = False)
        return name

    def get_portal_page_config(self,
                               key_name: str) -> str:
        """
        Select what is hopefully a single entry from the additional_info.portal_config
        table. Allows aliasing of functions inside of the portal, setting of the landing
        page, etc.
        """
        ob = self.select_where("additional_info.portal_config", target = key_name)
        return ob['value']


class VPSConfig:
    """
    Internal system configuration, taken from the `backend_config` table.

    Used to set host, port, etc for the actual flask application itself.
    """

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

    def __getitem__(self,
                    item):
        if hasattr(self, item):
            return getattr(self, item)

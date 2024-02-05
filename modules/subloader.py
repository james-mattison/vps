import importlib.util
from importlib.machinery import SourceFileLoader
import sys
import types
import os
from lib.config import ConfigDB

"""
subloader.py: A dynamic module-loading interface.

The main class, Subloader, will load all relevant modules from this same directory,
based on whether they are enabled in the `config.modules` table.

Any module that is marked enabled in the database must have a filename that matches
that module's name. For example, a module named send_email must have a corresponding
send_email.py in this directory.

Once one invokes the Subloader, ie:
`sl = Subloader()`

the modules will be populated out of the database. Each enabled module will have been
dynamically imported, based on its name.

Next, dyanmic properties are assigned to the module, based on the values found for the
module id in the `additional_info.module_info` database.
"""

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, f"{ROOT}/modules")

class Subloader:
    """
    Dynamic module loader
    """

    enabled = {}

    def __init__(self):
        self.db = ConfigDB()
        self.populate_modules()

    def populate_modules(self) -> None:
        """
        For each enabled module found in the config.modules table, enable that module, and
        load the module's __dir__ into the current context. Each loaded module is placed into the
        `enabled` array global to this class. Onyl enabled modules are added to the class.
        """

        # Gather module configuration from additional_info.module info.
        module_config = self.db.query("SELECT * FROM additional_info.module_info")

        # Get enabled modules
        modules = self.db.get_enabled_modules()


        for module in modules:
            if module['enabled']:
                # module is enabled. Load it dynamically...
                print(f"Loading {module}")

                mod = importlib.import_module(module['name'])

                # Assign the properties that are in the additional_info.module_info database
                # to the dictionary object that will represent the module....
                for thing in module_config:
                    if thing['module_id'] == module['module_id']:
                        key = thing['info_key']
                        val = thing['info_value']
                        setattr(mod, key, val)

                # Add the module to the `enabled` array for the class.
                self.enabled[module['name']] = mod

    def get_loaded_module(self, module_name: str) -> types.ModuleType:
        """
        Get the actual Module object for <module_name>
        """
        return self.enabled[module_name]

    def check_loaded(self, module_name: str) -> bool:
        """
        Is this module loaded? Return True if so, else False.
        """
        return self.enabled.get(module_name) or False

    def get_subloaded(self) -> list:
        """
        Get all modules that are currently loaded into the subloader context.
        Returns a list of dictionaries. Each dictionary is formed from the composite of
        all items selected from additional_info.module_info where the `module_id` matches.

        """
        additional_tabs = []
        additional_module_ids = self.db.query(f"SELECT module_id FROM additional_info.module_info WHERE info_key = 'portal_tab' and info_value = true;")
        if additional_module_ids:
            for ob in additional_module_ids:
                object_config = {}
                module_config = self.db.query(f"SELECT * FROM additional_info.module_info WHERE module_id = {ob['module_id']}")
                for item in module_config:
                    object_config[item['info_key']] = item['info_value']
                additional_tabs.append(object_config)
        return additional_tabs

    def unload_module(self, module_id: str):
        """
        Unload a module. Removes the module from the subloader context.
        """
        sql = f"UPDATE additional_info.module_info SET info_value = false WHERE info_key = 'portal_tab' and module_id = {module_id}"
        self.db.query(sql, results = False)

        sql = f"SELECT name from config.modules where module_id = {module_id}"
        name = self.db.query(sql)[0]['name']

        if name in self.enabled.keys():
            del self.enabled[name]
        print(f"Unloaded module {name}")

    def readd_module(self, module_id: int):
        """
        Load an unloaded, or previously loaded moduel into the subloadr context.
        Then, re-run the subloader module population
        """
        loaded_modules = self.db.get_enabled_modules()
        for loaded_module in loaded_modules:
            if loaded_module['module_id'] == module_id and loaded_module['enabled']:
                sql = f"UPDATE additional_info.module_info SET info_value = true WHERE info_key = 'portal_tab' and module_id = {module_id}"
                self.db.query(sql, results = False)
        self.populate_modules()

    def __getitem__(self, item):
        if item in self.enabled.keys():
            return self.enabled[item]
        return False

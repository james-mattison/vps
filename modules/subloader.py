import importlib.util
from importlib.machinery import SourceFileLoader
import sys
import types
import os
from lib.config import ConfigDB

ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, f"{ROOT}/modules")


class Subloader:

    enabled = {}

    def __init__(self):
        self.db = ConfigDB()

    def populate_modules(self):
        modules = self.db.get_enabled_modules()

        for module in modules:
            if module['enabled']:
                print(f"Loading {module}")
                mod = importlib.import_module(module['name'])
                self.enabled[module['name']] = mod

    def get_loaded_module(self, module):
        return self.enabled[module]

    def __getitem__(self, item):
        if item in self.enabled.keys():
            return self.enabled[item]
        return False

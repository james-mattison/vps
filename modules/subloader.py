from importlib.machinery import SourceFileLoader
import sys
import os
from lib.config import ConfigDB

ROOT = os.path.dirname(os.path.dirname(__file__))


class Subloader:

    enabled = []

    def __init__(self):
        self.db = ConfigDB()

    def populate_modules(self):
        self.enabled = []
        modules = self.db.get_modules()

        for module in modules:
            if module['enabled']:
                print(f"Loading {module}")
                SourceFileLoader(f"{ROOT}/{module['name']}", module['name'])
                self.enabled.append(module['name'])

    @staticmethod
    def get_enabled_modules():
        db = ConfigDB()
        modules = db.get_modules()
        enabled = [m for m in modules if m['enabled']]
        enabled = enabled
        return enabled

    @staticmethod
    def module_enabled(module):
        db = ConfigDB()
        modules = db.get_modules()
        for mod in modules:
            if mod['name'] == module:
                return True
        return False
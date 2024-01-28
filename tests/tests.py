import unittest
from unittest import TestCase
import requests
import sys
import os


ONE_DOWN = os.path.dirname(os.path.dirname(__file__))


sys.path.insert(0, ONE_DOWN)
from lib.db import DB
from lib.customer import CustomerDB
from lib.order import OrderDB
from lib.config import ConfigDB
import yaml

"""
tests.py: methods to test the validity of the VPS code.

Note: all methods have to start with test_
"""


class DatabaseTests(unittest.TestCase):

    def test_db_connection(self):
        print("Checking if we can connect to the database")
        empty = list()
        db = DB()

        ret = db.query("SHOW DATABASES;")

        self.assertNotEqual(empty, ret)


    def test_have_customers(self):
        print("Checking if we have customers in the customer db")
        empty = list()
        customer_db = CustomerDB()

        ret = customer_db.query("SELECT * FROM customer_info")

        self.assertNotEqual(empty, ret)

    def test_get_vendor_name(self):
        print("Checking if we can get vendor name from the config DB")
        empty = ""
        config_db = ConfigDB()

        ret = config_db.get_vendor_name()

        self.assertNotEqual(empty, ret)

    def test_docker_compose_valid(self):
        print("Checking docker-compose.yml")
        compose_file = os.path.join(ONE_DOWN, "docker-compose.yml")
        with open(compose_file, "r") as _o:
            ym = yaml.load(_o, Loader = yaml.Loader)

        self.assertTrue(ym is not None)

    def test_gitlab_ci_valid(self):
        print("Checking .gitlab-ci.yml")
        ci_file = os.path.join(ONE_DOWN, ".gitlab-ci.yml")
        with open(ci_file, "r") as _o:
            ym = yaml.load(_o, Loader = yaml.Loader)

        self.assertTrue(ym is not None)
from .db import DB
import time
import logging

"""
customer.py: methods to manage customers that are in the VPS deployment database
             This file is responsible for interactions with the `customers` database
"""

logging.getLogger(__name__)


class Customers(object):
    """
    Class representing all customers.
    """
    _customers = []

    @classmethod
    def register(cls,
                 customer):
        cls._customers.append(customer)

    @classmethod
    def customer_iter(cls):
        for customer in cls._customers:
            yield customer


class CustomerDB(DB):
    """
    Methods to manage the `customera` database.
    """

    def __init__(self):
        super().__init__("customers")

    def get_customer_names(self) -> list:
        """
        Return a list of customer names, as a list
        """
        ret = self.query("select name from customer_info")
        customer_names = [r['name'] for r in ret]
        return customer_names

    def get_customer_name_by_id(self,
                                id: int) -> str:
        ret = self.query(f"SELECT name FROM customer_info WHERE customer_id = {id}")
        return ret[0]['name']

    def get_customer_id_by_name(self,
                                name: str) -> int:
        ret = self.select_where("customer_info", "customer_id", name = name)
        return ret['customer_id']

    def insert_customer(self,
                        **kwargs
                        ) -> None:
        """
        Insert a customer into the customer DB. kwargs represent key: value
        pairings for the insert statement.
        """
        sql = "INSERT INTO customer_info ("
        for k in kwargs.keys():
            sql += f"{k}, "
        sql = sql[:-2]
        for v in kwargs.values():
            sql += f"{v}, "
        sql = sql[:-2] + ")"

        self.query(sql, results = False)

    def get_required_columns(self) -> list:
        """
        Get the column names froom the customer_info table.
        """
        table = "customer_info"

        blob = self.query(f"describe {table}")
        columns = []

        for item in blob:
            columns.append(item.get("Field"))

        return columns

    def __contains__(self,
                     item: str) -> True:
        """
        Get `item` from the customers database. Allows `x in y` interaction
        with this object
        """
        query = "SELECT * FROM customer_info"
        got = self.query(query)
        for thing in got:
            if item in thing.values():
                return True
        return False

    def select_random_customer(self):
        sql = "SELECT * from customer_info rand ORDER BY RAND() LIMIT 1"
        ret = self.query(sql)
        return ret[0]


class Customer(Customers):

    def __init__(self,
                 **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.items = kwargs
        self.db = CustomerDB()

    def insert_customer(self,
                        **kwargs):

        kwargs['customer_since'] = kwargs['customer_since'] or int(time.time())
        kwargs['total_spent'] = kwargs['total_spent'] or 0.0

        self.db.insert_row("customer_info",
                           **kwargs)

        print("Insert OK")

    def update_customer(self,
                        key,
                        value):
        """
        Update a customer setting key = value
        """
        self.db.update_value("customer_information", key, value)

    def __getitem__(self,
                    item: str) -> str or int or bool:
        if item in self.items.keys():
            return self.items[item]
        return False

    def __setitem__(self,
                    key,
                    value):
        self.db.update_value("customer_info",
                             key,
                             value,
                             customer_id = self.items['customer_id'])

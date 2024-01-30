from .db import DB
import time
import argparse
import logging

logging.getLogger(__name__)

COLUMN_MAPS = {

}


class Customers(object):
    """
    Class representing all customers.
    """
    _customers = []

    @classmethod
    def register(cls, customer):
        cls._customers.append(customer)

    @classmethod
    def customer_iter(cls):
        for customer in cls._customers:
            yield customer


class CustomerDB(DB):
    """
    Methods to manage the customer database.
    """

    def __init__(self):
        super().__init__("customers")

    def get_customer_names(self):
        return self.query("select name from customer_info")

    def get_customer_name_by_id(self, id: int):
        ret = self.query(f"SELECT name FROM customer_info WHERE customer_id = {id}")
        return ret[0]['name']

    def insert_customer(self,
                        **kwargs
                        ):


        customer = Customer(**kwargs)
        # customer = Customer(name = name, email = email, phone = phone, address = address, satisfaction_level = satisfaction_level,
        #                     customer_since = customer_since,
        #                     total_spent = total_spent,
        #                     pending_orders = pending_orders,
        #                     historical_orders = historical_orders)
        Customers.register(customer)
        self.query(f"INSERT INTO customer_information (name, email, phone, address) VALUES ('{name}', '{email}', '{phone}', '{address}');", results = False)


    def get_required_columns(self):
        table = "customer_information"

        blob = self.query(f"describe {table}")
        columns = []

        for item in blob:
            columns.append(item.get("Field"))

        return columns



    def __contains__(self, item):
        query = "SELECT * FROM customers WHERE "

        for k, v in item.__dict__.items():
            query += f"{k} = '{v}', "
        #query += ")"
        print(query[:-2])
        got = self.query(query[:-2])
        if got: return True
        else: return False

    def delete_customer_entry(self, customer_id):
        ...

    def select_random_customer(self):
        sql = "SELECT * from customer_info rand ORDER BY RAND() LIMIT 1"
        ret = self.query(sql)
        return ret[0]


class Customer(Customers):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.db = CustomerDB()
        self.insert_customer(**kwargs)

    def insert_customer(self,
                       **kwargs):

        #kwargs['satisfaction_level'] = kwargs['satisfaction_level'] or 10.0
        kwargs['customer_since'] = kwargs['customer_since'] or int(time.time())
        kwargs['total_spent'] = kwargs['total_spent'] or 0.0

        self.db.insert_row("customer_info",
                           **kwargs)

        print("Insert OK")

    def update_customer(self, key, value):
        """
        Update a customer setting key = value
        """
        self.db.update_value("customer_information", key, value)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, key):
        if not key in self.__dict__.keys():
            raise Exception(f"{key} not in {dir(self)}!")
        return self.__dict__[key]


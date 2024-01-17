from .db import DB
import time

class Customers(object):
    _customers = []

    @classmethod
    def register(cls, customer):
        cls._customers.append(customer)

    @classmethod
    def customer_iter(cls):
        for customer in cls._customers:
            yield customer


class CustomerDB(DB):

    def __init__(self):
        super().__init__("customers")

    def get_customer_names(self):
        return self.query("select name from customer_information")

    def insert_customer(self,
                        name,
                        email,
                        phone,
                        address,
                        satisfaction_level = 0,
                        customer_since = None,
                        total_spent = None,
                        pending_orders = None,
                        historical_orders = None,
                        ):

        customer = Customer(name = name, email = email, phone = phone, address = address, satisfaction_level = satisfaction_level,
                            customer_since = customer_since,
                            total_spent = total_spent,
                            pending_orders = pending_orders,
                            historical_orders = historical_orders)
        Customers.register(customer)
        self.query(f"INSERT INTO customer_information (name, email, phone, address) VALUES ('{name}', '{email}', '{phone}', '{address}');", results = False)


    def __contains__(self, item):
        query = "SELECT * FROM customers WHERE "

        for k, v in item.__dict__.items():
            query += f"{k} = '{v}', "
        #query += ")"
        print(query[:-2])
        got = self.query(query[:-2])
        if got: return True
        else: return False



class Customer(Customers):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.db = CustomerDB()
        self.insert_customer(**kwargs)

    def insert_customer(self,
                        name,
                        email,
                        phone,
                        address,
                        satisfaction_level = None,
                        customer_since = None,
                        total_spent = None,
                        pending_orders = None,
                        historical_orders = None):

        satisfaction_level = satisfaction_level or 10.0
        customer_since = customer_since or int(time.time())
        total_spent = total_spent or 0.0

        self.db.insert_row("customer_information",
                           name = name,
                           email = email,
                           phone = phone,
                           address = address,
                           satisfaction_level = satisfaction_level,
                           customer_since = customer_since,
                           total_spent = total_spent,
                           pending_orders = pending_orders,
                           historical_orders = historical_orders)

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


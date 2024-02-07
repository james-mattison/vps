from .db import DB
import logging

logging.getLogger(__name__)


class Orders:
    _orders = []

    @classmethod
    def register(cls,
                 order):
        cls._orders.append(order)


class OrderDB(DB):

    def __init__(self):
        super().__init__("orders")
        logging.debug("Connected to `orders` database.")

    def archive_order(self,
                      order_id):
        """
        Move an order from the 'pending_orders' to the
        'historical_orders' table.
        """
        order = self.select_where("pending_orders", order_id = order_id)
        logging.info(f"Moving order {order_id} to historical_orders.")
        sql = "INSERT INTO `historical_orders` ("
        for k in order.keys():
            sql += f"{k}, "
        sql = sql[:-2]
        sql += ") VALUES ("
        for v in order.values():
            sql += f"{v}, "
        sql = sql[:-2]
        sql += ")"
        logging.info(sql)
        self.query(sql, results = False)
        logging.info("...Done")


class Order(Orders):

    def __init__(self,
                 **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.db = OrderDB()

    def insert_order(self,
                     **kwargs):
        logging.info("Inserting new order for customer ID: {order['customer_id']}")
        self.db.insert_row("pending_orders", **kwargs)

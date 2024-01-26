from .db import DB

class Orders:
    _orders = []

    @classmethod
    def register(cls, order):
        cls._orders.append(order)


class OrderDB(DB):

    def __init__(self):
        super().__init__("orders")



class Order(Orders):

    def __init__(self,
                 customer_id,
                 salesperson_id,
                 vendor_id,
                 when_placed = None,
                 current_status = None,
                 recipient_status = None,
                 total_price = None,
                 total_outlay = None,
                 total_received = None,
                 shipping_price = None,
                 num_items = None,
                 description = None):

        ...

#####
##### The VPS reporting module
#####
import os
import sys
sys.path.insert(
    0, os.path.dirname(
        os.path.dirname(__file__)
    )
)

from lib.db import DB

class UsageReport:

    def __init__(self, context: str):
        self.context = context
        self.db = DB(context)

class CustomerUsageRepprt(UsageReport):

    def __init__(self):
        super().__init__("customers")

    def get_num_customers(self):
        return len(self.db.query("SELECT * FROM customer_info"))

class OrderUsageReport(UsageReport):

    def __init__(self):
        super().__init__("orders")

    def get_num_orders(self):
        return len(self.db.query("SELECT * FROM pending_orders"))

    def get_num_pending_orders(self):
        orders = self.db.query("SELECT * FROM pending_orders WHERE current_status = 'Pending';")
        return len(orders)

    def get_num_previous_orders(self):
        return len(self.db.query("SELECT * FROM historical_orders"))



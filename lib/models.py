from .db import DB

TABLE_MODELS = {
    "customers": "customer_information",
    "orders": "pending_orders",
    "employees": "employee_information",
    "products": "products"
}


class Model:
    def __init__(self, context: str):
        self.context = context
        self.table = TABLE_MODELS[self.context]
        self.db = DB(context)
        self.columns = self.db.get_columns_names(self.table)

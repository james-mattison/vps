from .db import DB
from .customer import CustomerDB
from .order import OrderDB
from .employee import EmployeeDB
from .product import ProductDB


class Model:

    def __init__(self, context: str):
        self.context = context
        self.table = TABLE_MODELS[self.context]
        self.db = DB(context)
        self.columns = self.db.get_columns_names(self.table)


class PortalModel:

    def __init__(self, labels, readonly_fields):
        self.labels = labels
        self.readonly_fields = readonly_fields

    def __getitem__(self, item):
        if item in self.labels.keys():
            return self.labels[item]

    def get_labels(self):
        return self.labels



class CustomerColumnModel(PortalModel):

    def __init__(self):
        self._labels = {
            "customer_id": "Customer ID",
            "name": "Name",
            "email": "E-Mail",
            "phone": "Phone Number",
            "address": "Street Address",
            "city": "City",
            "state": "State",
            "country_code": "Country Code",
            "customer_since": "Customer Since",
            "total_spent": "Total Spent",
            "pending_orders": "Pending Orders",
            "historical_orders": "Historical Orders"
        }

        self._readonly_fields = [
            "customer_id",
            "customer_since",
            "total_spent"
        ]
        super().__init__(self._labels, self._readonly_fields)

class ProductsColumnModel(PortalModel):

    def __init__(self):
        self._labels = {
            "product_id": "Product ID",
            "name": "Name",
            "manufacturer": "Manufacturer",
            "description": "Description",
            "unit_price": "Unit Price",
            "photograph": "Photograph",
            "price": "Total Price",
            "in_stock": "In Stock?"
        }

        self._readonly_fields = [
            "product_id"
        ]
        super().__init__(self._labels, self._readonly_fields)


class OrdersColumnModel(PortalModel):

    def __init__(self):
        self._labels = {
            "order_id": "Order ID",
            "customer_id": "Customer ID",
            "salesperson_id": "Employee ID",
            "when_placed": "When Placed?",
            "current_status": "Current Status",
            "recipient_address": "Recipient Address",
            "product_id": "Product ID",
            "product_quantity": "Quantity",
            "total_price": "Total Price",
            "total_received": "Total Received",
            "total_outlay": "Total Outlay",
            "shipping_cost": "Shipping Cost",
            "order_description": "Order Description"
        }

        self._readonly_fields = [
            "order_id"
        ]
        super().__init__(self._labels, self._readonly_fields)


class EmployeesColumnModel(PortalModel):
    def __init__(self):
        self._labels = {
            "employee_id": "Employee ID",
            "name": "Name",
            "email": "E-mail",
            "address": "Address",
            "city": "City",
            "state": "State",
            "country": "Country",
            "phone": "Phone",
            "active": "Active?",
            "satisfaction_level": "Satisfaction Level"
        }
        self._readonly_fields = [
            "employee_id",
            "satisfaction_level"
        ]
        super().__init__(self._labels, self._readonly_fields)


COLUMN_MODELS = {
    "customers": CustomerColumnModel,
    "employees": EmployeesColumnModel,
    "products": ProductsColumnModel,
    "orders": OrdersColumnModel
}

DB_MODELS = {
    "customers": CustomerDB,
    "employees": EmployeeDB,
    "products": ProductDB,
    "orders": OrderDB
}

TABLE_MODELS = {
    "customers": "customer_info",
    "orders": "pending_orders",
    "employees": "employee_information",
    "products": "product_info"
}


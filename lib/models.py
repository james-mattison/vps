from .db import DB

TABLE_MODELS = {
    "customers": "customer_info",
    "orders": "pending_orders",
    "employees": "employee_information",
    "products": "product_info"
}


class Model:
    def __init__(self, context: str):
        self.context = context
        self.table = TABLE_MODELS[self.context]
        self.db = DB(context)
        self.columns = self.db.get_columns_names(self.table)


class PortalModel:

    def __init__(self, labels):
        self.labels = labels

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
        super().__init__(self._labels)

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
        super().__init__(self._labels)


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
        super().__init__(self._labels)


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
        super().__init__(self._labels)


COLUMN_MODELS = {
    "customers": CustomerColumnModel,
    "employees": EmployeesColumnModel,
    "products": ProductsColumnModel,
    "orders": OrdersColumnModel
}


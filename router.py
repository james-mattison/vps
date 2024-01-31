#!/usr/bin/env python3

"""
router.py:
  route requests for the VPS portal
"""
import flask
from flask import url_for
import lib.models as models
from lib.config import ConfigDB
from flask_bootstrap import Bootstrap
from lib.customer import CustomerDB
from lib.config import VPSConfig
from lib.order import OrderDB
from lib.product import ProductDB
import logging
import argparse
import lib.util as util

parser = argparse.ArgumentParser()
parser.add_argument("--host", action = "store")
parser.add_argument("--port", action = "store")

logging.basicConfig(filename = "/var/log/vps.log",
                    level = logging.DEBUG,
                    datefmt = "%m-%d-%y/%H:%M:%S")

info = logging.info


def setup():
    """
    Setup the Bootstrap library
    """
    app = flask.Flask(__name__)
    info("Instantiated app")
    Bootstrap(app)
    info("Bootstrapped app...")
    return app


# app
app = setup()


#
# index - portal landing page
#
@app.route("/index")
@app.route("/", methods = ["GET"])
def index():
    """
    Return the portal landing page.

    vendor_name gets selected from the database
    """
    db = ConfigDB()
    info("Instantiated DB")
    vendor_name = db.get_vendor_name()['name']
    info(f"Selected vendor name: {vendor_name}. Rendering template")
    return flask.render_template("index.html", vendor_name = vendor_name)


#
# login - portal login page... todo: implement
#
@app.route("/login", methods = ["GET"])
def login():
    db = ConfigDB()
    info("Connected to config db...")
    name = db.select_column("vendor_info", "name", multi = False)
    info(f"Selected vendor name: {name}. Rendering template")
    return flask.render_template("login.html", vendor_name = name)


#
# Customers page
#
@app.route("/customers", methods = ["GET"])
def customers():
    """
    Return a page with a table of all customers on it.
    """

    config_db = ConfigDB()  # get vendor name
    name = config_db.get_vendor_name()['name']

    db = CustomerDB()  # connect to customer DB
    info("connected to customerDB")
    keys = db.get_columns_names("customer_info")
    info("Selected volumn names from customer_info")
    customers = db.select_all("customer_info")
    info("selected customers from customer_info")

    return flask.render_template("customers.html", keys = keys,
                                 customers = customers, vendor_name = name)


#
# Orders page
#
@app.route("/orders", methods = ["GET"])
def orders():
    order_db = OrderDB()
    conf_db = ConfigDB()
    vendor_name = conf_db.get_vendor_name()['name']
    keys = order_db.get_columns_names("pending_orders")
    orders = order_db.select_all("pending_orders")
    return flask.render_template("orders.html", keys = keys,
                                 customers = customers,
                                 vendor_name = vendor_name,
                                 orders = orders)


#
# Products page
#
@app.route("/products", methods = ["GET"])
def products():
    product_db = ProductDB()
    conf_db = ConfigDB()
    vendor_name = conf_db.get_vendor_name()
    keys = product_db.get_columns_names("product_info")
    products = product_db.select_all("product_info")
    next_id = product_db.get_next_key_incrementation()

    return flask.render_template("products.html", keys = keys,
                                 customers = customers,
                                 vendor_name = vendor_name,
                                 products = products)


#
# Modules page
#
@app.route("/modules", methods = ["GET"])
def modules():
    config_db = ConfigDB()
    modules = config_db.get_all_modules()
    vendor_name = config_db.get_vendor_name()['name']

    return flask.render_template("modules.html",
                                 vendor_name = vendor_name,
                                 modules = modules)


#
# About page
#
@app.route("/about")
def about():
    config_db = ConfigDB()
    vendor_name = config_db.get_vendor_name()['name']
    version = config_db.select_all_by_key("backend_config", "name", "version")[0]['value']
    license = config_db.select_all("license")[0]
    license['expiration'] = util.unixtime_to_string(license['expiration'])
    return flask.render_template("about.html", vendor_name = vendor_name, version = version, license = license)


#
# Add <customer|order|product|employee>
#
@app.route("/<context>/add", methods = ["GET", "POST"])
def add(context):
    """
    Valid contexts:
    - orders
    - customer
    - employees
    - product
    The above return add.html, used to both add and edit entries in the above dbs.

    - modules (note, handled separately)
    If the <context> is modules, then returns modules-add.html
    """
    if context == "modules":
        info(f"Got context to add modules!")
        return flask.render_template("modules-add.html")

    if not context in models.TABLE_MODELS.keys():
        return f"Failed - {context} not in {models.TABLE_MODELS.keys()}"

    customer_db = CustomerDB()
    customer_dict = customer_db.select_column("customer_info", "name")
    customer_names = [c['name'] for c in customer_dict]
    config_db = ConfigDB()
    vendor_name = config_db.get_vendor_name()['name']
    info(f"Adding {context}...")
    title = "Add " + context.capitalize()
    model = models.Model(context)
    columns = models.COLUMN_MODELS[context]()
    labels = columns.get_labels()
    next_id = model.db.get_next_key_incrementation()
    action = "add"
    info(f"Customer_names: {customer_names}, labels: {labels}")

    return flask.render_template('add.html',
                                 context = context,
                                 action = action,
                                 title = title,
                                 labels = labels,
                                 values = None,
                                 customer_names = customer_names,
                                 vendor_name = vendor_name,
                                 next_id = next_id)


#
# Special function for add/modules
#
def add_modules():
    return flask.render_template("modules-add.html")


#
# Submit data into the canonical databases. Return to the root.
#
@app.route("/submit", methods = ["POST"])
def submit():
    """
    Submit entries added by the <context>/add endpoint into the database.
    """
    form_items = flask.request.form
    logging.debug(form_items)

    action = form_items['action']
    context = form_items['context']
    id = form_items['id']

    filtered_form = {
        k: v for k, v in form_items.items() if not \
            k in ['id', 'action', 'context']
    }

    info(f"Received form with {len(filtered_form.keys())} keys")
    model = models.COLUMN_MODELS[context]()
    table_target = models.TABLE_MODELS[context]
    database_target = models.DB_MODELS[context]()
    table_columns = model.get_labels()

    info(f"Loaded {len(table_columns)} columns from table {models.COLUMN_MODELS[context]}")
    id_target = list(table_columns.keys())[0]  # customer_id, order_id, etc

    success_info = ""

    if action == "add":
        database_target.insert_row(table_target, **filtered_form)
        success_info = f"Success! Added {context} to database."
    elif action == "modify":
        database_target.update_row(table_target, id_target, id, **filtered_form)
        success_info = f"Success! Updated {context} ID {id_target}."
    else:
        success_info = f"Failed! Bad {context} or {id_target} - was not able to make changes to database!"

    info(success_info)
    return flask.render_template("success.html",
                                 success_info = success_info,
                                 context = context
                                 )


#
# Modify content in any of the canonical databases. Return to root.
#
@app.route("/<context>/modify/<id>", methods = ["GET", "POST"])
def modify(context, id):
    """
    Contextually modify any of the following databases:
    - orders
    - products
    - customers
    - employees

    Uses a form and a modification of the add.html template
    """
    if not context in models.TABLE_MODELS.keys():
        return f"Failed - {context} not in {models.Model.TABLE_MODELS.keys()}"

    info(f"Modifying {context} ID {id}")
    db = models.DB_MODELS[context]()
    model = models.Model(context)
    columns = models.COLUMN_MODELS[context]()
    labels = columns.get_labels()
    cols = labels.values()

    id_col = list(labels.keys())[0]
    id_kwargs = {id_col: id}
    selected = db.select_where(models.TABLE_MODELS[context], **id_kwargs)
    if "name" in selected.keys():
        title = "Modify " + context.capitalize() + ": " + selected['name']
    else:
        title = "Modify " + context.capitalize() + ": ID: " + id
    action = "modify"

    info(f"{labels.keys()} in {columns.readonly_fields}")
    return flask.render_template("add.html",
                                 id = id,
                                 action = action,
                                 title = title,
                                 context = context,
                                 labels = labels,
                                 readonly_fields = columns.readonly_fields,
                                 values = selected)


#
# Delete rows from database
#
@app.route("/<context>/delete/<id>", methods = ["GET", "POST"])
def delete(context, id):
    """
    Delete an entry from any of the following databases, by its primary key:
    - orders
    - products
    - customers
    - employees

    """
    config_db = ConfigDB()
    vendor_name = config_db.get_vendor_name()['name']
    db = models.DB_MODELS[context]()
    model = models.COLUMN_MODELS[context]()
    table = models.TABLE_MODELS[context]

    labels = model.get_labels()
    id_col = list(labels.keys())[0]
    id_kwargs = {id_col: id}
    db.delete_row(table, **id_kwargs)

    success_info = f"Deleted {context} from {context} DB."

    return flask.render_template("success.html",
                                 context = context,
                                 success_info = success_info)


if __name__ == "__main__":
    args = parser.parse_args()
    vps_config = VPSConfig()
    host = args.host or vps_config['host']
    port = args.port or vps_config['port']
    app.run(host = host, port = port)

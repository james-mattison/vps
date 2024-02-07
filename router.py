#!/usr/bin/env python3

"""
router.py:
    Script that routes requests received by the portal.
"""
import flask
from flask import url_for, session
import lib.models as models
from lib.auth import Auth
from lib.config import ConfigDB
from flask_bootstrap import Bootstrap
from lib.customer import CustomerDB
from lib.config import VPSConfig
from lib.order import OrderDB
from lib.product import ProductDB
from modules.subloader import Subloader
import time
import os
import logging
import argparse
import lib.util as util

parser = argparse.ArgumentParser()
parser.add_argument("--host", action = "store")
parser.add_argument("--port", action = "store")

logging.basicConfig(filename = "/var/log/vps.log",
                    level = logging.DEBUG   ,
                    datefmt = "%m-%d-%y/%H:%M:%S")

info = logging.info

def setup():
    """
    Set up the Bootstrap library
    """
    app = flask.Flask(__name__)
    info("Instantiated app")
    Bootstrap(app)
    info("Bootstrapped app...")
    return app


# subloader
subloader = Subloader()
# app
app = setup()
app.secret_key = os.environ['SECRET_KEY']
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

    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")

    db = ConfigDB()

    # load the landing page used in the index
    landing_page = db.get_portal_page_config('landing_page')
    vendor_name = db.get_vendor_name()['name']
    subloaded_modules = subloader.get_subloaded()
    return flask.render_template("index.html",
                                 vendor_name = vendor_name,
                                 landing_page = landing_page,
                                 session = session,
                                 subloaded_modules = subloaded_modules)

#
# logout - portal loguout
#
@app.route("/logout", methods = ["GET"])
def logout():
    """
    Clear a session, and log the user out.
    """
    app.logger.info(f"Clearing session for {session.get('id')} ({session.get('ip')}) logged in at: {session.get('when')}")
    session['loggedin'] = False
    session.pop('id', None)
    session.pop('when', None)
    session.pop('ip', None)


    return flask.render_template("success.html", context = "login", success_info = "Logged out successfully.")


#
# login - portal login page... todo: implement
#
@app.route("/login", methods = ["GET", "POST"])
def login():
    """
    Log in a user.

    If method is GET, then return the login page.
    If method is POST, then validate the username/password combination given.
       If it is acceptable, then start a session for this user.
    """
    db = ConfigDB()
    app.logger.info("Connected to config db...")
    name = db.select_column("vendor_info", "name", multi = False)
    app.logger.info(f"Selected vendor name: {name}. Rendering template")
    subloaded_modules = subloader.get_subloaded()

    # POST - means we got an attempt to log into the system
    if flask.request.method == "POST":
        form = flask.request.form
        auth = Auth()
        valid = auth.validate_login(form['username'], form['password'])
        if valid:
            session['loggedin'] = True
            session['id'] = form['username']
            session['ip'] = flask.request.remote_addr
            session['when'] = util.unixtime_to_string(str(int(time.time())))
            return flask.render_template("success.html",
                                         context = "index",
                                         vendor_name = name,
                                         success_info = f"Logged in {form['username']}",
                                         session = session,
                                         subloaded_modules = subloaded_modules)
        else:
            # Bad username / password
            return flask.render_template("login.html",
                                         vendor_name =
                                         name)
    else:
        # GET request; someone going to the login page.
        return flask.render_template("login.html",
                                     vendor_name = name)


#
# Customers page
#
@app.route("/customers", methods = ["GET"])
def customers():
    """
    Return a page with a table of all customers on it, with a context menu for
    each customer.
    """
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")

    config_db = ConfigDB()  # get vendor name
    name = config_db.get_vendor_name()['name']

    db = CustomerDB()  # connect to customer DB
    model = models.COLUMN_MODELS['customers']()
    labels = model.get_labels()
    info("connected to customerDB")
    keys = db.get_columns_names("customer_info")
    info("Selected volumn names from customer_info")
    customers = db.select_all("customer_info")
    info("selected customers from customer_info")

    subloaded_modules = subloader.get_subloaded()

    return flask.render_template("customers.html",
                                 keys = keys,
                                 labels = labels,
                                 customers = customers,
                                 vendor_name = name,
                                 session = session,
                                 subloaded_modules = subloaded_modules)


#
# Orders page
#
@app.route("/orders", methods = ["GET"])
def orders():
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
    order_db = OrderDB()
    conf_db = ConfigDB()
    model = models.COLUMN_MODELS["orders"]()
    labels = model.get_labels()
    vendor_name = conf_db.get_vendor_name()['name']
    keys = order_db.get_columns_names("pending_orders")
    orders = order_db.select_all("pending_orders")

    subloaded_modules = subloader.get_subloaded()
    return flask.render_template("orders.html",
                                 keys = keys,
                                 labels = labels,
                                 customers = customers,
                                 vendor_name = vendor_name,
                                 orders = orders,
                                 session = session,
                                 subloaded_modules = subloaded_modules)


#
# Products page
#
@app.route("/products", methods = ["GET"])
def products():
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
    product_db = ProductDB()
    conf_db = ConfigDB()
    vendor_name = conf_db.get_vendor_name()['name']
    keys = product_db.get_columns_names("product_info")
    products = product_db.select_all("product_info")
    next_id = product_db.get_next_key_incrementation()

    subloaded_modules = subloader.get_subloaded()

    return flask.render_template("products.html", keys = keys,
                                 customers = customers,
                                 vendor_name = vendor_name,
                                 products = products,
                                 session = session,
                                 subloaded_modules = subloaded_modules)


#
# Modules page
#
@app.route("/modules", methods = ["GET"])
def modules():
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
    config_db = ConfigDB()
    modules = config_db.get_all_modules()
    vendor_name = config_db.get_vendor_name()['name']
    subloader.populate_modules()
    subloaded_modules = subloader.get_subloaded()
    return flask.render_template("modules.html",
                                 vendor_name = vendor_name,
                                 modules = modules,
                                 session = session,
                                 subloaded_modules = subloaded_modules)


#
# About page
#
@app.route("/about")
def about():
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
    config_db = ConfigDB()
    vendor_name = config_db.get_vendor_name()['name']
    version = config_db.select_all_by_key("backend_config", "name", "version")[0]['value']
    license = config_db.select_all("license")
    license['expiration'] = util.unixtime_to_string(license['expiration'])

    subloaded_modules = subloader.get_subloaded()

    return flask.render_template("about.html",
                                 vendor_name = vendor_name,
                                 version = version,
                                 license = license,
                                 session = session,
                                 subloaded_modules = subloaded_modules)

#
# enable modules action
#
@app.route("/disable/<module_name>", methods = ["GET", "POST"])
def disable(module_name):
    config_db = ConfigDB()
    enabled = config_db.get_enabled_modules()
    module_id = config_db.get_module_id_by_name(module_name)
    if module_id is None:
        return flask.render_template("success.html",
                                     context = "modules",
                                     success_info = f"Failed - module {module_name} does not exist.",
                                     redirect_target = "login page")

    subloader.unload_module(module_id)
    config_db.disable_module(module_name)
    subloader.get_subloaded()
    return flask.render_template("success.html",
                                 context = "modules",
                                 success_info = f"Disabled module {module_name}",
                                 redirect_target = "modules"
                                 )


#
# disable modules action
#
@app.route("/enable/<module_name>", methods = ["GET", "POST"])
def enable(module_name):
    config_db = ConfigDB()
    if not config_db.module_enabled(module_name):
        config_db.enable_module(module_name)

    module_id = config_db.get_module_id_by_name(module_name)

    if module_id is None:
        return flask.render_template("success.html",
                                     context = "modules",
                                     success_info = f"FAILED: cannot re-enable {module_name} - doesn't exists!",
                                     redirect_target = "modules"
                                     )

    for loaded in subloader.get_subloaded():
        if subloader.check_loaded(module_name):
            subloader.readd_module(module_id)
            return flask.render_template("success.html",
                                 context = "modules",
                                 success_info = f"Enabled module {module_name}",
                                 redirect_target = "modules"
                                 )
    return  flask.render_template("success.html",
                                 context = "modules",
                                 success_info = f"FAILED: cannot re-enable {module_name} - already enabled!",
                                 redirect_target = "modules"
                                 )

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


    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
    if context == "modules":
        info(f"Got context to add modules!")
        return flask.render_template("modules-add.html", session = session)

    if not context in models.TABLE_MODELS.keys():
        return f"Failed - {context} not in {models.TABLE_MODELS.keys()}"

    customer_db = CustomerDB()
    customer_names = customer_db.get_customer_names()
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
    subloaded_modules = subloader.get_subloaded()

    return flask.render_template('add.html',
                                 context = context,
                                 action = action,
                                 title = title,
                                 labels = labels,
                                 values = None,
                                 customer_names = customer_names,
                                 vendor_name = vendor_name,
                                 next_id = next_id,
                                 session = session,
                                 subloaded_modules = subloaded_modules)


#
# Special function for add/modules
#
def add_modules():
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
    return flask.render_template("modules-add.html", session = session)


#
# Submit data into the canonical databases. Return to the root.
#
@app.route("/submit", methods = ["POST"])
def submit():
    """
    Submit entries added by the <context>/add endpoint into the database.
    """
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
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
                                 context = context,
                                 session = session
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
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
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
                                 values = selected,
                                 session = session)


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
    if not session.get('id'):
        return flask.render_template("success.html",
                                     context = "login",
                                     success_info = "Failed - not logged in",
                                     redirect_target = "login page")
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
                                 success_info = success_info,
                                 session = session)


#
# <module>/<module_name>
#
@app.route("/module/<module_name>", methods = ["GET", "POST"])
def module(module_name):
    loaded = subloader.enabled.get(module_name)
    template = subloader[module_name].PortalTemplate()
    rendered = template.render(module = loaded)


    if not loaded:
        return None

    return flask.render_template("module.html", module = loaded)


if __name__ == "__main__":
    args = parser.parse_args()
    vps_config = VPSConfig()
    host = args.host or vps_config['host']
    port = args.port or vps_config['port']
    app.run(host = host, port = port)

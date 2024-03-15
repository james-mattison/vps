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

logging.basicConfig(level = logging.DEBUG,
                    datefmt = "%m-%d-%y/%H:%M:%S",
                    handlers = [
                        logging.FileHandler("/var/log/vps.log"),
                        logging.StreamHandler()
                        ]
                    )

logging.info("---- VPS APP LOADING ----")


def setup():
    """
    Set up the Bootstrap library
    """
    app = flask.Flask(__name__)
    logging.info("Instantiated app")
    Bootstrap(app)
    logging.info("Bootstrapped app...")
    return app


# subloader
subloader = Subloader()

# app
app = setup()

# configure logging
info = logging.info

# required for session object
app.secret_key = os.environ['SECRET_KEY']


def get_required_kwargs(*excludes) -> dict:
    """
    Return a dictionary of the kwargs that are required for nearly every function
    used in this script.
     - vendor_name
     - subloaded_modules
     - session
    """
    config_db = ConfigDB()
    subloader.populate_modules()
    subloaded_modules = subloader.get_subloaded()
    kw = {
        "vendor_name": config_db.get_vendor_name(),
        "session": session,
        "subloaded_modules": subloaded_modules
    }
    if excludes:
        for exclude in excludes:
            if exclude in kw.keys():
                del kw[exclude]

    return kw


#
# DECORATOR: Check if the user has logged into a session.
#
def check_logged_in(f):
    """
    Decorator function. Determines if the user is logged into the VPS system.
    If not, kicks them back to the login page.

    This decorator _must_ be called before the @app.route.
    """

    def _inner_render(*args,
                      **kwargs):
        """
        Return either the failed login page....
        """
        for k, v in session.items():
            print(k, v)
            info("{:20} {:20}".format(k, v))
        if not session.get('id'):
            return flask.make_response(flask.render_template("success.html",
                                                             context = "login",
                                                             success_info = "Failed - not logged in",
                                                             redirect_target = "login page"),
                                       200
                                       )
        # ... or the pag ethe user was going to, routed with @app.route BELOW this decorator.
        else:
            return flask.make_response(f(*args, **kwargs))

    return _inner_render


#
# index - portal landing page
#
@check_logged_in
@app.route("/index")
@app.route("/", methods = ["GET"])
def index():
    """
    Return the portal landing page.

    vendor_name gets selected from the database
    """
    # if not session.get('id'):
    #     return flask.render_template("success.html",
    #                                  context = "login",
    #                                  success_info = "Failed - not logged in",
    #                                  redirect_target = "login page")

    db = ConfigDB()

    # load the landing page used in the index
    landing_page = db.get_portal_page_config('landing_page')
    return flask.render_template("index.html",
                                 landing_page = landing_page,
                                 **get_required_kwargs())


#
# logout - portal loguout
#
@app.route("/logout", methods = ["GET"])
def logout():
    """
    Clear a session, and log the user out.
    """
    app.logger.info(
        f"Clearing session for {session.get('id')} ({session.get('ip')}) logged in at: {session.get('when')}")
    session['loggedin'] = False
    session.pop('id', None)
    session.pop('when', None)
    session.pop('ip', None)

    flask.flash("Logged out succesfully")
    return flask.render_template("success.html", context = "login", success_info = "Logged out successfully.")


#
# login - Portal login page
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
        if valid is not False:
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
@check_logged_in
@app.route("/customers", methods = ["GET"])
def customers():
    """
    Return a page with a table of all customers on it, with a context menu for
    each customer.
    """
    db = CustomerDB()  # connect to customer DB
    model = models.COLUMN_MODELS['customers']()
    labels = model.get_labels()
    info("connected to customerDB")
    keys = db.get_columns_names("customer_info")
    info("Selected volumn names from customer_info")
    customers = db.select_all("customer_info")
    info("selected customers from customer_info")

    return flask.render_template("customers.html",
                                 keys = keys,
                                 labels = labels,
                                 customers = customers,
                                 **get_required_kwargs()
                                 )


#
# Orders page
#
@check_logged_in
@app.route("/orders", methods = ["GET"])
def orders():
    order_db = OrderDB()
    model = models.COLUMN_MODELS["orders"]()
    labels = model.get_labels()
    keys = order_db.get_columns_names("pending_orders")
    orders = order_db.select_all("pending_orders")

    return flask.render_template("orders.html",
                                 keys = keys,
                                 labels = labels,
                                 customers = customers,
                                 orders = orders,
                                 **get_required_kwargs()
                                 )


#
# Products page
#
@check_logged_in
@app.route("/products", methods = ["GET"])
def products():
    product_db = ProductDB()
    keys = product_db.get_columns_names("product_info")
    products = product_db.select_all("product_info")
    return flask.render_template("products.html", keys = keys,
                                 customers = customers,
                                 products = products,
                                 **get_required_kwargs()
                                 )


#
# Modules page
#
@check_logged_in
@app.route("/modules", methods = ["GET"])
def modules():
    config_db = ConfigDB()
    modules = config_db.get_all_modules()
    subloader.populate_modules()
    return flask.render_template("modules.html",
                                 modules = modules,
                                 **get_required_kwargs()
                                 )


#
# About page
#
@check_logged_in
@app.route("/about")
def about():
    """
    TODO: Fix so that license does not need to be license[0]
    """
    config_db = ConfigDB()
    version = config_db.select_all_by_key("backend_config", "name", "version")[0]['value']
    license = config_db.select_all("license")
    license[0]['expiration'] = util.unixtime_to_string(license[0]['expiration'])

    return flask.render_template("about.html",
                                 version = version,
                                 license = license[0],
                                 **get_required_kwargs()
                                 )


#
# enable modules action
#
@check_logged_in
@app.route("/disable/<module_name>", methods = ["GET", "POST"])
def disable(module_name):
    config_db = ConfigDB()
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
@check_logged_in
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

    return flask.render_template("success.html",
                                 context = "modules",
                                 success_info = f"Enabled {module_name}",
                                 redirect_target = "modules"
                                 )


@check_logged_in
@app.route("/users", methods = ["GET"])
def users():
    db = ConfigDB()
    users = db.select_all("portal_users")
    for i, user in enumerate(users):
        users[i]['privilege_str'] = models.USER_PRIVILEGES[int(user['privilege_level'])]
    return flask.render_template("users.html", users = users, **get_required_kwargs())
#
# Add <customer|order|product|employee>
#
@check_logged_in
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
        return flask.render_template("modules-add.html", session = session)

    if not context in models.TABLE_MODELS.keys():
        return f"Failed - {context} not in {models.TABLE_MODELS.keys()}"

    customer_db = CustomerDB()
    customer_names = customer_db.get_customer_names()
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
                                 next_id = next_id,
                                 **get_required_kwargs()
                                 )


#
# Submit data into the canonical databases. Return to the root.
#
@check_logged_in
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
    # TODO: This is a really shitty and nonportable way of doing this.
    # TODO: REFACTOR
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
@check_logged_in
@app.route("/<context>/modify/<id>", methods = ["GET", "POST"])
def modify(context,
           id):
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
    columns = models.COLUMN_MODELS[context]()
    labels = columns.get_labels()

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
                                 **get_required_kwargs()
                                 )


#
# Delete rows from database
#
@check_logged_in
@app.route("/<context>/delete/<id>", methods = ["GET", "POST"])
def delete(context,
           id):
    """
    Delete an entry from any of the following databases, by its primary key:
    - orders
    - products
    - customers
    - employees
    """
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
                                 **get_required_kwargs())


#
# <module>/<module_name>
#
@check_logged_in
@app.route("/module/<module_name>", defaults = {"action": None}, methods = ["GET"])
@app.route("/module/<module_name>/<action>", methods = ["POST"])
# This is WRONG todo: figure out wny its getting passed the whole module
# Todo: module_name is a dict here and that is breaking everything
def module(module_name,
           action):
    config_db = ConfigDB()
    customer_db = CustomerDB()
    customer_names = customer_db.get_customer_names()
    subloaded_modules = subloader.get_subloaded()
    subloaded_module = None
    for module in subloaded_modules:
        if module['name'] == module_name:
            subloaded_module = module
            break
    else:
        raise Exception(f"Subloaded {module_name} not found in {subloaded_modules}")

    print(flask.request.method)
    if flask.request.method == "GET":
        if subloaded_module.get('template'):
            target = subloaded_module['template']
        else:
            target = "module.html"
        return flask.render_template(target,
                                     subloaded_modules = subloaded_modules,
                                     subloaded_module = subloaded_module,
                                     customer_names = customer_names,
                                     **get_required_kwargs("subloaded_modules"))
    elif flask.request.method == "POST":
        if action == "enable":
            config_db.enable_module(module_name)
            return flask.render_template("success.html",
                                         success_info = f"Enabled {module_name}",
                                         context = "modules",
                                         subloaded_modules = subloaded_modules
                                         )
        elif action == "disable":
            config_db.disable_module(module_name)
            return flask.render_template("success.html",
                                         success_info = f"Disabled {module_name}",
                                         context = "modules",
                                         subloaded_modules = subloaded_modules
                                         )
        else:
            if action == None:
                return flask.render_template("module.html",
                                             subloaded_modules = subloaded_modules,
                                             subloaded_module = subloaded_module)

    else:
        return "Broken as heck"


if __name__ == "__main__":
    args = parser.parse_args()
    vps_config = VPSConfig()
    host = args.host or vps_config['host']
    port = args.port or vps_config['port']
    app.run(host = host, port = 443, ssl_context = ('passthru/ssl/cert.pem', 'passthru/ssl/key.pem'))

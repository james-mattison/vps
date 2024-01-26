import flask
from flask import url_for
from lib.db import DB
import lib.models as models
from lib.config import ConfigDB
from flask_bootstrap import Bootstrap
from lib.customer import CustomerDB
import logging

logging.basicConfig(filename = "/var/log/vps.log", level = logging.DEBUG)

info = logging.info

def setup():
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
# login - portal login page... todo
#
@app.route("/login", methods = ["GET"])
def login():
    db = ConfigDB()
    info("Connected to config db...")
    name = db.select_column("vendor", "name", multi = False)
    info(f"Selected vendor name: {name}. Rendering template")
    return flask.render_template("login.html", vendor_name = name)


#
# Customers page
#
@app.route("/customers", methods = ["GET", "POST"])
def customers():
    config_db = ConfigDB()
    name = config_db.select_column("vendor", "name", False)
    db = CustomerDB()
    info("connected to customerDB")
    keys = db.get_columns_names("customer_info")
    info("Selected volumn names from customer_info")
    customers = db.select_all("customer_info")
    info("selected customers from customer_info")
    return flask.render_template("customers.html", keys = keys,
                                 customers = customers, vendor_name = name)


#
# Add <customer|order|product|employee>
#
@app.route("/<context>/add", methods = ["GET", "POST"])
def add(context):
    if not context in models.Model.TABLE_MODELS.keys():
        return f"Failed - {context} not in {models.Model.TABLE_MODELS.keys()}"
    title = "Add " + context.capitalize()
    model = models.Model(context)
    columns = models.COLUMN_MODELS[context]()
    labels = columns.get_labels()
    action = "add"

    return flask.render_template('add.html',
                                 context = context,
                                 action= action,
                                 title = title,
                                 labels = labels,
                                 values = None)

@app.route("/submit", methods = ["POST"])
def submit():
    form_items = flask.request.form

    action = form_items.pop("action")
    context = form_items.pop("context")
    id = form_items.pop("id")

    table_target = models.Model.TABLE_MODELS[context]
    database_target = models.DB_MODELS[context]()
    table_columns = database_target.get_labels()
    id_target = list(table_columns.keys())[0] # customer_id, order_id, etc


    if action == "add":
        database_target.db.insert_row(table_target, **form_items)
    elif action == "modify":
        database_target.db.update_row(table_target, id_target, id, **form_items)



    st = str(form_items)
    return st
@app.route("/<context>/modify/<id>", methods = ["GET", "POST"])
def modify(context, id):
    if not context in models.Model.TABLE_MODELS.keys():
        return f"Failed - {context} not in {models.Model.TABLE_MODELS.keys()}"
    db = models.DB_MODELS[context]()
    model = models.Model(context)
    columns = models.COLUMN_MODELS[context]()
    labels = columns.get_labels()
    cols = labels.values()


    id_col = list(labels.keys())[0]
    id_kwargs = {id_col: id}
    selected = db.select_where(model.TABLE_MODELS[context], **id_kwargs)
    if "name" in selected.keys():
        title = "Modify " + context.capitalize() + ": " + selected['name']
    else:
        title = "Modify " + context.capitalize() + ": ID: " + id
    action = "modify"
    return flask.render_template("add.html",
                                 id = id,
                                 action = action,
                                 title = title,
                                 context = context,
                                 labels = labels,
                                 values = selected)


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)

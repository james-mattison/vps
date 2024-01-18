import flask
from lib.config import ConfigDB
from flask_bootstrap import Bootstrap
from lib.customer import CustomerDB

def setup():
    app = flask.Flask(__name__)
    Bootstrap(app)
    return app

# app
app = setup()

# Logging
info = app.logger.info

@app.route("/", methods = ["GET"])
def index():
    db = ConfigDB()
    info("Instantiated DB")
    vendor_name = db.select_column("vendor", "name", multi = False)
    info(f"Selected vendor name: {vendor_name}. Rendering template")
    return flask.render_template("index.html", vendor_name = vendor_name)


@app.route("/login", methods = ["GET"])
def login():
    db = ConfigDB()
    info("Connected to config db...")
    name = db.select_column("vendor", "name", multi = False)
    info(f"Selected vendor name: {name}. Rendering template")
    return flask.render_template("login.html", vendor_name = name)


@app.route("/customers", methods = ["GET", "POST"])
def customers():
    if flask.request.method == "GET":
        db = CustomerDB()
        info("connected to customerDB")
        keys = db.get_columns_names("customer_information")
        info("Selected volumn names from customer_information")
        customers = db.select_all("customer_information")
        info("selected customers from customer_information")
        return flask.render_template("customers.html", keys = keys,
                                     customers = customers)
    elif flask.request.method == "POST":
        for key, val in flask.request.form.items():
            print(key, val)




if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8080)
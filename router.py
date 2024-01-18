import flask
from lib.config import ConfigDB
from flask_bootstrap import Bootstrap
from lib.customer import CustomerDB

def setup():
    app = flask.Flask(__name__)
    Bootstrap(app)
    return app

app = setup()

@app.route("/", methods = ["GET"])
def index():
    db = ConfigDB()
    vendor_name = db.select_column("vendor", "name", multi = False)
    return flask.render_template("index.html", vendor_name = vendor_name)


@app.route("/login", methods = ["GET"])
def login():
    db = ConfigDB()
    name = db.select_column("vendor", "name", multi = False)
    return flask.render_template("login.html", vendor_name = name)


@app.route("/customers", methods = ["GET"])
def customers():
    db = CustomerDB()
    keys = db.get_columns_names("customer_information")
    customers = db.select_all("customer_information")
    return flask.render_template("customers.html", keys = keys,
                                 customers = customers)




if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
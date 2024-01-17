import flask
from lib.config import ConfigDB
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

def setup():
    app = flask.Flask(__name__)
    Bootstrap(app)
    LoginManager(app)
    return app

app = setup()

@app.route("/", methods = ["GET"])
@app.route("/login", methods = ["GET"])
def index():
    db = ConfigDB()
    name = db.select_column("vendor", "name", multi = False)
    return flask.render_template("login.html", vendor_name = name)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
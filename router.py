import flask


app = flask.Flask(__name__)

@app.route("/", methods = ["GET"])
def index():
    return "WOW IT WORKS"

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80)
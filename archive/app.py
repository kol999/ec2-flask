import flask
import hostinfo

app = flask.Flask(__name__)


@app.route("/")
def home():
    return flask.render_template("home.html", hostinfo=hostinfo.get_info())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

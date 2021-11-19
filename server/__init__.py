import flask

f_app = flask.Flask(__name__)


@f_app.route("/index",methods=["GET","POST"])
def upload():
    files = flask.request.files
    return "ok"


if __name__ == '__main__':
    f_app.run()
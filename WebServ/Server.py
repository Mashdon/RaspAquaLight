from flask import *
from WebController import C_WebController
app = Flask(__name__)


def start_app(_debug=False):
    app.debug = 1 if _debug else 0
    app.run(host="0.0.0.0")


@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


@app.route('/StartTest', methods=['POST'])
def start_test():
    return ""


@app.errorhandler(404)
def page_not_found(error):
    response = make_response("404", 404)
    return response


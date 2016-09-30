from flask import Flask, request, make_response

app = Flask(__name__)


def start_app():
    app.debug = 1
    app.run()


@app.route('/', methods=['GET'])
def home():
    return "Home Page " + request.path


@app.route('/test', methods=['POST'])
def test():
    return home()


@app.errorhandler(404)
def page_not_found(error):
    response = make_response("Tu sembles perdu...", 404)
    return response


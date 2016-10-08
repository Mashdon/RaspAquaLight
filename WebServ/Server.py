from flask import *
from WebController import C_WebController
app = Flask(__name__)


def start_app(_debug=False):
    app.debug = 1 if _debug else 0
    app.run(host="0.0.0.0")


@app.route('/', methods=['GET'])
def home():
    phases = get_all_phases()
    return render_template("home.html", phases=phases)


@app.route('/StartTest', methods=['POST'])
def start_test():
    #TODO action
    return ""


@app.route('/GetAllPhases', methods=['GET'])
def get_all_phases():
    phases = ""
    for i in xrange(1, 5):
        phases += get_phase(i)
    return phases


@app.route('/GetNewPhase/<int:_num_phase>', methods=['GET'])
def get_new_phase(_num_phase):
    return get_phase(_num_phase, fetch=False)


def get_phase(_num_phase, fetch=True):
    #TODO fetch informations

    return render_template("phase.html", num_phase=_num_phase)


@app.errorhandler(404)
def page_not_found(error):
    response = make_response("404", 404)
    return response


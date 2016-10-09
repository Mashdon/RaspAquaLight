from flask import *
from WebController import C_WebController
app = Flask(__name__)


def start_app(_debug=False):
    app.debug = 1 if _debug else 0
    app.run(host="0.0.0.0")


@app.route('/', methods=['GET'])
def home():
    phases = get_all_phases()
    return render_template("home.html", phases=phases, colorManual=[0, 0, 0], isManual=False)


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


@app.route('/SetManual', methods=['POST'])
def set_manual():
    isManual = request.form.get("isManual")

    if isManual:
        _r = request.form.get("r")
        _g = request.form.get("g")
        _b = request.form.get("b")
    return ""


@app.route('/SavePhases', methods=['POST'])
def save_phases():
    return ""




def get_phase(_num_phase, fetch=True):
    #TODO fetch informations

    return render_template("phase.html", num_phase=_num_phase)


@app.errorhandler(404)
def page_not_found(error):
    response = make_response("404", 404)
    return response


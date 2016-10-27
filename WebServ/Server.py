# -*- coding: utf-8 -*-
from flask import *
from Model import C_Model, Phase
import json
app = Flask(__name__)

model = C_Model.getInstance()

def start_app(_debug=False):
    app.debug = 1 if _debug else 0
    app.run(host="0.0.0.0")

@app.route('/', methods=['GET'])
def home():
    phases = get_all_phases()
    colorManual = model.getColorManual()
    isManual = model.getIsManual()
    return render_template("home.html", phases=phases, colorManual=colorManual, isManual=isManual)



@app.route('/StartTest', methods=['POST'])
def start_test():
    duration = int(request.form.get("duration"))
    model.startTest(duration)
    return ""


@app.route('/GetAllPhases', methods=['GET'])
def get_all_phases():
    dataPhases = model.getPhases()

    html_phases = ""
    for p in dataPhases:
        html_phases += get_html_phase(p)
    return html_phases


@app.route('/GetNewPhase/<int:_num_phase>', methods=['GET'])
def get_new_phase(_num_phase):
    phase = Phase(_num_phase)
    return get_html_phase(phase)


@app.route('/SetManual', methods=['POST'])
def set_manual():
    isManual = (request.form.get("isManual") == "true")

    rgb = (int(request.form.get("r")), int(request.form.get("g")), int(request.form.get("b")))

    model.setManual(isManual, rgb)

    return ""


@app.route('/SavePhases', methods=['POST'])
def save_phases():
    nbPhases = int(request.form.get("nbPhases"))
    phases = [request.form.getlist("phases[" + str(i) + "][]") for i in xrange(nbPhases)]
    model.savePhases(phases)
    return ""


def get_html_phase(phase):
    return render_template("phase.html", phase=phase)


@app.errorhandler(404)
def page_not_found(error):
    response = make_response("404", 404)
    return response


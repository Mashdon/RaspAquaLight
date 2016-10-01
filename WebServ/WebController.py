try:
    import cPickle as pickle
except:
    import pickle

import WebModel



instance_WebController = None


def getInstance():
    global instance_WebController
    if instance_WebController is None:
        instance_WebController = C_WebController()
    return instance_WebController

class C_WebController:

    def __init__(self):
        self.model = WebModel.C_WebModel()
        self.model.load()



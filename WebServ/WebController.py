try:
    import cPickle as pickle
except:
    import pickle

import WebModel


class WebController:

    def __init__(self):
        self.model = WebModel.WebModel()
        self.model.load()

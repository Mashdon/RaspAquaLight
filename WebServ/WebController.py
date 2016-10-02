from WebModel import C_WebModel
from threading import RLock


class C_WebController:
    instance_WebController = None

    locker = RLock()

    @staticmethod
    def getInstance():
        with C_WebController.locker:

            C_WebController.instance_WebController
            if C_WebController.instance_WebController is None:
                C_WebController.instance_WebController = C_WebController()
            return C_WebController.instance_WebController

    def __init__(self):
        self.model = C_WebModel()
        self.model.load()






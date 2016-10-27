from threading import RLock

from Model import C_Model


class C_WebController:
    instance_WebController = None

    locker = RLock()

    @staticmethod
    def getInstance():
        with C_WebController.locker:
            if C_WebController.instance_WebController is None:
                C_WebController.instance_WebController = C_WebController()
            return C_WebController.instance_WebController

    def __init__(self):
        self.model = C_Model.getInstance()






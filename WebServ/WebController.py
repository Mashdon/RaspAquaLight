from WebModel import C_WebModel


class C_WebController:
    instance_WebController = None

    @staticmethod
    def getInstance():
        C_WebController.instance_WebController
        if C_WebController.instance_WebController is None:
            C_WebController.instance_WebController = C_WebController()
        return C_WebController.instance_WebController

    def __init__(self):
        self.model = C_WebModel()
        self.model.load()





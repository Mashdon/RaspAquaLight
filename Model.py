import cPickle as pickle
from threading import RLock
import datetime
from copy import deepcopy


class Phase:

    def __init__(self, _num=0):
        self.num = _num
        self.time = datetime.time(hour=_num, minute=0, second=0)
        self.color = [0, 0, 0]
        self.name = ""


class C_Model:

    modelFilename = "Data/Model.data"
    locker = RLock()
    instance_Model = None

    @staticmethod
    def getInstance():
        with C_Model.locker:
            if C_Model.instance_Model is None:
                C_Model.instance_Model = C_Model()
            C_Model.instance_Model.load()
            return C_Model.instance_Model

    def __init__(self):
        self.colorProgram = [Phase(1), Phase(2), Phase(3)]
        self.isManual = False
        self.colorManual = [0, 0, 0]
        self.isTest = False
        self.needSave = False

    ############################################################################

    def load(self):
        with C_Model.locker:
            try:
                f = open(self.modelFilename, 'rb')
                tmp_dict = pickle.load(f)
                f.close()
                self.__dict__.update(tmp_dict)
            except IOError:
                self.save()

    def save(self):
        with C_Model.locker:
            f = open(self.modelFilename, 'wb')
            pickle.dump(self.__dict__, f, 2)
            f.close()
            self.needSave = False

    ############################################################################

    def getRGBToDisplay(self):
        with C_Model.locker:
            if self.isManual:
                colorToSend = deepcopy(self.colorManual)

            elif self.isTest:
                raise NotImplementedError()

            else:
                raise NotImplementedError()

        return colorToSend


    ##############################################################################

    def sendSafe(self, obj):
        with C_Model.locker:
            toSend = deepcopy(obj)
        return toSend

    def getPhases(self):
        return self.sendSafe(self.colorProgram)

    def getColorManual(self):
        return self.sendSafe(self.colorManual)

    def getIsManual(self):
        return self.sendSafe(self.isManual)

    def setManual(self, _isManual, _colorManual):
        with C_Model.locker:
            self.isManual = deepcopy(_isManual)
            self.colorManual = deepcopy(_colorManual)
            self.needSave = True

    def savePhases(self, _phases):
        #TODO traiter
        return""

    def startTest(self, _duration):
        #TODO traiter
        return ""


import cPickle
from threading import RLock
import datetime
from copy import deepcopy


class Phase:

    def __init__(self, _num=0):
        self.num = _num
        self.time = datetime.time(hour=0, minute=0, second=0)
        self.color = (0, 0, 0)
        self.name = ""


def minute_interval(start, end):
    reverse = False
    if start > end:
        start, end = end, start
        reverse = True

    delta = (end.hour - start.hour) * 60 + end.minute - start.minute + (end.second - start.second) / 60.0
    if reverse:
        delta = 1440 - delta  # 1440 = 60 * 24
    return delta


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
        self.isManual = True
        self.colorManual = (0, 0, 0)
        self.isTest = False
        self.needSave = False

    ############################################################################

    def load(self):
        with C_Model.locker:
            try:
                f = open(self.modelFilename, 'rb')
                tmp_dict = cPickle.load(f)
                f.close()
                self.__dict__.update(tmp_dict)
            except IOError:
                self.save()

    def save(self):
        with C_Model.locker:
            f = open(self.modelFilename, 'wb')
            cPickle.dump(self.__dict__, f, 2)
            f.close()
            self.needSave = False

    ############################################################################

    def getRGBToDisplay(self):
        # if nothing correct show 0
        colorToSend = (0, 0, 0)

        with C_Model.locker:
            if self.isManual:
                colorToSend = deepcopy(self.colorManual)

            elif self.isTest:
                print "Not implemented !"

            else:
                currentTime = datetime.datetime.now().time()
                for i in xrange(len(self.colorProgram)):
                    iNext = 0 if i == len(self.colorProgram) - 1 else i + 1
                    if self.colorProgram[i].time < currentTime <= self.colorProgram[iNext].time \
                            or currentTime <= self.colorProgram[iNext].time < self.colorProgram[i].time :

                        deltaTimePhase = minute_interval(self.colorProgram[i].time, self.colorProgram[iNext].time)
                        deltaTimeCurrent = minute_interval(self.colorProgram[i].time, currentTime)

                        percentageDone = deltaTimeCurrent / float(deltaTimePhase)

                        currentColor = tuple(int(x + (y - x) * percentageDone) for x, y in zip(self.colorProgram[i].color, self.colorProgram[iNext].color))
                        colorToSend = deepcopy(currentColor)
                        break

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
        phases = []
        for i, p in enumerate(_phases):
            newP = Phase(i + 1)
            newP.name = str(p[0])
            try:
                newP.time = datetime.datetime.strptime(p[1], '%H:%M').time()
            except ValueError:
                newP.time = datetime.datetime.strptime(p[1], '%H:%M:%S').time()
            newP.color = (int(p[2]), int(p[3]), int(p[4]))
            phases.append(newP)

        with C_Model.locker:
            self.colorProgram = deepcopy(tuple(phases))



    def startTest(self, _duration):
        #TODO traiter
        return ""




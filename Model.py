# -*- coding: utf-8 -*-
import cPickle
from threading import RLock
import datetime
from copy import deepcopy
import os


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

    delta = (end.hour - start.hour) * 60 \
        + end.minute - start.minute \
        + (end.second - start.second) / 60.0 \
        + (end.microsecond - start.microsecond) / (60 * 1e6)

    # 1440 = 60 * 24
    return 1440 - delta if reverse else delta

refreshBase = 1
refreshTest = 0.05

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
        self.colorManual = (0, 0, 0)
        self.needSave = False
        self.isTest = False
        self.durationTest = 0
        self.beginTest = None
        self.refreshRate = refreshBase

    ############################################################################

    def load(self):
        with C_Model.locker:
            try:
                f = open(self.modelFilename, 'rb')
                tmp_dict = cPickle.load(f)
                f.close()
                self.__dict__.update(tmp_dict)
                self.needSave = False
            except IOError:
                if not os.path.exists("Data"):
                    os.makedirs("Data")
                self.save()

    def save(self):
        with C_Model.locker:
            f = open(self.modelFilename, 'wb')
            cPickle.dump(self.__dict__, f, 2)
            f.close()
            self.needSave = False
        print "*** File Saved"

    ############################################################################

    def getRGBToDisplay(self):
        # if nothing correct show 0
        colorToSend = (0, 0, 0)

        with C_Model.locker:
            if self.isManual:
                colorToSend = deepcopy(self.colorManual)

            else:
                currentTimeToDisplay = datetime.datetime.now().time()

                if self.isTest:
                    progress = minute_interval(self.beginTest, currentTimeToDisplay)
                    globalPercentage = progress / self.durationTest
                    if globalPercentage >= 1:
                        self.stopTest()
                    else:

                        newTimeSeconds = int(globalPercentage * 86400)  # 86400 seconds in 24h

                        newTimeMinutes = int(newTimeSeconds / 60)
                        newTimeHours = int(newTimeMinutes / 60)

                        newTimeSeconds = int(newTimeSeconds % 60)
                        newTimeMinutes = int(newTimeMinutes % 60)

                        currentTimeToDisplay = datetime.time(hour=newTimeHours, minute=newTimeMinutes, second=newTimeSeconds)

                for i in xrange(len(self.colorProgram)):
                    iNext = 0 if i == len(self.colorProgram) - 1 else i + 1
                    if self.colorProgram[i].time < currentTimeToDisplay <= self.colorProgram[iNext].time \
                            or currentTimeToDisplay <= self.colorProgram[iNext].time < self.colorProgram[i].time \
                            or self.colorProgram[iNext].time < self.colorProgram[i].time <= currentTimeToDisplay:

                        deltaTimePhase = minute_interval(self.colorProgram[i].time, self.colorProgram[iNext].time)
                        deltaTimeCurrent = minute_interval(self.colorProgram[i].time, currentTimeToDisplay)


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

    def getRefreshRate(self):
        return self.sendSafe(self.refreshRate)

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
            newP.name = str(p[0].encode("utf-8"))
            try:
                newP.time = datetime.datetime.strptime(p[1], '%H:%M').time()
            except ValueError:
                newP.time = datetime.datetime.strptime(p[1], '%H:%M:%S').time()
            newP.color = (int(p[2]), int(p[3]), int(p[4]))
            phases.append(newP)

        with C_Model.locker:
            self.colorProgram = deepcopy(tuple(phases))
            self.needSave = True

    def startTest(self, _duration):
        with C_Model.locker:
            self.durationTest = (_duration / 60.0) + 1e-5  # in minutes
            self.beginTest = datetime.datetime.now().time()
            self.refreshRate = refreshTest
            self.isTest = True


    def stopTest(self):
        with C_Model.locker:
            self.refreshRate = refreshBase
            self.isTest = False






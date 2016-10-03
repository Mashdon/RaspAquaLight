import cPickle as pickle
import datetime


class C_WebModel:

    modelFilename = "Data/WebModel.data"

    def __init__(self):
        self.switchOn = False
        self.mode = 0
        self.colorProgram = [[datetime.time(hour=11, minute=30, second=0), [0, 0, 0]],
                             [datetime.time(hour=12, minute=0, second=0), [255, 255, 255]],
                             [datetime.time(hour=22, minute=0, second=0), [255, 255, 255]],
                             [datetime.time(hour=22, minute=30, second=0), [0, 0, 0]]]
        self.colorManual = [0, 0, 0]




    ############################################################################

    def load(self):
        try:
            f = open(self.modelFilename, 'rb')
            tmp_dict = pickle.load(f)
            f.close()
            self.__dict__.update(tmp_dict)
        except IOError:
            self.save()

    def save(self):
        f = open(self.modelFilename, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()

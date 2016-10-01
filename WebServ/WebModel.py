try:
    import cPickle as pickle
except:
    import pickle


class C_WebModel:

    modelFilename = "Data/WebModel.data"



    def __init__(self):
        self.switchOn = False





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

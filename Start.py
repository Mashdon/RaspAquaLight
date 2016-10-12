from WebServ import Server
from WebServ.WebController import C_WebController
from Model import C_Model
from threading import Thread
from time import sleep
import os

role_web = 0
role_led = 1
role_save = 2

class C_Launcher(Thread):

    def __init__(self, _role):
        Thread.__init__(self)
        self.role = _role

    def run(self):
        if self.role == role_web:
            self.StartWeb()
        elif self.role == role_led:
            self.StartLED()
        else:
            self.SaveModel()

    def StartWeb(self):
        Server.start_app(_debug=False)

    def StartLED(self):
        print "Nothing to do for the moment :o"

    def SaveModel(self):
        model = C_Model.getInstance()
        while True:
            sleep(25)
            if model.needSave:
                model.save()

if __name__ == "__main__":
    if not os.path.exists("Data"):
        os.makedirs("Data")

    controller = C_WebController.getInstance()

    ThreadWeb = C_Launcher(role_web)
    ThreadLED = C_Launcher(role_led)
    ThreadSave = C_Launcher(role_save)

    ThreadWeb.start()
    ThreadLED.start()
    ThreadSave.start()

    ThreadWeb.join()
    ThreadLED.join()
    ThreadSave.join()




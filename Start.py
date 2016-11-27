# -*- coding: utf-8 -*-
from WebServ import Server
from WebServ.WebController import C_WebController
from Model import C_Model
from threading import Thread
from time import sleep
import os


if os.name == "nt":
    prod = False
else:
    prod = True

role_web = 0
role_led = 1
role_save = 2

pin_R = 17
pin_G = 22
pin_B = 24



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
        model = C_Model.getInstance()
        while True:
            timeToSleep = model.getRefreshRate()
            sleep(timeToSleep)
            color = model.getRGBToDisplay()

            if prod:
                cmd = "echo '" + str(pin_R) + "=" + str(color[0]) + "' > /dev/pi-blaster;"
                cmd += "echo '" + str(pin_G) + "=" + str(color[1]) + "' > /dev/pi-blaster;"
                cmd += "echo '" + str(pin_B) + "=" + str(color[2]) + "' > /dev/pi-blaster;"
                os.system(cmd)
            else:
                #print "Color Displayed : " + str(color)
                pass



    def SaveModel(self):
        model = C_Model.getInstance()
        while True:
            sleep(25)
            if model.needSave:
                model.save()

if __name__ == "__main__":

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







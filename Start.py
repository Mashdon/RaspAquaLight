# -*- coding: utf-8 -*-
from WebServ import Server
from WebServ.WebController import C_WebController
from Model import C_Model
from threading import Thread
from time import sleep


try:
    import pigpio
    print " ******************* In Production !"
    prod = True

except ImportError:
    print " ******************* Dev-only"
    prod = False

role_web = 0
role_led = 1
role_save = 2

pin_R = 17
pin_G = 22
pin_B = 24



class C_Launcher(Thread):

    def __init__(self, _role, _pi=None):
        Thread.__init__(self)
        self.role = _role
        self.pi = _pi

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
                self.pi.set_PWM_dutycycle(pin_R, color[0])
                self.pi.set_PWM_dutycycle(pin_G, color[1])
                self.pi.set_PWM_dutycycle(pin_B, color[2])
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

    pi = pigpio.pi() if prod else None

    ThreadWeb = C_Launcher(role_web)
    ThreadLED = C_Launcher(role_led, pi)
    ThreadSave = C_Launcher(role_save)

    ThreadWeb.start()
    ThreadLED.start()
    ThreadSave.start()

    ThreadWeb.join()
    ThreadLED.join()
    ThreadSave.join()







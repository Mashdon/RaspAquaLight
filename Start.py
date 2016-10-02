from WebServ import Server
from WebServ.WebController import C_WebController
import os
import time


if __name__ == "__main__":
    if not os.path.exists("Data"):
        os.makedirs("Data")

    controller = C_WebController.getInstance()
    Server.start_app()

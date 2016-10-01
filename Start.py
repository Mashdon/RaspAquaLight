import WebServ.Server
import WebServ.WebController
import os

if __name__ == "__main__":
    if not os.path.exists("Data"):
        os.makedirs("Data")

    controller = WebServ.WebController.C_WebController()
    WebServ.Server.start_app()

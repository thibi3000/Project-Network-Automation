
import os
import json
import vagrant
from resources.globalscripts.clearscreen import clearScreen

class VagrantBoxManagement:

    def __init__(self):

        self.header = " - Configured Vagrant boxes - "
        self.error = ""

        self.mainpath = os.getcwd()
        self.serverdatabase = os.path.join("resources", "database", "database.json")
        self.allinteractiveboxes = os.path.join("resources", "database", "vagrant", "interactive")

    def show_menu(self):


        clearScreen()
        print(self.header)
        print(self.error)

        with open(self.serverdatabase, "r") as serverdatabase:

            data = json.load(serverdatabase)

            if len(data["vagrantboxes"]) == 0:

                print("No boxes have been configured (yet).")
                return

            else:

                for box in data["vagrantboxes"]:

                    path = box["location"]
                    name = box["name"]

                    boxpath = os.path.join(os.getcwd(), path)
                    os.chdir(boxpath)

                    v = vagrant.Vagrant(root=os.getcwd())
                    status = v.status()[0]

                    print(f"Name: {name}")
                    print(f"Status: {status.state}")
                    print(f"Provider: {status.provider}")
                    print("-------------------------------")
                    os.chdir(self.mainpath)

                while True:

                    print("Please input machine name and action.\nFor example: boxname-[start, suspend, stop, resume, destroy]")

                    choice = input("")

        return

    
    def start_box(self):

        pass 

    def suspend_box(self):

        pass

    def stop_box(self):

        pass

    def resume_box(self):

        pass

    def destroy_box(self):

        pass




        


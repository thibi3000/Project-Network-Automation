
import os
import json
import vagrant
from resources.globalscripts.clearscreen import clearScreen

class VagrantBoxManagement:

    def __init__(self):

        self.header = " - Configured Vagrant boxes - "
        self.error = ""

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

                """for box in data["vagrantboxes"]:

                    
                    path = box["location"]
                    boxpath = os.path.join(os.getcwd(), path)
                    os.chdir(boxpath)
                    print(os.getcwd())
                    v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
                    print()
                    """
        return




        


import vagrant
import os
import ipaddress
import requests
import json
import inspect
from resources.globalscripts.clearscreen import clearScreen
from shutil import copyfile

class PredefinedVagrantBox:

    def __init__(self):

        #self.serverdatabase = os.path.join("resources", "database", "database.json")
        self.allpredefinedvagrantfiles = os.path.join("resources", "database", "vagrant", "predefined")
        self.predefinedboxlocation = None

        self.mainpath = os.getcwd()

        self.header = " - Create Vagrant Box (predefined) - "
        self.error = ""

    def move_vagrantfile(self, type):

        clearScreen()
                
        print(self.header)
        print(self.error)

        try:

            self.predefinedboxlocation = input(f"You have chosen a {type} installation. Please specify the path: ")
            
            
            if os.path.exists(self.predefinedboxlocation):

                print("Folder has been found!")

                if os.path.isfile(os.path.join(self.predefinedboxlocation, "Vagrantfile")):

                    while True:

                        choice = input("There is already a Vagrantfile in this location. Do you want to replace it? (y|n)")

                        if choice in ["y", "n"]:

                            if choice == "y":

                                os.remove(os.path.join(self.predefinedboxlocation, "Vagrantfile"))
                                break

                            else:

                                return

                        else:

                            print("Please pick a valid option!")

            else:

                os.mkdir(self.predefinedboxlocation)
                print("Succesfully created this directory!")
                
            
            self.vagrantfile = os.path.join("resources", "database", "vagrant", "predefined", f"Vagrant{type}")

            

            copyfile(self.vagrantfile, os.path.join(self.predefinedboxlocation, "Vagrantfile"))

            if type == "windows":

                self.windowsprovisionfile = os.path.join("resources", "database", "vagrant", "predefined", "windowsprovision.ps1")
                copyfile(self.windowsprovisionfile, os.path.join(self.predefinedboxlocation, "windowsprovision.ps1"))

            
            
            print(f"Succesfully copied Vagrantfile to {self.predefinedboxlocation} ")
        
        except Exception as e:

            print(e)



import os
import json
import vagrant
import time
from resources.globalscripts.clearscreen import clearScreen
from shutil import rmtree

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

                    v = vagrant.Vagrant(root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)
                    status = v.status()[0]

                    print(f"Name: {name}")
                    print(f"Status: {status.state}")
                    print(f"Provider: {status.provider}")
                    print("-------------------------------")
                    os.chdir(self.mainpath)

                serverdatabase.close()

                while True:

                    try:

                        print("Please input machine name and action.\nFor example: boxname-[start, suspend, halt, destroy]")

                        choice = input("")
                        valid = False
                        for box in data["vagrantboxes"]:

                            if choice.split("-")[0] == box["name"] and choice.split("-")[1] in ["start","suspend","halt","destroy"]:

                                valid = True
                                action = choice.split("-")[1]
                                validbox = box

                        if valid:
                            
                            if action == "start":
                                
                                self.start_box(validbox)
                                os.chdir(self.mainpath)

                            elif action == "suspend":
                                
                                self.suspend_box(validbox)
                                os.chdir(self.mainpath)

                            elif action == "halt":

                                self.halt_box(validbox)
                                os.chdir(self.mainpath)

                            elif action == "destroy":

                                self.destroy_box(validbox)
                                
                                os.chdir(self.mainpath)

                                rmtree(validbox["location"])
                            
                        else:

                            raise ValueError("Wrong format!")

                    except ValueError as e:

                        print(e)
        return  

    
    def start_box(self, box):
        
        path = os.path.join(os.getcwd(), box["location"])
        os.chdir(path)
        start = vagrant.Vagrant(root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)
        
        start.up()
        
    def halt_box(self, box):

        path = os.path.join(os.getcwd(), box["location"])
        os.chdir(path)
        start = vagrant.Vagrant(root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)
        
        start.halt()

    def suspend_box(self, box):

        path = os.path.join(os.getcwd(), box["location"])
        os.chdir(path)
        start = vagrant.Vagrant(root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)
        
        start.suspend()

    def destroy_box(self, box):

        path = os.path.join(os.getcwd(), box["location"])
        os.chdir(path)
        start = vagrant.Vagrant(root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)
        test = start.halt()
        
        test2 = start.destroy()
        

        '''print("Please wait a few seconds...")
        time.sleep(60)'''

        '''kill_virtualbox_related_proceses()'''
        '''kill_virtualbox_related_services()'''
        
        os.chdir(self.mainpath)

        with open(self.serverdatabase, 'r') as serverdatabase:
            data = json.load(serverdatabase)

            serverdatabase.close()

        for element in data["vagrantboxes"]:

            if element["name"] == box["name"]:

                data["vagrantboxes"].remove(element)

        with open(self.serverdatabase, 'w') as serverdatabase:
            data = json.dump(data, serverdatabase)

            serverdatabase.close()



        


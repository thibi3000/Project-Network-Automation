
import os
import json
import vagrant
import inspect
import sys
from resources.globalscripts.clearscreen import clearScreen
from shutil import rmtree


class VagrantBoxManagement:

    def __init__(self):
        """ Constructor

            Attributes: 

                header (str) : Contains the name of the current option
                serverdatabase (str) : Location of the json database
                mainpath (str) : Location where main.py gets executed
                allinteractiveboxes (str) : Location of all the created Vagrant boxes.
        """

        self.header = " - Configured Vagrant boxes - "

        self.mainpath = os.getcwd()
        self.serverdatabase = os.path.join(
            "resources", "database", "database.json")
        self.allinteractiveboxes = os.path.join(
            "resources", "database", "vagrant", "interactive")

    def show_menu(self):
        """ Method: This method will clear your screen and show you all interactive Vagrant boxes that have been created.
            It will show the name, status and provider of the box.

            You get the option to change the state of certain box (halt, suspend, start, destroy)

        """

        clearScreen()
        print(self.header)
        print("")

        try:

            with open(self.serverdatabase, "r") as serverdatabase:

                data = json.load(serverdatabase)

                if len(data["vagrantboxes"]) == 0:

                    serverdatabase.close()

                    print(inspect.cleandoc(f"""

                            No boxes have been configured (yet).
                            """))

                    choice = input("Press Enter to return to the menu.")

                    if choice == "":

                        return

                    else:

                        raise ValueError

                else:

                    for box in data["vagrantboxes"]:

                        path = box["location"]
                        name = box["name"]

                        boxpath = os.path.join(os.getcwd(), path)
                        os.chdir(boxpath)

                        v = vagrant.Vagrant(
                            root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)
                        status = v.status()[0]

                        print(inspect.cleandoc(f"""

                        Name: {name}
                        Status: {status.state}
                        Provider: {status.provider}
                        -------------------------------
                        """))

                        os.chdir(self.mainpath)

                    serverdatabase.close()

        except Exception as e:

            sys.exit(f"Error: {e}!")

        while True:

            try:

                print(inspect.cleandoc(f"""

                Please input the machine named, followed by the action.
                For example: boxname-[start, suspend, halt, destroy]
                
                To leave this menu please enter 'q'.

                """))

                choice = input("")

                if choice.lower() == "q":

                    return

                valid = False
                for box in data["vagrantboxes"]:

                    if choice.split("-")[0] == box["name"] and choice.split("-")[1] in ["start", "suspend", "halt", "destroy"]:

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

                    raise ValueError("Error: Wrong format!")

            except ValueError as e:

                print(e)
                continue

            except Exception as e:

                sys.exit(f"Error: {e}")

    def start_box(self, box):
        """ Method: Used to start a Vagrant box.

        """

        clearScreen()

        try:

            path = os.path.join(os.getcwd(), box["location"])
            os.chdir(path)
            start = vagrant.Vagrant(
                root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)

            start.up()

            return

        except Exception as e:

            print(f"Error: {e}")
            return

    def halt_box(self, box):
        """ Method: Used to halt a Vagrant box.

        """

        clearScreen()

        try:

            path = os.path.join(os.getcwd(), box["location"])
            os.chdir(path)
            start = vagrant.Vagrant(
                root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)

            start.halt()

            return

        except Exception as e:

            print(f"Error: {e}")
            return

    def suspend_box(self, box):
        """ Method: Used to suspend a Vagrant box.

        """

        clearScreen()

        try:

            path = os.path.join(os.getcwd(), box["location"])
            os.chdir(path)
            start = vagrant.Vagrant(
                root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)

            start.suspend()

            return

        except Exception as e:

            print(f"Error: {e}")
            return

    def destroy_box(self, box):
        """ Method: Used to destroy a Vagrant box.

        """

        clearScreen()

        try:

            path = os.path.join(os.getcwd(), box["location"])
            os.chdir(path)
            start = vagrant.Vagrant(
                root=os.getcwd(), quiet_stdout=False, quiet_stderr=False)
            test = start.halt()

            test2 = start.destroy()

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

            return

        except Exception as e:

            print(f"Error: {e}")
            return

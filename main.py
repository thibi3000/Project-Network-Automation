import inspect
from resources.servers.scripts.serverregistration import ServerRegistration
from resources.vagrant.scripts.vagrantboxcreation import InteractiveVagrantBox
from resources.vagrant.scripts.vagrantboxmanagement import VagrantBoxManagement
from resources.servers.scripts.interactiveconnection import InteractiveConnection
from resources.vagrant.scripts.predefinedvagrantbox import PredefinedVagrantBox
from resources.globalscripts.clearscreen import clearScreen

class MainMenu:

    
    def __init__(self):

        """ Constructor: We don't need any attributes in this class (for now). """
        
        self.header = " - Project Network Automation 1 - "
        self.error = ""

    def show_menu(self):

        """ Method: This method will clear your screen, start an endless loop, show you a list of options
            and will keep running untill you enter a certain option.
            Depending on your choice it will create a new class object from another script or exit.

            1, 2, 3, 4, 5, 6 -> Valid options

            6 will exit the script.

            Any other input will raise a Valuerror and clear your screen.
        """

        

        while True:

            try:

                clearScreen()
                
                print(inspect.cleandoc(f"""
                        {self.header}
                        {self.error}
                        Select one of the following options:
                        1) Register server
                        2) Vagrant box management
                        3) Remote execution
                        4) Remote hosts monitoring
                        5) Setup predefined Vagrant box
                        6) Quit
                        """))

                choice = int(input("Enter your choice: "))
                
                if choice not in range(1,6) or choice == "":

                    if choice == 6:
                        
                        clearScreen()

                        exit("Bye!")

                    else:
                
                        raise ValueError
                
                else:

                    if choice == 1:

                        serverreg = ServerRegistration()
                        serverreg.register_server()
                    
                    elif choice == 2:

                        vagrantboxmanagementsubmenu = VagrantBoxManagementSubMenu()
                        vagrantboxmanagementsubmenu.show_menu()

                    elif choice == 3:
                        
                        interactiveconnectionsubmenu = InteractiveConnectionSubMenu()
                        interactiveconnectionsubmenu.show_menu()

                    elif choice == 5:

                        vagrantpredefinedsubmenu = VagrantPredefinedSubMenu()
                        vagrantpredefinedsubmenu.show_menu()

            except ValueError:

                clearScreen()
                self.error = "* Error: Please enter a valid option!"




class VagrantBoxManagementSubMenu():

    def __init__(self):

        self.header = " - Vagrant Box Management - "
        self.error = ""

    def show_menu(self):

        while True:

            #clearScreen()

            try:

                print(inspect.cleandoc(f"""
                        {self.header}
                        {self.error}
                        Select one of the following options:
                        1) Create Vagrant box (interactive)
                        2) Manage existing boxes
                        3) Return to main menu
                        """))
                
                choice = int(input("Enter your choice: "))
                
                if choice not in [1,2] or choice == "":

                    if choice == 3:
                        
                        return

                    else:
                
                        raise ValueError
                
                else:

                    if choice == 1:

                        interactivevagrantbox = InteractiveVagrantBox()
                        interactivevagrantbox.ask_for_options()
                        interactivevagrantbox.create_interactive_box()
                        
                        
                    elif choice == 2:
                        
                        vagrantboxmanagement = VagrantBoxManagement()
                        vagrantboxmanagement.show_menu()
                        

            except ValueError:

                clearScreen()
                self.error = "* Error: Please enter a valid option!"  
                         

class InteractiveConnectionSubMenu():

    def __init__(self):

        self.header = " - Remote Execution of Scripts/Commands On Servers - "
        self.error = ""

    def show_menu(self):

        while True:

            clearScreen()

            try:

                print(inspect.cleandoc(f"""
                        {self.header}
                        {self.error}
                        Select one of the following options:
                        1) Interactive connection
                        2) Run remote script
                        3) Return to main menu
                        """))

                choice = int(input("Enter your choice: "))

                if choice not in [1, 2] or choice == "":

                    if choice == 3:

                        return

                    else:

                        raise ValueError

                else:

                    if choice == 1:

                        interactiveconnection = InteractiveConnection()
                        interactiveconnection.ask_options()
                        interactiveconnection.connect_to_server()

                    elif choice == 2:

                        interactiveconnection = InteractiveConnection()
                        interactiveconnection.ask_options()
                        interactiveconnection.send_script()


            except ValueError:

                clearScreen()
                self.error = "* Error: Please enter a valid option!"

class VagrantPredefinedSubMenu():

    def __init__(self):

        self.header = " - Please pick a predefined Vagrant box - "
        self.error = ""

    def show_menu(self):

        while True:

            clearScreen()

            try:

                print(inspect.cleandoc(f"""
                        {self.header}
                        {self.error}
                        Select one of the following options:
                        1) LAMP
                        2) Windows with Git & Chrome
                        3) Return to main menu
                        """))

                choice = int(input("Enter your choice: "))

                if choice not in [1, 2] or choice == "":

                    if choice == 3:

                        return

                    else:

                        raise ValueError

                else:

                    if choice == 1:

                        lampinstallation = PredefinedVagrantBox()
                        lampinstallation.move_vagrantfile("lamp")

                    elif choice == 2:

                        lampinstallation = PredefinedVagrantBox()
                        lampinstallation.move_vagrantfile("windows")


            except ValueError:

                clearScreen()
                self.error = "* Error: Please enter a valid option!"


if __name__ == '__main__':
    MainMenu().show_menu()
from resources.servers.scripts.serverregistration import ServerRegistration
from resources.vagrant.scripts.vagrantboxmanagement import InteractiveVagrantBox
from resources.globalscripts.clearscreen import clearScreen

class MainMenu:

    
    def __init__(self):

        """ Constructor: We don't need any attributes in this class (for now). """
        
        pass

    def show_menu(self):

        """ Method: This method will clear your screen, start an endless loop, show you a list of options
            and will keep running untill you enter a certain option.
            Depending on your choice it will create a new class object from another script or exit.

            1, 2, 3, 4, 5, 6 -> Valid options

            6 will exit the script.

            Any other input will raise a Valuerror and clear your screen.
        """

        clearScreen()

        while True:

            try:
                   
                print("""
    Select one of the following options:
    1) Register server
    2) Vagrant box management
    3) Remote execution
    4) Remote hosts monitoring
    5) Setup predefined Vagrant box
    6) Quit
        """)

                choice = int(input('Enter your choice: '))
                
                if choice not in range(1,6) or choice == '':

                    if choice == 6:
                        
                        exit("Bye!")

                    else:
                
                        raise ValueError
                
                else:

                    if choice == 1:

                        serverreg = ServerRegistration()
                        serverreg.register_server()
                    
                    elif choice == 2:

                        interactivevagrantbox = InteractiveVagrantBox()
                        interactivevagrantbox.ask_for_options()

            except ValueError:

                clearScreen()
                print("Please enter a valid option!")
                

if __name__ == '__main__':
    MainMenu().show_menu()
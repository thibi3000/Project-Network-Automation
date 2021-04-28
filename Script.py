from resources.servers.scripts.serverregistration import ServerRegistration
from resources.vagrant.scripts.vagrantboxmanagement import InteractiveVagrantBox
from resources.globalscripts.clearscreen import clearScreen

class MainMenu:

    def __init__(self):
        pass

    def show_menu(self):

        
        try:

            while True:
                clearScreen()
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
                
                        raise ValueError('Please pick a valid option!')
                
                else:

                    if choice == 1:

                        serverreg = ServerRegistration()
                        serverreg.register_server()
                    
                    elif choice == 2:

                        interactivevagrantbox = InteractiveVagrantBox()
                        interactivevagrantbox.ask_for_options()


        except ValueError as e:

            print(e)


if __name__ == '__main__':
    MainMenu().show_menu()
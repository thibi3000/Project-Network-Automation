import vagrant
import os
import ipaddress
from resources.globalscripts.clearscreen import clearScreen

class InteractiveVagrantBox:

    def __init__(self):

        self.interactiveboxlocation = os.path.join("resources", "database", "vagrant", "interactive")

    def ask_for_options(self):


        print(""" The following wizard will allow you to specify certain settings for your Vagrant box.
        Examples: #CPU's, #RAM, Network settings & Provisioning""")
        
        while True:

            try:

                cpu = int(input("""Please enter the amount of CPU cores: 
Options: 1, 2, 3, 4: """))

                if cpu not in range(1,5):

                    raise ValueError
                
                break
            
            except ValueError:
                clearScreen()
                print("Please input a valid CPU option!")
            
        
        while True:

            try:

                ram = int(input("""Please enter the amount of RAM (in MB): 
Options: 512, 1024, 2048, 4096: """))

                if ram not in [512, 1024, 2048, 4096]:

                    raise ValueError
                
                break
            
            except ValueError:
                clearScreen()
                print("Please input a valid RAM option!")
        

        while True:

            
            try:

                ip = ipaddress.ip_address(input("""Please specify the server ip (Example: 192.168.1.1): """))
                
                break
            
            except ValueError:

                clearScreen()
                print("Please input a valid ip-address!")
        

        while True:

            try:

                choice = input("Would you like to configure portforwarding? (y|n)")

                if choice.lower() == "y":

                    local = int(input("Please enter the local port: "))
                    public = int(input("Please enter the public port: "))

                    portforwarddict = {

                        "local" : local,
                        "public" : public 
                    }

                    break

                elif choice.lower() == "n":
                    
                    print("Portforwarding won't be configured!")
                    break

                else:

                    raise ValueError
            
            except ValueError:

                clearScreen()
                print("Please input y or n!")


        
        
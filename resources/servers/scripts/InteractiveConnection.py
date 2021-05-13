import inspect
import json
import os
from netmiko import ConnectHandler
import netmiko
from resources.globalscripts.clearscreen import clearScreen

class InteractiveConnection:
    
    def __init__(self):

        self.header = " - Interactive connection - "
        self.error = ""

        self.servername = None
        self.netmikodict = {}
        self.ip = None
        self.username = None
        self.password = None
        self.serverdatabase = os.path.join("resources", "database", "database.json")

    def ask_options(self):

        clearScreen()

        '''print(inspect.cleandoc(f"""
                                {self.header}
                                {self.error}
                                The following wizard will ask your for a few settings to configure your Vagrant box"""))'''

        while True:

            try:

                servername = input("Please pick a server: ")
                
                with open(self.serverdatabase, "r") as serverdatabase:
                        
                    databasecontents = json.load(serverdatabase)
                        
                    serverlist = databasecontents["servers"]

                    serverdatabase.close()

                    valid = False
                    for s in serverlist:

                        if s["server-name"] == servername:
                            
                            valid = True
                            self.servername = s["server-name"]
                            self.netmikodict["host"] = s["ip-address"]


                    if valid == True:

                        self.netmikodict["username"] = input("Please enter your username: ")
                        self.netmikodict["password"] = input("Please enter your password: ")
                        self.netmikodict["device_type"] = "linux"
                        print(self.netmikodict)
                        return

                    else:

                        raise ValueError("Please pick a valid server!")
            
            except ValueError as e:

                print(e)
            
            except Exception:

                print(e)

            
    def connect_to_server(self):
        
        try:

            net_connect = ConnectHandler(**self.netmikodict)

            while True:

                command = input("Please enter your command (to quit: enter 'disconnect'): ")

                if command == "disconnect":

                    net_connect.disconnect()
                    return

                else:

                    output = net_connect.send_command(command)
                    print(output)
                
        except netmiko.NetmikoAuthenticationException:

            print("Unable to login using your credentials!")
        
        except netmiko.NetMikoTimeoutException:

            print("A timeout occured! The host is not available!")

    
    def send_script(self):

        try:

            self.scriptfilelocation = input("Please specify the path of the script: ")
            self.scriptfilename = os.path.basename(self.scriptfilelocation) 
            with open(self.scriptfilelocation, "r") as pvf:

                print(f"{self.scriptfilelocation} was found!")
                self.scriptfilecontents = pvf.read().splitlines() 
                pvf.close()
            
            net_connect = ConnectHandler(**self.netmikodict)


            output = net_connect.send_config_set(self.scriptfilecontents)
            print(output)
                
        except netmiko.NetmikoAuthenticationException:

            print("Unable to login using your credentials!")
        
        except netmiko.NetMikoTimeoutException:

            print("A timeout occured! The host is not available!")
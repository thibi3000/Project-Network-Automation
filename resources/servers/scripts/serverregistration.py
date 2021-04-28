import os
import json
import ipaddress
from resources.globalscripts.clearscreen import clearScreen

class ServerRegistration:

    def __init__(self):

        self.serverdatabase = os.path.join("resources", "servers", "database", "serverdatabase.json")

    def register_server(self):

        while True:

            try:
                
                servername = input('Please specify the server name: ')
                serverip = ipaddress.ip_address(input("""Please specify the server ip (Example: 192.168.1.1): """)) 

                serverdictionary = {
                    "server-name": servername,
                    "ip-address": str(serverip)
                }

                with open(self.serverdatabase, 'r') as serverdatabase:
                    
                    databasecontents = json.load(serverdatabase)
                    
                    serverlist = databasecontents['servers']
                    serverlist.append(serverdictionary)
                    
                
                with open(self.serverdatabase, 'w') as serverdatabase:

                    json.dump(databasecontents, serverdatabase)
                
                clearScreen()
                break
                

            except json.JSONDecodeError:
                clearScreen()
                print("Serverdatabase.json is empty!")

            except ValueError:
                clearScreen()
                print("Please input a valid IPv4 address!")


import os
import json
import ipaddress
from resources.globalscripts.clearscreen import clearScreen

class ServerRegistration:

    def __init__(self):

        """ Constructor:

            self.serverdatabase -> holds the location of the json server database file.

        """
        
        self.serverdatabase = os.path.join("resources", "database", "database.json")

    def register_server(self):

        """ Method: This method is used to register a certain server based on name and ip-address.

            Both inputs (servername, serverip) are nested inside an endless loop, the loop will only break when the inputs are right.

            servername expects a String as input.
            serverip expects a valid ip-address as input, any other input will raise a Valuerror and clear your screen.

            Servername and serverip get written to the json database file.
            A JSONDecodeError gets raised when there is no server array in the json file.
            A FileNotFoundError gets raised when the json database is missing.

        """

        clearScreen()

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
            
            except FileNotFoundError:
                clearScreen()
                print("Serverdatabase.json was not found!")

            except ValueError:
                clearScreen()
                print("Please input a valid ip-address!")


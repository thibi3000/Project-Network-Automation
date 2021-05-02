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
        self.header = " - Server Registration - "
        self.error = ""

    def register_server(self):

        """ Method: This method is used to register a certain server based on name and ip-address.

            Both inputs (servername, serverip) are nested inside an endless loop, the loop will only break when the inputs are right.

            servername expects a String as input.
            serverip expects a valid ip-address as input, any other input will raise a Valuerror and clear your screen.

            Servername and serverip get written to the json database file.
            A JSONDecodeError gets raised when there is no server array in the json file.
            A FileNotFoundError gets raised when the json database is missing.

        """

        while True:

            try:

                clearScreen()
                
                print(self.header)
                print(self.error)

                servername = input("Please specify the server name: ")
                serverip = str(ipaddress.ip_address(input("Please specify the server ip (Example: 192.168.1.1): ")))
                
                serverdictionary = {

                    "server-name": servername,
                    "ip-address": serverip
                }

                with open(self.serverdatabase, "r") as serverdatabase:
                    
                    databasecontents = json.load(serverdatabase)
                    
                    serverlist = databasecontents["servers"]
                    
                    for server in serverlist:

                        if server["server-name"] == servername:
                            
                            serverdatabase.close()
                            raise Exception("* Error: This name is already in use!")

                    serverlist.append(serverdictionary)

                    serverdatabase.close()
                    
                with open(self.serverdatabase, "w") as serverdatabase:

                    json.dump(databasecontents, serverdatabase)

                    serverdatabase.close()
                
                clearScreen()

                break
                

            except json.JSONDecodeError:

                clearScreen()
                self.error = "* Error: Serverdatabase.json is empty!"
            
            except FileNotFoundError:

                clearScreen()
                self.error = "* Error: Serverdatabase.json was not found!"

            except ValueError:

                clearScreen()
                self.error = "* Error: This IPv4-address is not valid!"
            
            except Exception as namealreadyindb:
                
                clearScreen()
                self.error = namealreadyindb



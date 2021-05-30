import os
import json
import ipaddress
import inspect
from resources.globalscripts.clearscreen import clearScreen

class ServerRegistration:

    def __init__(self):

        """ Constructor

            Attributes: 

                header (str) : Contains the name of the current option
                serverdatabase (str) : Location of the json database
        """
        
        self.serverdatabase = os.path.join("resources", "database", "database.json")
        self.header = " - Server Registration - "


    def register_server(self):

        """ Method: This method will clear your screen and ask you for some information to register the server.
            (name, ip, server os)

            An invalid servername will raise an Exception.
            An empty database will raise a JSONDecodeError.
            If the database file is missing it will raise a FileNotFoundError.
        """

        clearScreen()
        
        print(self.header)
        print("")

        while True:
        
            try:
            
                servername = input("Please specify the server name: ")

                with open(self.serverdatabase, "r") as serverdatabase:
                
                    databasecontents = json.load(serverdatabase)
                    
                    serverlist = databasecontents["servers"]
                    
                    for server in serverlist:

                        if server["server-name"] == servername:
                            
                            serverdatabase.close()
                            raise Exception("Error: This name is already in use!")

                    serverdatabase.close()
                
                break

            except json.JSONDecodeError:
                
                
                print("Error: serverdatabase.json is empty!")
                exit(1)
            
            except FileNotFoundError:

                print("Error: serverdatabase.json was not found!")
                exit(1)
            
            except Exception as e:

                print(e)

                continue
                

        while True:

            try:


                serveros = input("Please specify the server OS (windows | macos | linux): ")

                if serveros.lower() not in ["windows", "macos", "linux"]:

                    raise Exception("Error: This OS is not supported!")
                
                break
            
            except Exception as e:

                print(e)

                continue
        

        while True:

            try:

                serverip = str(ipaddress.ip_address(input("Please specify the server ip (Example: 192.168.1.1): ")))

                break

            except ValueError as e:

                print(f"Error: {e}!")

                continue

  
        try:

            serverdictionary = {

                "server-name": servername,
                "ip-address": serverip,
                "os" : serveros.lower()

            }

            with open(self.serverdatabase, "r") as serverdatabase:
                    
                databasecontents = json.load(serverdatabase)

                serverdatabase.close()
                
                serverlist = databasecontents["servers"]
                serverlist.append(serverdictionary)

            
            with open(self.serverdatabase, "w") as serverdatabase:

                json.dump(databasecontents, serverdatabase)

                serverdatabase.close()

            
        except json.JSONDecodeError:
                
            print("Error: serverdatabase.json is empty!")
            exit(1)

        except FileNotFoundError:

            print("Error: serverdatabase.json was not found!")
            exit(1)
            

        while True:

            try:
                
                clearScreen()

                print(inspect.cleandoc(f"""

                        Succesfully added a new server!
                        Summary:

                        Name: {servername}
                        OS: {serveros}
                        IPv4: {serverip}

                        """))

                choice = input("Press Enter to return to the main menu.")

                if choice == "":

                    return
                
                else:

                    raise ValueError

            except ValueError:

                continue
import inspect
import json
import os
import sys
from netmiko import ConnectHandler
import netmiko
from resources.globalscripts.clearscreen import clearScreen


class InteractiveConnection:

    def __init__(self):
        """ Constructor

            Attributes: 

                header (str) : Contains the name of the current option
                netmikodict  (dictionary) : Dictionary used by netmiko to connect to the server
                serverdatabase (str) : Location of the json database

                User input:

                    servername : The name of the chosen server
                    ip : The IPv4 address of the chosen server
                    username: The username that is used to login to the chosen server
                    password: The password that is used to login to the chosen server
        """

        self.header = " - Interactive connection - "

        self.servername = None
        self.ip = None
        self.username = None
        self.password = None

        self.netmikodict = {}

        self.serverdatabase = os.path.join(
            "resources", "database", "database.json")

    def ask_options(self):
        """ Method: This method will clear your screen, start an endless loop and ask you to input a server name.
            If the database contains this server name it will grab the IPv4 address and ask you for your username and password.

            An invalid server input will raise a Valuerror.
        """

        clearScreen()

        print(self.header)
        print("")

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

                        self.netmikodict["username"] = input(
                            "Please enter your username: ")
                        self.netmikodict["password"] = input(
                            "Please enter your password: ")
                        self.netmikodict["device_type"] = "linux"
                        print(self.netmikodict)
                        return

                    else:

                        raise ValueError("Please pick a valid server!")

            except ValueError as e:

                print(e)

                continue

            except Exception as e:

                sys.exit(f"Error: {e}")

    def connect_to_server(self):
        """ Method: This method will use all your credentials to connect to the remote server.
            You will then be able to send unix commands to the server. Entering 'disconnect' will close the session.

            Invalid credentials will raise a NetmikoAuthenticationException.
            Invalid IPv4 or anything else network related will raise a NetMikoTimeoutException.
        """

        try:

            net_connect = ConnectHandler(**self.netmikodict)

            while True:

                command = input(
                    "Please enter your command (to quit: enter 'disconnect'): ")

                if command == "disconnect":

                    net_connect.disconnect()
                    return

                else:

                    output = net_connect.send_command(command)
                    print(output)

        except netmiko.NetmikoAuthenticationException:

            sys.exit("Unable to login using your credentials!")

        except netmiko.NetMikoTimeoutException:

            sys.exit("A timeout occured! The host is not available!")

        except Exception as e:

            sys.exit(f"Error: {e}")

    def send_script(self):
        """ Method: This method will use all your credentials to connect to the remote server.
            You will then be able to send bash scripts to the server. Input can be a relative of full path.

            An invalid script will raise an exception.
            Invalid credentials will raise a NetmikoAuthenticationException.
            Invalid IPv4 or anything else network related will raise a NetMikoTimeoutException.
        """

        try:

            self.scriptfilelocation = input(
                "Please specify the path of the script: ")
            self.scriptfilename = os.path.basename(self.scriptfilelocation)
            with open(self.scriptfilelocation, "r") as pvf:

                print(f"{self.scriptfilelocation} was found!")
                self.scriptfilecontents = pvf.read().splitlines()
                pvf.close()

            net_connect = ConnectHandler(**self.netmikodict)

            output = net_connect.send_config_set(self.scriptfilecontents)
            print(output)

            while True:

                try:

                    choice = input("Press Enter to return to the menu.")

                    if choice == "":

                        return

                    else:

                        raise ValueError

                except ValueError as e:

                    print(e)

                    continue

        except netmiko.NetmikoAuthenticationException:

            sys.exit("Unable to login using your credentials!")

        except netmiko.NetMikoTimeoutException:

            sys.exit("A timeout occured! The host is not available!")

        except Exception as e:

            sys.exit(f"Error: {e}")

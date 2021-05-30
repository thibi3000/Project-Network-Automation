from resources.globalscripts.clearscreen import clearScreen
import os
import json
import sys
import inspect

if sys.platform == 'win32':
        
    import wmi

import netmiko
from netmiko import ConnectHandler

class RemoteHostMonitoring:

    def __init__(self):

        """ Constructor

            Attributes: 

                header (str) : Contains the name of the current option
                netmikodict  (dictionary) : Dictionary used by netmiko to connect to the server
                serverdatabase (str) : Location of the json database
        """
        
        self.serverdatabase = os.path.join("resources", "database", "database.json")
        self.netmikoandwmidict = {}
        self.netmikodict = {}

        self.header = " - Remote Host Monitoring - "

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
                            
                            self.netmikoandwmidict["host"] = s["ip-address"]
                            self.netmikoandwmidict["os"] = s["os"]

                    if valid == True:

                        self.netmikoandwmidict["username"] = input("Please enter your username: ")
                        self.netmikoandwmidict["password"] = input("Please enter your password: ")
                        
                        return

                    else:

                        raise ValueError("Please pick a valid server!")
            
            except ValueError as e:

                print(e)

                continue
            
            except Exception:

                print(e)

                exit(1)

    def try_to_connect(self):

        """ Method: This method will first determine your operating system. If you're running this script on Windows you can
            request information from Windows and Unix-based servers. If you're running Linux or macOS you can only request informatio
            from Unix-based servers.

            The information contains: running processes, disk usage, ram usage & cpu usage.
            
            Invalid credentials will raise a NetmikoAuthenticationException.
            Invalid IPv4 or anything else network related will raise a NetMikoTimeoutException.
            
        """

        try:

            if self.netmikoandwmidict["os"] == "windows":

                if sys.platform == "win32":

                
                    print("Windows!")

                    c = wmi.WMI(self.netmikoandwmidict["host"], user=self.netmikoandwmidict["username"], password=self.netmikoandwmidict["password"],)
                    
                    print("Running processes: ")
                    for process in c.Win32_Process():
                        print(process.ProcessId, process.Name)

                    print("")
                    print("Disk usage: ")
                    for disk in c.Win32_logicaldisk():

                        if disk.Caption == "C:":
                            
                            usedspace = float(disk.Size) - float(disk.FreeSpace)

                            print(f"{round(usedspace / 1024**3,2)} GB / {round(float(disk.Size) / 1024**3, 2)} GB")

                    print("")
                    print("RAM usage: ")
                    for memory in c.Win32_OperatingSystem():
        
                        usedmemory = float(memory.TotalVisibleMemorySize) - float(memory.FreePhysicalMemory)
                        
                        print(f"{round(usedmemory / 1024**2,2)} GB / {round(float(memory.TotalVisibleMemorySize) / 1024**2, 2)} GB")

                    print("")
                    print("CPU usage: ")
                    for cpu in c.Win32_Processor():
        
                        if cpu.LoadPercentage == None:

                            raise Exception("Error: Unable to retrieve CPU LoadPercentage!")
                            
                        else:

                            print(f"{cpu.LoadPercentage} %")
                
                else:

                    
                    raise Exception("Error: Sorry! Monitoring Windows machines is not possible on Linux & macOS!")

            else:

                print("Linux or macOS!")

                self.netmikodict["device_type"] = "linux"
                self.netmikodict["host"] = self.netmikoandwmidict["host"]
                self.netmikodict["username"] = self.netmikoandwmidict["username"]
                self.netmikodict["password"] = self.netmikoandwmidict["password"]
                
                
                set = ['df -H | grep -vE "^Filesystem/tmpfs/cdrom"',
                 "free -m",
                 "ps -a",
                 "mpstat -P ALL"]

                net_connect = ConnectHandler(**self.netmikodict)


                output = net_connect.send_config_set(set)

                print(output)
                

            while True:

                try:

                    choice = input("Press Enter to return to the menu.")

                    if choice == "":

                        return
                    
                    else:

                        raise ValueError

                except ValueError:

                    continue

        except netmiko.NetmikoAuthenticationException:

            print("Unable to login using your credentials!")
            exit(1)

        except netmiko.NetMikoTimeoutException:

            print("A timeout occured! The host is not available!")
            exit(1)

        except Exception as e:
            print(e)
            exit(1)
        
        except wmi.x_wmi:

            print("Something went wrong while connecting to the remote machine.\nPossible reasons: You're trying to connect to a Linux machine, your credentials are wrong, ...")
            exit(1)

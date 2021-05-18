from resources.globalscripts.clearscreen import clearScreen
import os
import json
import sys

if sys.platform == 'win32':
        
    import wmi

import netmiko
from netmiko import ConnectHandler

class RemoteHostMonitoring:

    def __init__(self):
        
        self.serverdatabase = os.path.join("resources", "database", "database.json")
        self.netmikoandwmidict = {}
        self.netmikodict = {}

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
            
            except Exception:

                print(e)

    def try_to_connect(self):


        try:

            if self.netmikoandwmidict["os"] == "windows":
                
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
    
                    pass

            else:

                print("Linux or macOS!")

                self.netmikodict["device_type"] = "linux"
                self.netmikodict["host"] = self.netmikoandwmidict["host"]
                self.netmikodict["username"] = self.netmikoandwmidict["username"]
                self.netmikodict["password"] = self.netmikoandwmidict["password"]
                
                

                print(self.netmikodict)
                
                set = ['df -H | grep -vE "^Filesystem/tmpfs/cdrom"',
                 "free -m",
                 "ps -a",
                 "mpstat -P ALL"]

                net_connect = ConnectHandler(**self.netmikodict)


                output = net_connect.send_config_set(set)

                print(output)
                
        


        except wmi.x_wmi:

            print("Something went wrong while connecting to the remote machine.\nPossible reasons: You're trying to connect to a Linux machine, your credentials are wrong, ...")
        
        except netmiko.NetmikoAuthenticationException:

            print("Unable to login using your credentials!")
        
        except netmiko.NetMikoTimeoutException:

            print("A timeout occured! The host is not available!")

        except Exception as e:
            print(e)
            exit(1)

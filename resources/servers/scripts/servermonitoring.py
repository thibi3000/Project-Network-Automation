import inspect
import json
import os
from netmiko import ConnectHandler
from resources.globalscripts.clearscreen import clearScreen

class ServerMonitoring:

    def __init__(self):

        self.header = " - Server Monitoring - "
        self.error = ""

        """
        Als python script uitgevoerd wordt op W10:
-> Remote OS checken:
-> Indien Windows: Powershell aanroepen met subprocess (met Enter-PSSession -HostName <IP>)
-> Indien Linux: Verbinden via SSH en zo info opvragen

Als python script uitgevoerd wordt op Linux/macOS
-> Remote OS checken:
-> Indien Windows: PSWSMan installeren, ssh toelaten op remote windows (moet op voorhand gebeuren door gebruiker), pwsh oproepen via subprocess (met Enter-PSSession -HostName <IP>)
-> Indien Linux/macOS: Verbinden via SSH en zo info opvragen
	
	

         """
import vagrant
import os
import ipaddress
import requests
import json
from resources.globalscripts.clearscreen import clearScreen

class InteractiveVagrantBox:

    def __init__(self):

        """ Constructor: 

            self.interactiveboxlocation -> holds the location of the interactive vagrant folder.

        """


        self.serverdatabase = os.path.join("resources", "database", "database.json")
        self.allinteractiveboxes = os.path.join("resources", "database", "vagrant", "interactive")
        self.interactiveboxlocation = None
        self.interactiveboxname = None
        self.interactiveboximage = None
        self.cpu = None
        self.ram = None
        self.ip = None
        self.portforwarddict = {
            "local": "None",
            "public": "None"
        }
        self.provisionfilecontents = None
        self.provisionfilelocation = None


    def ask_for_options(self):

        """ Method: This method will ask you to input several configuration options for your Vagrant box.

            Each input is nested inside an endless loop, the loop will only break when the input is right.

            cpu and ram expect an Integer as input, any other input will raise a Valuerror and clear your screen.
            ip expects a valid ip-address as input, any other input will raise a Valuerror and clear your screen.

        """

        clearScreen()

        print(""" The following wizard will allow you to specify certain settings for your Vagrant box.
        Examples: #CPU's, #RAM, Network settings & Provisioning""")

        while True:

            self.interactiveboximage = input("""Please enter a valid Vagrant image: """)
            if self.check_vagrant_image(self.interactiveboximage):

                break
        
        
        while True:

            self.interactiveboxname = input('Please enter a name for your Vagrant box: ')
            boxnames = []
            valid = True
            with open(self.serverdatabase,'r') as serverdatabase:
                data = json.load(serverdatabase)
                for box in data['vagrantboxes']:
                    boxnames.append(box['name'])
            
            for name in boxnames:

                if self.interactiveboxname == name:
                    valid = False
                        
            if valid == True:

                print('Valid name!')
                self.interactiveboxlocation = os.path.join("resources", "database", "vagrant", "interactive", self.interactiveboxname)
                break

            else:

                clearScreen()
                print('This name is already in use! Please pick another one!')
            
           

        
        while True:

            try:

                self.cpu = int(input("""Please enter the amount of CPU cores: 
Options: 1, 2, 3, 4: """))

                if self.cpu not in range(1,5):

                    raise ValueError
                
                break
            
            except ValueError:
                clearScreen()
                print("Please input a valid CPU option!")
            
        
        while True:

            try:

                self.ram = int(input("""Please enter the amount of RAM (in MB): 
Options: 512, 1024, 2048, 4096: """))

                if self.ram not in [512, 1024, 2048, 4096]:

                    raise ValueError
                
                break
            
            except ValueError:
                clearScreen()
                print("Please input a valid RAM option!")
        

        while True:

            
            try:

                self.ip = format(ipaddress.ip_address(input("""Please specify the server ip (Example: 192.168.1.1): """)))
                
                break
            
            except ValueError:

                clearScreen()
                print("Please input a valid ip-address!")
        

        while True:

            try:

                choice = input("Would you like to configure portforwarding? (y|n): ")

                if choice.lower() == "y":

                    while True:

                        try:

                            local = int(input("Please enter the local port you'd like to forward: "))
                            break

                        except ValueError:
                            
                            clearScreen()
                            print('Please input a valid local port!')



                    while True:

                        try:

                            public = int(input("Please enter the public port you'd like to forward: "))
                            break

                        except ValueError:
                            
                            clearScreen()
                            print('Please input a valid public port!')

                    self.portforwarddict = {
                        
                        "local" : local,
                        "public" : public 
                    }

                    break



                elif choice.lower() == "n":
                    
                    print("Portforwarding won't be configured!")
                    break

                else:

                    raise ValueError('Please input y or n!')
            
            
            except ValueError:

                clearScreen()
                print('Please input y or n!')

        
        while True:

            try:

                self.provisionfilelocation = input("Please specify the path of the provision file (.sh) or (.ps1): ")

                with open(self.provisionfilelocation, 'r') as pvf:

                    print(f'{self.provisionfilelocation} was found!')
                    self.provisionfilecontents = pvf.readlines()
                    clearScreen()
                    break
 
            except FileNotFoundError:

                clearScreen()
                print(f'Unable to find {provisionfilelocation}')
        

        self.write_to_database(self.interactiveboxname, self.interactiveboximage, self.interactiveboxlocation, self.cpu, self.ram, self.ip, self.portforwarddict, self.provisionfilelocation)
            
        
        print(f"""You selected these options: \n
    # Name: {self.interactiveboxname}\n
    # Image: {self.interactiveboximage}\n
    # Location : {self.interactiveboxlocation}\n
    # CPU: {self.cpu}\n
    # RAM: {self.ram}\n
    # IP: {self.ip}\n
    # Portforwarding: local: {self.portforwarddict['local']}, public: {self.portforwarddict['public']}\n
    # Provision file: {self.provisionfilelocation}""")


    def create_interactive_box(self):

        try:

            os.chdir(self.allinteractiveboxes)
            os.mkdir(self.interactiveboxname)
            os.chdir(self.interactiveboxname)
            v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
            v.init(self.interactiveboximage)

        except OSError:

            print('')

        except Exception as e:

            print(e)

        '''    def apply_config_file_settings(self):


        contents = f"""
  config.vm.provider "virtualbox" do |v|
    v.memory = {self.ram}
    v.cpus = {self.cpu}


    config.vm.hostname = '{self.interactiveboxname}'
    config.vm.network "private_network", ip: "{self.ip}"
    config.vm.network "forwarded_port", guest: {self.portforwarddict["local"]}}, host: {self.portforwarddict["public"]}
            """
        #with open(os.path.join(self.interactiveboxlocation, 'Vagrantfile')) as VagrantFile:
            '''








































































    def check_vagrant_image(self, image):

        try:
  
            user = image.split('/')[0]
            os = image.split('/')[1]

        except IndexError:

            print('This image name is not valid! Example: ubuntu/trusty64')

            return False
        
        try:

            r = requests.get(f'https://app.vagrantup.com/{user}/boxes/{os}')

            if r.status_code == 200:

                clearScreen()
                print('This is a valid image!')

                return True

            else:
                
                clearScreen()
                print('This image is not valid!')

                return False
        
        except requests.HTTPError as e:

            clearScreen()
            print(e)
            return False

        except requests.ConnectionError as e:

            clearScreen()
            print(e)
            return False

    
    def write_to_database(self, name, image, location, cpu, ram, ip, portforward, provision):

        
        vagrantdictionary = {

            "name" : name,
            "image" : image,
            "location" : location,
            "cpu" : cpu,
            "ram" : ram,
            "ip" : ip,
            "local" : portforward['local'],
            "public": portforward['public'],
            "provision" : provision
        }

        try:

            with open(self.serverdatabase, 'r') as serverdatabase:
                        
                        databasecontents = json.load(serverdatabase)
                        
                        vagrantlist = databasecontents['vagrantboxes']
                        vagrantlist.append(vagrantdictionary)
                        
                    
            with open(self.serverdatabase, 'w') as serverdatabase:
                
                json.dump(databasecontents, serverdatabase)

    
        except json.JSONDecodeError:

            clearScreen()
            print("Serverdatabase.json is empty!")
            
        except FileNotFoundError:
            clearScreen()
            print("Serverdatabase.json was not found!")


    
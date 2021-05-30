import vagrant
import os
import ipaddress
import requests
import json
import inspect
from resources.globalscripts.clearscreen import clearScreen


class InteractiveVagrantBox:

    def __init__(self):
        """ Constructor

            Attributes: 

                header (str) : Contains the name of the current option
                serverdatabase (str) : Location of the json database
                allinteractiveboxes (str) : Location of all the newly created Vagrant boxes.

                User input:

                    interactiveboxname : Name of the new Vagrant box.
                    interactiveboximage : Image of the new Vagrant box. For example: hashicorp/precise64
                    cpu : Amount of cpu cores
                    ram : Amount of RAM
                    ip : IPv4 address
                    portforwarddict (dictionary) : Dictionary containing local and public ports for portforwarding
                    provisionfilecontents : Holds the contents of the given provisionfile
                    provisionfilelocation : Location of the given provisionfile
        """

        self.serverdatabase = os.path.join(
            "resources", "database", "database.json")
        self.allinteractiveboxes = os.path.join(
            "resources", "database", "vagrant", "interactive")
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
        self.mainpath = os.getcwd()

        self.header = " - Create Vagrant Box (interactive) - "

    def ask_for_options(self):
        """ Method: This method will ask you to input several configuration options for your Vagrant box.

            Each input is nested inside an endless loop, the loop will only break when the input is right.

            cpu and ram expect an Integer as input, any other input will raise a Valuerror.
            ip expects a valid ip-address as input, any other input will raise a Valuerror.
            portforwarding (local and public) expect an Integer as input, any other input will raise a Valuerror.

            A new and valid Vagrant box gets written to the Json database.
        """

        clearScreen()

        print(inspect.cleandoc(f"""
                        {self.header}

                        The following wizard will ask your for a few inputs to configure your Vagrant box.
                        
                        """))

        while True:

            try:

                self.interactiveboximage = input(
                    """Please enter a valid Vagrant image: """)

                if self.check_vagrant_image(self.interactiveboximage):

                    break

                else:

                    raise Exception(
                        "Error: This is not a valid image! Example: hashicorp/precise64.")

            except Exception as e:

                print(e)

                continue

        while True:

            try:

                self.interactiveboxname = input(
                    "Please enter a name for your Vagrant box: ")

                if self.interactiveboximage == '':

                    raise ValueError(
                        "Error: Invalid name! Please pick another one!")

                boxnames = []

                with open(self.serverdatabase, "r") as serverdatabase:

                    data = json.load(serverdatabase)

                    for box in data["vagrantboxes"]:

                        boxnames.append(box["name"])

                    serverdatabase.close()

                for name in boxnames:

                    if self.interactiveboxname == name:

                        raise ValueError(
                            "Error: This name already exists! Please pick another one!")

                self.interactiveboxlocation = os.path.join(
                    "resources", "database", "vagrant", "interactive", self.interactiveboxname)

                break

            except json.JSONDecodeError:

                print("Error: serverdatabase.json is empty!")
                exit(1)

            except FileNotFoundError:

                print("Error: serverdatabase.json was not found!")
                exit(1)

            except ValueError as e:

                print(e)
                continue

        while True:

            try:

                self.cpu = int(input(inspect.cleandoc("""
                    Please enter the amount of CPU cores: 
                    Options: 1, 2, 3, 4: 
                    """)))

                if self.cpu not in range(1, 5):

                    raise ValueError("Error: Please input a valid CPU option!")

                break

            except ValueError as e:

                print(e)

                continue

        while True:

            try:

                self.ram = int(input(inspect.cleandoc("""
                    Please enter the amount of RAM (in MB): 
                    Options: 512, 1024, 2048, 4096: 
                    """)))

                if self.ram not in [512, 1024, 2048, 4096]:

                    raise ValueError("Error: Please input a valid RAM option!")

                break

            except ValueError as e:

                print(e)

                continue

        while True:

            try:

                self.ip = format(ipaddress.ip_address(
                    input("""Please specify the server ip (Example: 192.168.1.1): """)))

                break

            except ValueError as e:

                print(f"Error: {e}!")

                continue

        while True:

            try:

                choice = input(
                    "Would you like to configure portforwarding? (y|n): ")

                if choice.lower() == "y":

                    while True:

                        try:

                            local = int(
                                input("Please enter the local port you'd like to forward: "))
                            break

                        except ValueError:

                            print("Error: Please input a valid local port!")

                            continue

                    while True:

                        try:

                            public = int(
                                input("Please enter the public port you'd like to forward: "))
                            break

                        except ValueError:

                            print("Please input a valid public port!")

                            continue

                    self.portforwarddict = {

                        "local": local,
                        "public": public
                    }

                    break

                elif choice.lower() == "n":

                    print("Portforwarding won't be configured!")
                    break

                else:

                    raise ValueError("Error: Please input y or n!")

            except ValueError as e:

                print(e)

                continue

        while True:

            try:

                self.provisionfilelocation = input(
                    "Please specify the path of the provision file (.sh) or (.ps1): ")
                self.provisionfilename = os.path.basename(
                    self.provisionfilelocation)
                with open(self.provisionfilelocation, "r") as pvf:

                    print(f"{self.provisionfilelocation} was found!")
                    self.provisionfilecontents = pvf.read()
                    pvf.close()

                    break

            except FileNotFoundError:

                print(f"Unable to find provision file!")

                continue

        self.write_to_database(self.interactiveboxname, self.interactiveboximage, self.interactiveboxlocation,
                               self.cpu, self.ram, self.ip, self.portforwarddict, self.provisionfilelocation)

        while True:

            try:

                clearScreen()

                print(inspect.cleandoc(f"""

                        Succesfully checked all your inputs!
                        Summary:

                        Name: {self.interactiveboxname}
                        Image: {self.interactiveboximage}
                        IPv4: {self.ip}
                        Location : {self.interactiveboxlocation}
                        CPU cores: {self.cpu}
                        RAM: {self.ram} MB
                        Portforwarding: local: {self.portforwarddict['local']}, public: {self.portforwarddict['public']}
                        Provision file: {self.provisionfilelocation}

                        In order to complete this process we will need to initiate your Vagrant box.
                        This will take some time. Please be patient.
                        """))

                choice = input("Press Enter to continue.")

                if choice == "":

                    return

                else:

                    raise ValueError

            except ValueError:

                continue

    def create_interactive_box(self):
        """ Method: This method creates a new directory for your Vagrant box. It will then initiate/start the box.

            apply_config_file_settings() is called to apply all your personal inputs.

            If everything goes well the box will shutdown. Any errors will cause the script to stop.
        """

        try:

            clearScreen()

            os.chdir(self.allinteractiveboxes)
            os.mkdir(self.interactiveboxname)
            os.chdir(self.interactiveboxname)

            v = vagrant.Vagrant(quiet_stdout=False, quiet_stderr=False)
            v.init(self.interactiveboximage)

            self.apply_config_file_settings()

            v.up()
            v.halt()

            os.chdir(self.mainpath)

        except Exception as e:

            print(f"Error while initiating your Vagrant box: {e}")
            exit(1)

        while True:

            try:

                clearScreen()

                print(inspect.cleandoc(f"""

                        Succesfully configured your new Vagrant box!
                        You can launch this box with the option 'Manage existing boxes'.
                        """))

                choice = input(
                    "Press Enter to return to the Vagrant Box Management menu.")

                if choice == "":

                    return

                else:

                    raise ValueError

            except ValueError:

                continue

    def apply_config_file_settings(self):
        """ Method: By far the most complicated method.
            1) Provisionfile gets added to the box.
            2) All your personal inputs (ram, cpu, image, portforwarding) get written to the Vagrantfile.
        """

        try:

            with open(os.path.join(self.mainpath, self.interactiveboxlocation, self.provisionfilename), 'w') as ProvisionFile:

                ProvisionFile.write(self.provisionfilecontents)
                ProvisionFile.close()

            contents = inspect.cleandoc(f"""
            Vagrant.configure("2") do |config|

              config.vm.box = "{self.interactiveboximage}"

              config.vm.provider "virtualbox" do |v|
                v.memory = {self.ram}
                v.cpus = {self.cpu}
                v.gui = true
            end

            config.vbguest.auto_update = false
            config.vm.synced_folder '.', '/vagrant', disabled: true
            config.vm.provision :shell, path: "{self.provisionfilename}"

            """)

            if self.portforwarddict["local"] != "None":

                contents += f"""\n  config.vm.network :forwarded_port, guest: {self.portforwarddict["local"]}, host: {self.portforwarddict["public"]}"""

            contents += """\nend"""

            with open(os.path.join(self.mainpath, self.interactiveboxlocation, 'Vagrantfile'), 'w') as VagrantFile:

                VagrantFile.write(contents)
                VagrantFile.close()

        except FileNotFoundError:

            print(
                f"Error: Unable to find {os.path.join(self.mainpath, self.interactiveboxlocation, 'Vagrantfile')}")
            exit(1)

        except Exception:

            print(
                f"Error: Something went wrong while writing the configuration settings!")
            exit(1)

    def check_vagrant_image(self, image):
        """ Method: This method will check the availability of the given Vagrantimage. We don't users to input false images.
            We're using the api endpoint used by https://vagrantcloud.com.

            All requests related errors will return False
        """

        try:

            user = image.split('/')[0]
            os = image.split('/')[1]

        except IndexError:

            return False

        try:

            r = requests.get(f'https://app.vagrantup.com/{user}/boxes/{os}')
            r.raise_for_status()

            if r.status_code == 200:

                return True

            else:

                return False

        except requests.HTTPError as e:

            return False

        except requests.ConnectionError as e:

            return False

        except requests.exceptions.HTTPError:

            return False

    def write_to_database(self, name, image, location, cpu, ram, ip, portforward, provision):
        """ Method: Simple method to write your Vagrant box and its settings to the Json database.
        """

        vagrantdictionary = {

            "name": name,
            "image": image,
            "location": location,
            "cpu": cpu,
            "ram": ram,
            "ip": ip,
            "local": portforward['local'],
            "public": portforward['public'],
            "provision": provision
        }

        try:

            with open(self.serverdatabase, 'r') as serverdatabase:

                databasecontents = json.load(serverdatabase)

                vagrantlist = databasecontents['vagrantboxes']
                vagrantlist.append(vagrantdictionary)
                serverdatabase.close()

            with open(self.serverdatabase, 'w') as serverdatabase:

                json.dump(databasecontents, serverdatabase)
                serverdatabase.close()

        except json.JSONDecodeError:

            print("Serverdatabase.json is empty!")
            exit(1)

        except FileNotFoundError:

            print("Serverdatabase.json was not found!")
            exit(1)

        except Exception as e:

            print(f"Error: {e}!")
            exit(1)

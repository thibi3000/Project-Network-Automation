from netmiko import ConnectHandler

class InteractiveConnection:
    def __init__(self):

        self.header = " - Interactive connection - "
        self.error = ""

        self.deviceType = None;
        self.ip = None;
        self.username = None;
        self.password = None;

    def ask_options(self):

        clearScreen()

        print(inspect.cleandoc(f"""
                                {self.header}
                                {self.error}
                                The following wizard will ask your for a few settings to configure your Vagrant box"""))

        while True:

            self.deviceType = input("""Please enter a valid deviceType, ex. linux: """)
            if self.deviceType in ["Linux, Windows, Mac"]
                print(self.header)
                break
            else:
                print(self.error)

import sys
import os

def clearScreen():

    """ Method: This method will check what operating system you are using by calling sys.platform
        and will wipe the console/command prompt.
        win32 -> 'cls'
        linux -> 'clear'
        darwin -> 'clear'
    """

    if sys.platform == 'win32':
        os.system('cls')
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        os.system('clear')
        

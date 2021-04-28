import sys
import os

def clearScreen():

    if sys.platform == 'win32':
        os.system('cls')
    elif sys.platform == 'linux' or sys.platform == 'darwin':
        os.system('clear')
        

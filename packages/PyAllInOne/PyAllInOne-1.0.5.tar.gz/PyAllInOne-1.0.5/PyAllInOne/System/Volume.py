# PyAllInOne (System) - Volume

''' This is the "Volume" module. '''

# Imports
import os
import platform

# The Directory
directory = os.path.dirname(os.path.realpath(__file__)).replace(os.sep, "/")

# Function 1 - Max
def max():
    # Checking the OS
    if (platform.uname().system == "Windows"):
        # Setting the Volume
        os.chdir(directory + "/assets")
        os.system("setvol 100")
    else:
        raise Exception("This function only works on Windows.")

# Function 2 - Min
def min():
    # Checking the OS
    if (platform.uname().system == "Windows"):
        # Setting the Volume
        os.chdir(directory + "/assets")
        os.system("setvol 0")
    else:
        raise Exception("This function only works on Windows.")

# Function 3 - Increase
def increase(value):
    # Checking the OS
    if (platform.uname().system == "Windows"):
        # Checking the Data Type of "value"
        if (isinstance(value, int)):
            # Setting the Volume
            os.chdir(directory + "/assets")
            os.system("setvol +" + str(value))
        else:
            raise TypeError("The 'value' argument must be an integer.")
    else:
        raise Exception("This function only works on Windows.")

# Function 4 - Decrease
def decrease(value):
    # Checking the OS
    if (platform.uname().system == "Windows"):
        # Checking the Data Type of "value"
        if (isinstance(value, int)):
            # Setting the Volume
            os.chdir(directory + "/assets")
            os.system("setvol -" + str(value))
        else:
            raise TypeError("The 'value' argument must be an integer.")
    else:
        raise Exception("This function only works on Windows.")

# Function 5 - Mute
def mute():
    # Checking the OS
    if (platform.uname().system == "Windows"):
        # Setting the Volume
        os.chdir(directory + "/assets")
        os.system("setvol mute")
    else:
        raise Exception("This function only works on Windows.")

# Function 6 - Unmute
def unmute():
    # Checking the OS
    if (platform.uname().system == "Windows"):
        # Setting the Volume
        os.chdir(directory + "/assets")
        os.system("setvol unmute")
    else:
        raise Exception("This function only works on Windows.")

# Function 7 - Set
def set(value):
    # Checking the OS
    if (platform.uname().system == "Windows"):
        # Checking the Data Type of "value"
        if (isinstance(value, int)):
            # Setting the Volume
            os.chdir(directory + "/assets")
            os.system("setvol " + str(value))
        else:
            raise TypeError("The 'value' argument must be an integer.")
    else:
        raise Exception("This function only works on Windows.")
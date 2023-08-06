# PyAllInOne (Computer) - Brightness

''' This is the "Brightness" module. '''

# Imports
import screen_brightness_control as sbc
import platform

# Function 1 - Max
def max():
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Setting the Brightness
        sbc.set_brightness(100)
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 2 - Min
def min():
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Setting the Brightness
        sbc.set_brightness(0)
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 3 - Set
def set(value):
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Setting the Brightness
        if (isinstance(value, (int, float))):
            sbc.set_brightness(value)
        else:
            raise Exception("The 'value' argument must be an integer or a float.")
    else:
        raise Exception("This function only works on Windows and Linux.")
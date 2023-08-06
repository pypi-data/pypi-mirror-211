# PyAllInOne (System) - Brightneszs

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
def set(value, display=0):
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Checking the Data Type of "value"
        if (isinstance(value, (int, float))):
            # Checking the Data Type of "display"
            if (isinstance(display, int)):
                # Setting the Brightness
                sbc.set_brightness(value, display=display)
            else:
                raise TypeError("The 'display' argument must be an integer.")
        else:
            raise TypeError("The 'value' argument must be an integer or a float.")
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 4 - Get
def get(display=0):
    # Checking the OS
    if (platform.uname().system == "Windows" or platform.uname().system == "Linux"):
        # Checking the Data Type of "display"
        if (isinstance(display, int)):
            # Returning the Data
            return {"Brightness": sbc.get_brightness(display=0), "Monitors": sbc.list_monitors()}
        else:
            raise TypeError("The 'display' argument must be an integer.")
    else:
        raise Exception("This function only works on Windows and Linux.")
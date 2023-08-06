# PyAllInOne (System) - Clipboard

''' This is the "Clipboard" module. '''

# Imports
import pyperclip

# Function 1 - Copy
def copy(text):
    # Checking the Data Type of "text"
    if (isinstance(text, str)):
        # Copying the Text
        pyperclip.copy(text)
    else:
        raise TypeError("The 'text' argument must be a string.")

# Function 2 - Paste
def paste():
    return pyperclip.paste()
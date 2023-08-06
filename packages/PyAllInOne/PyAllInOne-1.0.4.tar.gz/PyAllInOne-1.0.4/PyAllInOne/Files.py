# PyAllInOne - Files

''' This is the "Files" module. '''

# Imports
import os
import mimetypes

# Function 1 - Exists
def exists(path):
    return os.path.exists(path)

# Function 2 - File Type
def file_type(path):
    # Initializing Mimetypes
    mimetypes.init()

    # Checking if Path Exists
    if (exists(path)):
        return mimetypes.guess_type(path)[0].split("/")[0]
    else:
        raise Exception("The file path doesn't exist.")
# PyAllInOne - JSON

''' This is the "JSON" module. '''

# Imports
import json

# Function 1 - Convert
def convert(data, indent=4):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Checking the Data Type of "indent"
        if (isinstance(indent, int)):
            return json.dumps(data, indent=indent) # Converts Python Dict to JSON String
        else:
            raise TypeError("The 'indent' argument must be an integer.")
    elif (isinstance(data, str)):
        return json.loads(data) # Converts JSON String to Python Dict
    else:
        raise TypeError("The 'data' argument must be a dictionary or a string.")
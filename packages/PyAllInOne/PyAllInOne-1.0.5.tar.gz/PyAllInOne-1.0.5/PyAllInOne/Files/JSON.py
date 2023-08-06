# PyAllInOne (Files) - JSON

''' This is the "JSON" module. '''

# Imports
import json

# Function 1 - Convert
def convert(data, indent=4):
    # Checking the Data Type of "data"
    if (isinstance(data, dict)):
        # Checking the Data Type of "indent"
        if (isinstance(indent, int)):
            # Converting Python Dict to JSON String
            return json.dumps(data, indent=indent)
        else:
            raise TypeError("The 'indent' argument must be an integer.")
    elif (isinstance(data, str)):
        # Converting JSON String to Python Dict
        return json.loads(data)
    else:
        raise TypeError("The 'data' argument must be a dictionary or a string.")
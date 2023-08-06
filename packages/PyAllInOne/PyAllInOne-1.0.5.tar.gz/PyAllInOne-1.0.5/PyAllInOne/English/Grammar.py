# PyAllInOne (English) - Grammar

''' This is the "Grammar" module. '''

# Imports
from gingerit.gingerit import GingerIt

# Function 1 - Capitalized
def capitalized(phrase):
    # Checking the Data Type of "phrase"
    if (isinstance(phrase, str)):
        # Checking if Phrase is Capitalized
        if (phrase[0] >= "A" and phrase[0] <= "Z"):
            return True
        elif (phrase[0] >= "a" and phrase[0] <= "z"):
            return False
    else:
        raise TypeError("The 'phrase' argument must be a string.")

# Function 2 - Correct
def correct(text, full_result=False):
    # Checking the Data Type of "text"
    if (isinstance(text, str)):
        # Checking the Data Type of "full_result"
        if (isinstance(full_result, bool)):
            # Returning the Corrected Text
            if (full_result):
                return GingerIt().parse(text)
            else:
                return GingerIt().parse(text)["result"]
        else:
            raise TypeError("The 'full_result' argument must be a boolean.")
    else:
        raise TypeError("The 'text' argument must be a string.")
# PyAllInOne (English) - Grammar

''' This is the "Grammar" module. '''

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
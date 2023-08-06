# PyAllInOne (Math) - Statistics

''' This is the "Statistics" module. '''

# Function 1 - Mean
def mean(data):
    if isinstance(data, (list, tuple, set)):
        if (len(data) != 0):
            return sum(data) / len(data)
        else:
            raise Exception("The array can't be empty.")
    else:
        raise TypeError("The data must be in the form of a list, tuple, or set.")

# Function 2 - Mode
def mode(data):
    if isinstance(data, (list, tuple, set)):
        if (len(data) != 0):
            return max(data)
        else:
            raise Exception("The array can't be empty.")
    else:
        raise TypeError("The data must be in the form of a list, tuple, or set.")

# Function 3 - Median
def median(data):
    if isinstance(data, (list, tuple, set)):
        if (len(data) != 0):
            data.sort()
            mid = len(data) // 2

            return (data[mid] + data[~mid]) / 2
        else:
            raise Exception("The array can't be empty.")
    else:
        raise TypeError("The data must be in the form of a list, tuple, or set.")
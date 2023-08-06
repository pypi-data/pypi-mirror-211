# PyAllInOne (Math) - Quadratic

''' This is the "Quadratic" module. '''

# Imports
import math

# Function 1 - Find Discriminant
def find_discriminant(a, b, c):
    newA = float(a)
    newB = float(b)
    newC = float(c)

    # Returning the Discriminant
    return (b**2) - (4*a*c)

# Function 2 - Find Roots
def find_roots(a, b, c):
    newA = float(a)
    newB = float(b)
    newC = float(c)

    discriminant = findDiscriminant(a, b, c)

    alpha = (-newB + math.sqrt(discriminant)) / (2*newA)
    beta = (-newB - math.sqrt(discriminant)) / (2*newA)

    # Returning the Roots
    return (alpha, beta)
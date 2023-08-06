# PyAllInOne (Math) - Trigonometry

''' This is the "Trigonometry" module. '''

# Imports
import math

# Functions - Conversions
def degrees_to_radians(degrees): return degrees * (3.14/180)
def radians_to_degrees(radians): return radians * (180/3.14)

# Functions - Trigonometric Ratios
def sin(radians): return math.sin(radians)
def cos(radians): return math.cos(radians)
def tan(radians): return math.tan(radians)
def cosec(radians): return 1 / (sin(radians))
def sec(radians): return 1 / (cos(radians))
def cot(radians): return 1 / (tan(radians))
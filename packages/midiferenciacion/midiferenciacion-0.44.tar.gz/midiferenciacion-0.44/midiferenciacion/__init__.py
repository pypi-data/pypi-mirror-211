from scipy.misc import derivative
import numpy as np

def dif(funcion, x):
    """ First derivative
    """
    return derivative(funcion, x)

#dif(x**2, x=1)
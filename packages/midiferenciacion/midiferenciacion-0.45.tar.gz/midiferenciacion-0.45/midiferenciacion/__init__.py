import sympy as sp

def derivative(function, eval_a, eval_b):
    """ This function returns the first derivative of a given function 
    Parameters
    ----------
    function : string
        Defined function in terms of x
    eval_a : float
        First value to evaluate the derivative
    eval_b : float
        Second value to evaluate the derivative 

    Returns
    -------
    symbol_dif : string
        Simbolic solution to derivative 
    resul_a : float
        Solution to the derivative evaluated at the first value
    resul_b : float
        Solution to the derivative evaluated at the second value
    
    """

    x = sp.Symbol('x')
    
    #Conversion 
    expr = sp.sympify(function)
    
    #First derivative
    deriv = sp.diff(expr, x)
    
    #Evaluation
    resul_a = deriv.subs(x, eval_a)
    resul_b = deriv.subs(x, eval_b)
    
    return deriv, resul_a, resul_b


#derivative("x**2", 1.5, 2)
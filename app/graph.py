import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, diff, integrate, lambdify, sympify, sin, cos, exp, log, tan, sqrt, pi
from matplotlib.figure import Figure

def parse_function(expression):
    """
    Converts user input string into a sympy expression and numpy-compatible function
    
    Args:
        expression (str): Mathematical expression string
        
    Returns:
        tuple: (sympy expression, lambda function)
    """
    x = symbols('x')
    math_functions = {
        "sin": sin, 
        "cos": cos, 
        "exp": exp, 
        "log": log,
        "tan": tan, 
        "sqrt": sqrt, 
        "pi": pi
    }
    
    try:
        parsed_expr = sympify(expression.strip(), locals=math_functions)
        return parsed_expr, lambdify(x, parsed_expr, 'numpy')
    except Exception as e:
        print(f"Error parsing expression '{expression}': {e}")
        return None, None

def calculate_derivative(expression, order=1):
    """
    Calculate the nth order derivative of a function
    
    Args:
        expression: Sympy expression
        order (int): Order of the derivative (default=1)
        
    Returns:
        tuple: (derivative expression, lambda function)
    """
    x = symbols('x')
    
    try:
        derivative_expr = expression
        for _ in range(order):
            derivative_expr = diff(derivative_expr, x)
        
        derivative_func = lambdify(x, derivative_expr, 'numpy')
        return derivative_expr, derivative_func
    except Exception as e:
        print(f"Error calculating derivative: {e}")
        return None, None

def calculate_integral(expression, with_constant=True):
    """
    Calculate the indefinite integral of a function
    
    Args:
        expression: Sympy expression
        with_constant (bool): Whether to include constant of integration
        
    Returns:
        tuple: (integral expression, lambda function)
    """
    x = symbols('x')
    
    try:
        integral_expr = integrate(expression, x)
        integral_func = lambdify(x, integral_expr, 'numpy')
        return integral_expr, integral_func
    except Exception as e:
        print(f"Error calculating integral: {e}")
        return None, None
        
def find_critical_points(func, x_range, derivative_values=None):
    """
    Find critical points (where derivative = 0 or changes sign)
    
    Args:
        func: Lambda function of the original function
        x_range: numpy array of x values
        derivative_values: Pre-calculated derivative values (optional)
        
    Returns:
        list: Tuples of (x, y) for critical points
    """
    if derivative_values is None:
        # We'd need to calculate derivative values here
        # This is simplified and would need numerical differentiation
        # for a complete implementation without sympy
        return []
    
    critical_points = []
    
    # Find where derivative crosses zero
    for i in range(1, len(x_range)):
        if (derivative_values[i-1] < 0 and derivative_values[i] > 0) or \
           (derivative_values[i-1] > 0 and derivative_values[i] < 0):
            x = x_range[i]
            y = func(x)
            critical_points.append((x, y))
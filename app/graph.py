import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.optimize import approx_fprime
from scipy.integrate import quad

def parse_function(expression):
    """Converts user input into a Python function"""
    x = sp.symbols('x')
    func = sp.sympify(expression) 
    return sp.lambdify(x, func, 'numpy') 

def compute_derivative(func, x_values):
    """Numerical differentiation using approx_fprime"""
    epsilon = 1e-5  # Step size
    return np.array([approx_fprime([x], func, epsilon)[0] for x in x_values])

def compute_integral(func, x_values):
    """Computes definite integral from min to x"""
    integral_values = []
    for x in x_values:
        integral, _ = quad(func, x_values[0], x)
        integral_values.append(integral)
    return np.array(integral_values)

def plot_graph(expression, x_range):
    """Plots function, derivative, and integral"""
    x_values = np.linspace(x_range[0], x_range[1], 400)
    func = parse_function(expression)

    y_values = func(x_values)
    dy_values = compute_derivative(func, x_values)
    int_values = compute_integral(func, x_values)

    plt.figure(figsize=(10, 5))
    plt.plot(x_values, y_values, label="Function", color="blue")
    plt.plot(x_values, dy_values, label="Derivative", color="red", linestyle="dashed")
    plt.plot(x_values, int_values, label="Integral", color="green", linestyle="dotted")

    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Graph of {expression}")
    plt.grid()
    plt.show()

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, diff, integrate, lambdify, sympify, sin, cos, exp, log

class GraphingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculus-Powered Graphing App")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("Enter three functions (comma-separated, in terms of x):")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_field = QLineEdit("x**2 + 3*x + 5, sin(x), exp(x)")
        self.plot_button = QPushButton("Plot Graphs")

        self.canvas = FigureCanvas(plt.figure(figsize=(10, 6))) 

        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.canvas, stretch=1)  

        self.plot_button.clicked.connect(self.plot_functions)

    def plot_functions(self):
        expressions = self.input_field.text().split(",")  
        x_range = np.linspace(-10, 10, 400)
        x = symbols('x')

        math_functions = {"sin": sin, "cos": cos, "exp": exp, "log": log}

        fig, axes = plt.subplots(2, len(expressions), figsize=(12, 8))  

        if len(expressions) == 1:
            axes = np.array([[axes[0]], [axes[1]]])  

        combined_ax = fig.add_subplot(2, 1, 2)  

        for i, expr in enumerate(expressions):
            expr = expr.strip()
            
            try:
                parsed_expr = sympify(expr, locals=math_functions) 
                parsed_func = lambdify(x, parsed_expr, 'numpy')

                derivative_expr = diff(parsed_expr, x)
                integral_expr = integrate(parsed_expr, x)

                derivative_func = lambdify(x, derivative_expr, 'numpy')
                integral_func = lambdify(x, integral_expr, 'numpy')

                axes[0, i].plot(x_range, parsed_func(x_range), label=f"f(x) = {expr}", color='b')
                axes[0, i].set_title(f"Graph of {expr}")
                axes[0, i].legend()

                combined_ax.plot(x_range, parsed_func(x_range), label=f"f(x) = {expr}", linestyle='solid')
                combined_ax.plot(x_range, derivative_func(x_range), label=f"f'(x) = {derivative_expr}", linestyle='dashed')
                combined_ax.plot(x_range, integral_func(x_range), label=f"∫ f(x) dx = {integral_expr}", linestyle='dotted')

            except Exception as e:
                print(f"Error parsing expression '{expr}': {e}")

        combined_ax.set_title("Combined Graph of Functions, Derivatives, and Integrals")
        combined_ax.legend()
        
        self.canvas.figure.clf()  
        self.canvas.figure = fig
        self.canvas.draw()

app = QApplication(sys.argv)
window = GraphingApp()
window.showMaximized()
sys.exit(app.exec())

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt
from . import graph

class GraphingApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculus-Powered Graphing App")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label = QLabel("Enter function (in terms of x):")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.input_field = QLineEdit("x**2 + 3*x + 5")
        self.plot_button = QPushButton("Plot Graph")

        self.canvas = FigureCanvas(plt.figure())  # Matplotlib canvas

        # Stretch UI elements to fit full-screen view
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.plot_button)
        layout.addWidget(self.canvas, stretch=1)  # Expands to fit window size

        self.plot_button.clicked.connect(self.plot_function)

    def plot_function(self):
        expression = self.input_field.text()
        x_range = (-10, 10)

        plt.clf()
        graph.plot_graph(expression, x_range)

app = QApplication(sys.argv)
window = GraphingApp()
window.showMaximized()
sys.exit(app.exec())

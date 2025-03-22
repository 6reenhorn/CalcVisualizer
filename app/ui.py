from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QGroupBox, QGridLayout, QComboBox,
                            QSlider, QSpinBox, QTabWidget, QSplitter, QFrame, QCheckBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import sys
import numpy as np
from sympy import symbols, diff, integrate, lambdify, sympify, sin, cos, exp, log, tan, sqrt, pi

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor("#f0f0f0")
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)
        self.setMinimumSize(400, 300)

class GraphingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2e2e2e;
                color: white;
            }
            QLabel {
                color: white;
                font-size: 12px;
            }
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4a94ff;
            }
            QPushButton:pressed {
                background-color: #2a76ef;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 4px;
                margin-top: 12px;
                font-weight: bold;
                color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLineEdit {
                background-color: #3e3e3e;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
            }
            QComboBox {
                background-color: #3e3e3e;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #3e3e3e;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3a86ff;
                border: 1px solid #5c5c5c;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSpinBox {
                background-color: #3e3e3e;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
            }
            QCheckBox {
                color: white;
            }
            QFrame#graphFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #555;
            }
            QTabWidget::pane {
                border: 1px solid #555;
                background-color: #3e3e3e;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #2e2e2e;
                color: white;
                padding: 8px 16px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3a86ff;
            }
        """)

        self.setWindowTitle("Calculus-Powered Graphing App")
        self.setMinimumSize(1200, 800)

        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel (Controls)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel.setMaximumWidth(400)
        
        # Header
        header_label = QLabel("Calculus Visualizer")
        header_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #3a86ff; margin-bottom: 10px;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(header_label)
        
        # Function Input Group
        function_group = QGroupBox("Function Input")
        function_layout = QVBoxLayout(function_group)
        
        self.function_label = QLabel("Enter functions (comma-separated):")
        self.function_input = QLineEdit("x**2 + 3*x + 5, sin(x), exp(x)")
        self.function_input.setPlaceholderText("e.g., x**2 + 3*x + 5, sin(x), exp(x)")
        
        function_layout.addWidget(self.function_label)
        function_layout.addWidget(self.function_input)
        
        # Range settings
        range_layout = QGridLayout()
        self.x_min_label = QLabel("X Min:")
        self.x_min_input = QSpinBox()
        self.x_min_input.setRange(-100, 0)
        self.x_min_input.setValue(-10)
        
        self.x_max_label = QLabel("X Max:")
        self.x_max_input = QSpinBox()
        self.x_max_input.setRange(0, 100)
        self.x_max_input.setValue(10)
        
        self.resolution_label = QLabel("Resolution:")
        self.resolution_slider = QSlider(Qt.Orientation.Horizontal)
        self.resolution_slider.setRange(100, 1000)
        self.resolution_slider.setValue(400)
        self.resolution_slider.setTickInterval(100)
        self.resolution_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.resolution_value = QLabel("400 points")
        
        range_layout.addWidget(self.x_min_label, 0, 0)
        range_layout.addWidget(self.x_min_input, 0, 1)
        range_layout.addWidget(self.x_max_label, 0, 2)
        range_layout.addWidget(self.x_max_input, 0, 3)
        range_layout.addWidget(self.resolution_label, 1, 0)
        range_layout.addWidget(self.resolution_slider, 1, 1, 1, 2)
        range_layout.addWidget(self.resolution_value, 1, 3)
        
        function_layout.addLayout(range_layout)
        left_layout.addWidget(function_group)
        
        # Visualization Options
        viz_group = QGroupBox("Visualization Options")
        viz_layout = QVBoxLayout(viz_group)
        
        # Checkboxes for what to display
        display_layout = QGridLayout()
        self.show_function = QCheckBox("Show Functions")
        self.show_function.setChecked(True)
        self.show_derivative = QCheckBox("Show Derivatives")
        self.show_derivative.setChecked(True)
        self.show_integral = QCheckBox("Show Integrals")
        self.show_integral.setChecked(True)
        self.show_second_derivative = QCheckBox("Show Second Derivatives")
        
        display_layout.addWidget(self.show_function, 0, 0)
        display_layout.addWidget(self.show_derivative, 0, 1)
        display_layout.addWidget(self.show_integral, 1, 0)
        display_layout.addWidget(self.show_second_derivative, 1, 1)
        
        viz_layout.addLayout(display_layout)
        
        # Graph style options
        style_layout = QGridLayout()
        self.grid_lines = QCheckBox("Show Grid")
        self.grid_lines.setChecked(True)
        self.legend = QCheckBox("Show Legend")
        self.legend.setChecked(True)
        
        self.theme_label = QLabel("Graph Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Default", "Dark", "Seaborn", "Science", "High Contrast"])
        
        style_layout.addWidget(self.grid_lines, 0, 0)
        style_layout.addWidget(self.legend, 0, 1)
        style_layout.addWidget(self.theme_label, 1, 0)
        style_layout.addWidget(self.theme_combo, 1, 1)
        
        viz_layout.addLayout(style_layout)
        left_layout.addWidget(viz_group)
        
        # Action Buttons
        button_group = QGroupBox("Actions")
        button_layout = QGridLayout(button_group)
        
        self.plot_all_button = QPushButton("Plot All Graphs")
        self.plot_all_button.setMinimumHeight(40)
        self.plot_function_button = QPushButton("Plot Functions")
        self.plot_derivative_button = QPushButton("Plot Derivatives")
        self.plot_integral_button = QPushButton("Plot Integrals")
        self.clear_button = QPushButton("Clear All")
        self.clear_button.setStyleSheet("background-color: #ff3a5e;")
        self.save_button = QPushButton("Save Plots")
        self.save_button.setStyleSheet("background-color: #38b000;")
        
        button_layout.addWidget(self.plot_all_button, 0, 0, 1, 2)
        button_layout.addWidget(self.plot_function_button, 1, 0)
        button_layout.addWidget(self.plot_derivative_button, 1, 1)
        button_layout.addWidget(self.plot_integral_button, 2, 0)
        button_layout.addWidget(self.clear_button, 2, 1)
        button_layout.addWidget(self.save_button, 3, 0, 1, 2)
        
        left_layout.addWidget(button_group)
        left_layout.addStretch()
        
        # Credits at bottom
        credits = QLabel("Created by Group 5 - Calculus Visualization Project")
        credits.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credits.setStyleSheet("color: #888; font-style: italic;")
        left_layout.addWidget(credits)
        
        # Right panel (Graphs)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Create a frame for the graph area with white background
        graph_frame = QFrame()
        graph_frame.setObjectName("graphFrame")
        graph_layout = QVBoxLayout(graph_frame)
        
        # Create tab widget for different graph views
        self.tab_widget = QTabWidget()
        
        # Individual function tabs
        self.individual_tab = QWidget()
        individual_layout = QGridLayout(self.individual_tab)
        
        # Create individual canvases
        self.canvas1 = MplCanvas(width=5, height=4, dpi=100)
        self.canvas2 = MplCanvas(width=5, height=4, dpi=100)
        self.canvas3 = MplCanvas(width=5, height=4, dpi=100)
        
        individual_layout.addWidget(self.canvas1, 0, 0)
        individual_layout.addWidget(self.canvas2, 0, 1)
        individual_layout.addWidget(self.canvas3, 1, 0)
        
        # Combined tab
        self.combined_tab = QWidget()
        combined_layout = QVBoxLayout(self.combined_tab)
        self.combined_canvas = MplCanvas(width=10, height=8, dpi=100)
        combined_layout.addWidget(self.combined_canvas)
        
        # Analysis tab
        self.analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(self.analysis_tab)
        self.analysis_canvas = MplCanvas(width=10, height=8, dpi=100)
        analysis_layout.addWidget(self.analysis_canvas)
        
        # Add tabs to widget
        self.tab_widget.addTab(self.individual_tab, "Individual Functions")
        self.tab_widget.addTab(self.combined_tab, "Combined View")
        self.tab_widget.addTab(self.analysis_tab, "Analysis View")
        
        graph_layout.addWidget(self.tab_widget)
        right_layout.addWidget(graph_frame)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial splitter sizes (30% left, 70% right)
        splitter.setSizes([300, 700])
        
        # Connect signals
        self.plot_all_button.clicked.connect(self.plot_all_graphs)
        self.plot_function_button.clicked.connect(lambda: self.plot_specific("functions"))
        self.plot_derivative_button.clicked.connect(lambda: self.plot_specific("derivatives"))
        self.plot_integral_button.clicked.connect(lambda: self.plot_specific("integrals"))
        self.clear_button.clicked.connect(self.clear_plots)
        self.save_button.clicked.connect(self.save_plots)
        self.resolution_slider.valueChanged.connect(self.update_resolution_label)
        
        # Initialize with empty plots
        self.initialize_plots()
    
    def update_resolution_label(self, value):
        self.resolution_value.setText(f"{value} points")
    
    def initialize_plots(self):
        """Initialize empty plots with grids and labels"""
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas, self.analysis_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(True, linestyle='--', alpha=0.7)
            canvas.axes.set_xlabel('x')
            canvas.axes.set_ylabel('y')
            canvas.draw()
    
    def parse_function(self, expression):
        """Parse function expression using sympy"""
        x = symbols('x')
        math_functions = {"sin": sin, "cos": cos, "exp": exp, "log": log, 
                         "tan": tan, "sqrt": sqrt, "pi": pi}
        
        try:
            parsed_expr = sympify(expression.strip(), locals=math_functions)
            return parsed_expr, lambdify(x, parsed_expr, 'numpy')
        except Exception as e:
            print(f"Error parsing expression '{expression}': {e}")
            return None, None
    
    def plot_all_graphs(self):
        """Plot all graphs: individual functions, combined view, and analysis"""
        expressions = self.function_input.text().split(",")
        x_min = self.x_min_input.value()
        x_max = self.x_max_input.value()
        resolution = self.resolution_slider.value()
        
        x_range = np.linspace(x_min, x_max, resolution)
        x = symbols('x')
        
        # Clear all canvases
        for canvas in [self.canvas1, self.canvas2, self.canvas3]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
        
        self.combined_canvas.axes.clear()
        self.combined_canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
        
        self.analysis_canvas.axes.clear()
        self.analysis_canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
        
        # Colors for different functions
        colors = ['#3a86ff', '#ff3a5e', '#38b000', '#fcbf49', '#9d4edd']
        
        # Plot individual functions
        for i, expr in enumerate(expressions[:3]):  # Limit to 3 functions for individual plots
            parsed_expr, func = self.parse_function(expr)
            
            if parsed_expr is None or func is None:
                continue
                
            try:
                # Calculate function, derivative, and integral
                y_values = func(x_range)
                
                # Calculate derivative
                derivative_expr = diff(parsed_expr, x)
                derivative_func = lambdify(x, derivative_expr, 'numpy')
                d_values = derivative_func(x_range)
                
                # Second derivative if selected
                if self.show_second_derivative.isChecked():
                    second_derivative_expr = diff(derivative_expr, x)
                    second_derivative_func = lambdify(x, second_derivative_expr, 'numpy')
                    d2_values = second_derivative_func(x_range)
                
                # Calculate integral
                integral_expr = integrate(parsed_expr, x)
                integral_func = lambdify(x, integral_expr, 'numpy')
                int_values = integral_func(x_range)
                
                # Plot on individual canvas if available
                if i < 3:
                    canvas = [self.canvas1, self.canvas2, self.canvas3][i]
                    
                    if self.show_function.isChecked():
                        canvas.axes.plot(x_range, y_values, label=f"f(x) = {expr}", color=colors[0])
                    
                    if self.show_derivative.isChecked():
                        canvas.axes.plot(x_range, d_values, label=f"f'(x) = {derivative_expr}", 
                                        color=colors[1], linestyle='--')
                    
                    if self.show_second_derivative.isChecked():
                        canvas.axes.plot(x_range, d2_values, label=f"f''(x) = {second_derivative_expr}", 
                                        color=colors[4], linestyle=':')
                    
                    if self.show_integral.isChecked():
                        canvas.axes.plot(x_range, int_values, label=f"∫f(x)dx = {integral_expr}", 
                                        color=colors[2], linestyle='-.')
                    
                    canvas.axes.set_title(f"Graph of {expr}")
                    if self.legend.isChecked():
                        canvas.axes.legend()
                    canvas.draw()
                
                # Add to combined plot
                if self.show_function.isChecked():
                    self.combined_canvas.axes.plot(x_range, y_values, label=f"f(x) = {expr}", 
                                                 color=colors[i % len(colors)])
                
                if self.show_derivative.isChecked():
                    self.combined_canvas.axes.plot(x_range, d_values, label=f"f'(x) = {expr}", 
                                                 color=colors[i % len(colors)], linestyle='--')
                
                if self.show_integral.isChecked():
                    self.combined_canvas.axes.plot(x_range, int_values, label=f"∫f(x)dx = {expr}", 
                                                 color=colors[i % len(colors)], linestyle='-.')
                
                # Analysis view - overlay function, derivative, integral for comparison
                self.analysis_canvas.axes.plot(x_range, y_values, label=f"f(x) = {expr}", 
                                             color=colors[i % len(colors)])
                
                # Add critical points to analysis (where derivative = 0)
                critical_x = []
                for j in range(1, len(x_range)):
                    if (d_values[j-1] < 0 and d_values[j] > 0) or (d_values[j-1] > 0 and d_values[j] < 0):
                        critical_x.append(x_range[j])
                        self.analysis_canvas.axes.plot(x_range[j], y_values[j], 'o', 
                                                    color=colors[i % len(colors)], markersize=8)
                
            except Exception as e:
                print(f"Error plotting {expr}: {e}")
        
        self.combined_canvas.axes.set_title("Combined Functions")
        if self.legend.isChecked():
            self.combined_canvas.axes.legend()
        self.combined_canvas.draw()
        
        self.analysis_canvas.axes.set_title("Analysis View with Critical Points")
        if self.legend.isChecked():
            self.analysis_canvas.axes.legend()
        self.analysis_canvas.draw()
        
        # Switch to combined tab to show results
        self.tab_widget.setCurrentIndex(1)
    
    def plot_specific(self, plot_type):
        """Plot only specific type (functions, derivatives, or integrals)"""
        expressions = self.function_input.text().split(",")
        x_min = self.x_min_input.value()
        x_max = self.x_max_input.value()
        resolution = self.resolution_slider.value()
        
        x_range = np.linspace(x_min, x_max, resolution)
        x = symbols('x')
        
        # Clear canvases
        for canvas in [self.canvas1, self.canvas2, self.canvas3]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
        
        self.combined_canvas.axes.clear()
        self.combined_canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
        
        # Colors for different functions
        colors = ['#3a86ff', '#ff3a5e', '#38b000', '#fcbf49', '#9d4edd']
        
        for i, expr in enumerate(expressions[:3]):
            parsed_expr, func = self.parse_function(expr)
            
            if parsed_expr is None or func is None:
                continue
                
            try:
                if plot_type == "functions":
                    y_values = func(x_range)
                    
                    # Individual canvas
                    if i < 3:
                        canvas = [self.canvas1, self.canvas2, self.canvas3][i]
                        canvas.axes.plot(x_range, y_values, label=f"f(x) = {expr}", color=colors[0])
                        canvas.axes.set_title(f"Function: {expr}")
                        if self.legend.isChecked():
                            canvas.axes.legend()
                        canvas.draw()
                    
                    # Combined canvas
                    self.combined_canvas.axes.plot(x_range, y_values, label=f"f(x) = {expr}", 
                                                 color=colors[i % len(colors)])
                
                elif plot_type == "derivatives":
                    derivative_expr = diff(parsed_expr, x)
                    derivative_func = lambdify(x, derivative_expr, 'numpy')
                    d_values = derivative_func(x_range)
                    
                    # Individual canvas
                    if i < 3:
                        canvas = [self.canvas1, self.canvas2, self.canvas3][i]
                        canvas.axes.plot(x_range, d_values, label=f"f'(x) = {derivative_expr}", color=colors[1])
                        canvas.axes.set_title(f"Derivative of {expr}")
                        if self.legend.isChecked():
                            canvas.axes.legend()
                        canvas.draw()
                    
                    # Combined canvas
                    self.combined_canvas.axes.plot(x_range, d_values, label=f"f'(x) = {expr}", 
                                                 color=colors[i % len(colors)])
                
                elif plot_type == "integrals":
                    integral_expr = integrate(parsed_expr, x)
                    integral_func = lambdify(x, integral_expr, 'numpy')
                    int_values = integral_func(x_range)
                    
                    # Individual canvas
                    if i < 3:
                        canvas = [self.canvas1, self.canvas2, self.canvas3][i]
                        canvas.axes.plot(x_range, int_values, label=f"∫f(x)dx = {integral_expr}", color=colors[2])
                        canvas.axes.set_title(f"Integral of {expr}")
                        if self.legend.isChecked():
                            canvas.axes.legend()
                        canvas.draw()
                    
                    # Combined canvas
                    self.combined_canvas.axes.plot(x_range, int_values, label=f"∫f(x)dx = {expr}", 
                                                 color=colors[i % len(colors)])
            
            except Exception as e:
                print(f"Error plotting {plot_type} for {expr}: {e}")
        
        # Set title for combined plot
        if plot_type == "functions":
            self.combined_canvas.axes.set_title("All Functions")
        elif plot_type == "derivatives":
            self.combined_canvas.axes.set_title("All Derivatives")
        elif plot_type == "integrals":
            self.combined_canvas.axes.set_title("All Integrals")
        
        if self.legend.isChecked():
            self.combined_canvas.axes.legend()
        self.combined_canvas.draw()
        
        # Switch to appropriate tab
        self.tab_widget.setCurrentIndex(1)
    
    def clear_plots(self):
        """Clear all plots"""
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas, self.analysis_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            canvas.axes.set_xlabel('x')
            canvas.axes.set_ylabel('y')
            canvas.draw()
    
    def save_plots(self):
        """Save all plots as images"""
        # This is a placeholder - in a real app, you'd use file dialogs
        try:
            self.canvas1.fig.savefig("function1.png")
            self.canvas2.fig.savefig("function2.png")
            self.canvas3.fig.savefig("function3.png")
            self.combined_canvas.fig.savefig("combined_view.png")
            self.analysis_canvas.fig.savefig("analysis_view.png")
            # You would normally show a success message here
            print("Plots saved successfully!")
        except Exception as e:
            print(f"Error saving plots: {e}")

# This would be in main.py
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingApp()
    window.showMaximized()
    sys.exit(app.exec())
import sys
import os
import numpy as np
from datetime import datetime
from sympy import symbols, sympify, diff, integrate, sin, cos, tan, exp, log, sqrt, pi
from sympy.utilities.lambdify import lambdify
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QGroupBox, QLabel, QLineEdit, QPushButton, QGridLayout, QSlider, 
                           QSpinBox, QComboBox, QCheckBox, QSplitter, QScrollArea, QFrame,
                           QTabWidget, QFileDialog, QMessageBox, QDoubleSpinBox)
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from calcvisualizer.ui.canvas import MplCanvas

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
            QSpinBox, QDoubleSpinBox {
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
        
        # X Range settings
        range_layout = QGridLayout()
        self.x_min_label = QLabel("X Min:")
        self.x_min_input = QSpinBox()
        self.x_min_input.setRange(-100, 0)
        self.x_min_input.setValue(-10)
        
        self.x_max_label = QLabel("X Max:")
        self.x_max_input = QSpinBox()
        self.x_max_input.setRange(0, 100)
        self.x_max_input.setValue(10)
        
        range_layout.addWidget(self.x_min_label, 0, 0)
        range_layout.addWidget(self.x_min_input, 0, 1)
        range_layout.addWidget(self.x_max_label, 0, 2)
        range_layout.addWidget(self.x_max_input, 0, 3)
        
        # Y Range settings (new)
        self.y_min_label = QLabel("Y Min:")
        self.y_min_input = QDoubleSpinBox()
        self.y_min_input.setRange(-1000, 0)
        self.y_min_input.setValue(-10)
        self.y_min_input.setDecimals(1)
        
        self.y_max_label = QLabel("Y Max:")
        self.y_max_input = QDoubleSpinBox()
        self.y_max_input.setRange(0, 1000)
        self.y_max_input.setValue(10)
        self.y_max_input.setDecimals(1)
        
        self.auto_scale_y = QCheckBox("Auto-scale Y")
        self.auto_scale_y.setChecked(True)
        
        range_layout.addWidget(self.y_min_label, 1, 0)
        range_layout.addWidget(self.y_min_input, 1, 1)
        range_layout.addWidget(self.y_max_label, 1, 2)
        range_layout.addWidget(self.y_max_input, 1, 3)
        range_layout.addWidget(self.auto_scale_y, 2, 0, 1, 4)
        
        # Y scale options (new)
        self.y_scale_label = QLabel("Y Scale:")
        self.y_scale_combo = QComboBox()
        self.y_scale_combo.addItems(["Linear", "Logarithmic", "Symmetric Log"])
        
        range_layout.addWidget(self.y_scale_label, 3, 0)
        range_layout.addWidget(self.y_scale_combo, 3, 1, 1, 3)
        
        # Resolution settings
        self.resolution_label = QLabel("Resolution:")
        self.resolution_slider = QSlider(Qt.Orientation.Horizontal)
        self.resolution_slider.setRange(100, 1000)
        self.resolution_slider.setValue(400)
        self.resolution_slider.setTickInterval(100)
        self.resolution_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.resolution_value = QLabel("400 points")
        
        range_layout.addWidget(self.resolution_label, 4, 0)
        range_layout.addWidget(self.resolution_slider, 4, 1, 1, 2)
        range_layout.addWidget(self.resolution_value, 4, 3)
        
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
        self.normalize = QCheckBox("Normalize Functions") # New option
        self.normalize.setChecked(False)
        
        self.theme_label = QLabel("Graph Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Default", "Dark", "Seaborn", "Science", "High Contrast"])
        
        style_layout.addWidget(self.grid_lines, 0, 0)
        style_layout.addWidget(self.legend, 0, 1)
        style_layout.addWidget(self.normalize, 1, 0)
        style_layout.addWidget(self.theme_label, 2, 0)
        style_layout.addWidget(self.theme_combo, 2, 1)
        
        viz_layout.addLayout(style_layout)
        left_layout.addWidget(viz_group)
        
        # Function Visibility Group (new)
        visibility_group = QGroupBox("Function Visibility")
        visibility_layout = QVBoxLayout(visibility_group)
        self.function_visibility_checkboxes = []
        # Will be populated dynamically
        
        self.update_visibility_button = QPushButton("Update Visibility")
        visibility_layout.addWidget(self.update_visibility_button)
        left_layout.addWidget(visibility_group)
        
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
        credits = QLabel("Created by _Nu1L - Calculus Visualization Project")
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
        
        # New Entire View tab
        self.entire_tab = QWidget()
        entire_layout = QVBoxLayout(self.entire_tab)

        # Top section for individual function plots
        entire_top = QWidget()
        entire_top_layout = QHBoxLayout(entire_top)
        entire_top_layout.setContentsMargins(0, 0, 0, 0)

        # Will dynamically create/populate these in plot_all_graphs
        self.function_canvases = []
        self.entire_top_scrollarea = QScrollArea()
        self.entire_top_scrollarea.setWidgetResizable(True)
        self.entire_top_scrollcontent = QWidget()
        self.entire_top_scrolllayout = QHBoxLayout(self.entire_top_scrollcontent)
        self.entire_top_scrollarea.setWidget(self.entire_top_scrollcontent)
        entire_top_layout.addWidget(self.entire_top_scrollarea)
        entire_layout.addWidget(entire_top, stretch=1)  # 2:1 ratio for top:bottom
        
        # Bottom section for combined and analysis views
        entire_bottom = QWidget()
        entire_bottom_layout = QHBoxLayout(entire_bottom)
        entire_bottom_layout.setContentsMargins(0, 0, 0, 0)

        entire_bottom_layout.setSpacing(5)
        
        # Bottom left: Combined view
        entire_bottom_left = QWidget()
        entire_bottom_left_layout = QVBoxLayout(entire_bottom_left)
        entire_bottom_left_layout.setContentsMargins(0, 0, 0, 0)
        self.combined_small_canvas = MplCanvas(width=5, height=4, dpi=100)
        entire_bottom_left_layout.addWidget(self.combined_small_canvas)
        combined_label = QLabel("Combined View")
        combined_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        combined_label.setStyleSheet("font-weight: bold;")
        entire_bottom_left_layout.addWidget(combined_label)

        
        # Bottom right: Analysis view
        entire_bottom_right = QWidget()
        entire_bottom_right_layout = QVBoxLayout(entire_bottom_right)
        entire_bottom_right_layout.setContentsMargins(0, 0, 0, 0)
        self.analysis_small_canvas = MplCanvas(width=5, height=4, dpi=100)
        entire_bottom_right_layout.addWidget(self.analysis_small_canvas)
        analysis_label = QLabel("Analysis View")
        analysis_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        analysis_label.setStyleSheet("font-weight: bold;")
        entire_bottom_right_layout.addWidget(analysis_label)
        
        entire_bottom_layout.addWidget(entire_bottom_left)
        entire_bottom_layout.addWidget(entire_bottom_right)
        entire_layout.addWidget(entire_bottom, stretch=1) 
        
        # Individual function tabs
        self.individual_tab = QWidget()
        individual_layout = QGridLayout(self.individual_tab)
        
        # Create individual canvases
        self.canvas1 = MplCanvas(width=6, height=4, dpi=100)
        self.canvas2 = MplCanvas(width=6, height=4, dpi=100)
        self.canvas3 = MplCanvas(width=6, height=4, dpi=100)
        
        individual_layout.addWidget(self.canvas1, 0, 0)
        individual_layout.addWidget(self.canvas2, 0, 1)
        individual_layout.addWidget(self.canvas3, 1, 0)
        
        # Combined tab
        self.combined_tab = QWidget()
        combined_layout = QVBoxLayout(self.combined_tab)
        self.combined_canvas = MplCanvas(width=10, height=12, dpi=100)
        combined_layout.addWidget(self.combined_canvas)
        
        # Analysis tab
        self.analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(self.analysis_tab)
        self.analysis_canvas = MplCanvas(width=10, height=12, dpi=100)
        analysis_layout.addWidget(self.analysis_canvas)
        
        # Add tabs to widget in the new order
        self.tab_widget.addTab(self.entire_tab, "Entire View")
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
        self.update_visibility_button.clicked.connect(self.plot_all_graphs)
        self.auto_scale_y.toggled.connect(self.toggle_y_scale_controls)
        
        # Initialize visibility and function list
        self.function_visibility = {}
        
        # Initialize with empty plots
        self.initialize_plots()
        
    def toggle_y_scale_controls(self, checked):
        """Enable/disable Y scale controls based on auto-scale checkbox"""
        self.y_min_input.setEnabled(not checked)
        self.y_max_input.setEnabled(not checked)
    
    def update_resolution_label(self, value):
        self.resolution_value.setText(f"{value} points")
    
    def initialize_plots(self):
        """Initialize empty plots with grids and labels"""
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas, 
                      self.analysis_canvas, self.combined_small_canvas, self.analysis_small_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(True, linestyle='--', alpha=0.7)
            canvas.axes.set_xlabel('x')
            canvas.axes.set_ylabel('y')
            canvas.draw()
    
    def create_dynamic_canvases(self, expressions):
        """Create canvases dynamically based on the number of functions"""
        # Clear any existing content
        self.function_canvases = []
        
        # Clear layout
        while self.entire_top_scrolllayout.count():
            item = self.entire_top_scrolllayout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        # Create a canvas for each function
        for i, expr in enumerate(expressions):
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Create canvas
            canvas = MplCanvas(width=4, height=3, dpi=100)
            self.function_canvases.append(canvas)
            container_layout.addWidget(canvas)
            
            # Add label
            label = QLabel(f"Function {i+1}: {expr}")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setMargin(15)
            label.setStyleSheet("font-weight: bold;")
            label.setWordWrap(True)
            container_layout.addWidget(label)
            
            # Add to layout
            self.entire_top_scrolllayout.addWidget(container)
        
        # Update function visibility checkboxes
        self.update_function_visibility_checkboxes(expressions)
    
    def update_function_visibility_checkboxes(self, expressions):
        """Update the function visibility checkboxes based on the current functions"""
        # Clear existing checkboxes
        while self.function_visibility_checkboxes:
            checkbox = self.function_visibility_checkboxes.pop()
            checkbox.setParent(None)
        
        # Find the layout
        layout = None
        for i in range(self.layout().count()):
            if self.layout().itemAt(i).widget().objectName() == "visibility_group":
                layout = self.layout().itemAt(i).widget().layout()
                break
        
        # If we have a layout and expressions, add checkboxes
        if layout:
            # Create checkboxes for each function
            for i, expr in enumerate(expressions):
                function_checkbox = QCheckBox(f"Show: {expr}")
                function_checkbox.setChecked(True)
                # Store the function index with the checkbox
                function_checkbox.setProperty("function_index", i)
                # Add to our list and layout
                self.function_visibility_checkboxes.append(function_checkbox)
                self.function_visibility[i] = True
                layout.insertWidget(i, function_checkbox)
    
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
    
    def set_y_scale(self, ax):
        """Set the y-scale for an axis based on user selection"""
        scale_type = self.y_scale_combo.currentText()
        if scale_type == "Logarithmic":
            # Use symlog for handling negative values
            ax.set_yscale('log')
            # Add a small positive value to avoid log(0) issues
            ax.set_ylim(bottom=max(1e-10, ax.get_ylim()[0]))
        elif scale_type == "Symmetric Log":
            # Symlog can handle negative values
            ax.set_yscale('symlog', linthresh=0.1)
        else:  # Linear is default
            ax.set_yscale('linear')
    
    def apply_axis_limits(self, ax):
        """Apply user-defined axis limits if auto-scale is off"""
        if not self.auto_scale_y.isChecked():
            y_min = self.y_min_input.value()
            y_max = self.y_max_input.value()
            ax.set_ylim(y_min, y_max)
    
    def plot_all_graphs(self):
        """Plot all graphs: individual functions, combined view, and analysis"""
        expressions = [expr.strip() for expr in self.function_input.text().split(",") if expr.strip()]
        x_min = self.x_min_input.value()
        x_max = self.x_max_input.value()
        resolution = self.resolution_slider.value()
        
        x_range = np.linspace(x_min, x_max, resolution)
        x = symbols('x')
        
        # Create dynamic canvases for the Entire View tab
        self.create_dynamic_canvases(expressions)
        
        # Clear all canvases
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas, 
                      self.analysis_canvas, self.combined_small_canvas, self.analysis_small_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            self.set_y_scale(canvas.axes)
        
        # Clear the function canvases
        for canvas in self.function_canvases:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            self.set_y_scale(canvas.axes)
        
        # Colors for different functions
        colors = ['#3a86ff', '#ff3a5e', '#38b000', '#fcbf49', '#9d4edd', 
                 '#f72585', '#4cc9f0', '#fb8500', '#0077b6', '#7209b7']
        
        # For displaying group plots in Entire View
        all_functions_data = []
        all_derivatives_data = []
        all_integrals_data = []
        all_critical_points = []
        
        # Update function visibility from checkboxes
        for checkbox in self.function_visibility_checkboxes:
            index = checkbox.property("function_index")
            self.function_visibility[index] = checkbox.isChecked()
        
        # Plot individual functions
        for i, expr in enumerate(expressions):
            # Skip if function is hidden
            if i in self.function_visibility and not self.function_visibility[i]:
                continue
                
            parsed_expr, func = self.parse_function(expr)
            
            if parsed_expr is None or func is None:
                continue
                
            try:
                # Calculate function, derivative, and integral
                y_values = func(x_range)
                
                # Handle NaN or inf values for proper plotting
                y_values = np.nan_to_num(y_values, nan=0.0, posinf=1e10, neginf=-1e10)
                
                # Normalize values if selected
                if self.normalize.isChecked():
                    # Avoid division by zero
                    y_max = max(abs(np.max(y_values)), abs(np.min(y_values)))
                    if y_max > 0:
                        y_values = y_values / y_max
                
                # Calculate derivative
                derivative_expr = diff(parsed_expr, x)
                derivative_func = lambdify(x, derivative_expr, 'numpy')
                d_values = derivative_func(x_range)
                d_values = np.nan_to_num(d_values, nan=0.0, posinf=1e10, neginf=-1e10)
                
                if self.normalize.isChecked():
                    d_max = max(abs(np.max(d_values)), abs(np.min(d_values)))
                    if d_max > 0:
                        d_values = d_values / d_max
                
                # Second derivative if selected
                if self.show_second_derivative.isChecked():
                    second_derivative_expr = diff(derivative_expr, x)
                    second_derivative_func = lambdify(x, second_derivative_expr, 'numpy')
                    d2_values = second_derivative_func(x_range)
                    d2_values = np.nan_to_num(d2_values, nan=0.0, posinf=1e10, neginf=-1e10)
                    
                    if self.normalize.isChecked():
                        d2_max = max(abs(np.max(d2_values)), abs(np.min(d2_values)))
                        if d2_max > 0:
                            d2_values = d2_values / d2_max
                
                # Calculate integral
                integral_expr = integrate(parsed_expr, x)
                integral_func = lambdify(x, integral_expr, 'numpy')
                int_values = integral_func(x_range)
                int_values = np.nan_to_num(int_values, nan=0.0, posinf=1e10, neginf=-1e10)
                
                if self.normalize.isChecked():
                    int_max = max(abs(np.max(int_values)), abs(np.min(int_values)))
                    if int_max > 0:
                        int_values = int_values / int_max
                
                # Store data for entire view
                all_functions_data.append((expr, x_range, y_values, colors[i % len(colors)]))
                all_derivatives_data.append((expr, derivative_expr, x_range, d_values, colors[i % len(colors)]))
                all_integrals_data.append((expr, integral_expr, x_range, int_values, colors[i % len(colors)]))
                
                # Find critical points (where derivative = 0)
                critical_points = []
                for j in range(1, len(x_range) - 1):
                    if (d_values[j-1] * d_values[j+1] <= 0) or abs(d_values[j]) < 1e-6:
                        critical_points.append((x_range[j], y_values[j]))
                
                all_critical_points.extend([(expr, cp[0], cp[1], colors[i % len(colors)]) for cp in critical_points])
                
                # Plot on individual canvases
                canvas = None
                if i == 0:
                    canvas = self.canvas1
                elif i == 1:
                    canvas = self.canvas2
                elif i == 2:
                    canvas = self.canvas3
                
                # Also plot on the function-specific canvas in Entire View
                func_canvas = self.function_canvases[i] if i < len(self.function_canvases) else None
                
                for current_canvas in [canvas, func_canvas]:
                    if current_canvas is not None:
                        if self.show_function.isChecked():
                            current_canvas.axes.plot(x_range, y_values, color=colors[i % len(colors)], 
                                                   linewidth=2, label=f"f(x) = {expr}")
                        
                        if self.show_derivative.isChecked():
                            current_canvas.axes.plot(x_range, d_values, color=colors[i % len(colors)], 
                                                   linewidth=1.5, linestyle='--', 
                                                   label=f"f'(x) = {derivative_expr}")
                        
                        if self.show_second_derivative.isChecked():
                            current_canvas.axes.plot(x_range, d2_values, color=colors[i % len(colors)], 
                                                   linewidth=1, linestyle='-.', 
                                                   label=f"f''(x) = {second_derivative_expr}")
                        
                        if self.show_integral.isChecked():
                            current_canvas.axes.plot(x_range, int_values, color=colors[i % len(colors)], 
                                                   linewidth=1.5, linestyle=':', 
                                                   label=f"∫f(x)dx = {integral_expr} + C")
                        
                        # Plot critical points
                        for cp in critical_points:
                            current_canvas.axes.plot(cp[0], cp[1], 'o', color=colors[i % len(colors)], 
                                                  markersize=6)
                        
                        current_canvas.axes.set_xlabel('x')
                        current_canvas.axes.set_ylabel('y')
                        current_canvas.axes.set_title(f"Function: {expr}")
                        
                        if self.legend.isChecked():
                            current_canvas.axes.legend(loc='upper left', fontsize='small')
                        
                        # Apply axis limits if auto-scale is disabled
                        self.apply_axis_limits(current_canvas.axes)
                        
                        # Draw the plots
                        current_canvas.draw()
            
            except Exception as e:
                print(f"Error plotting function '{expr}': {e}")
        
        # Plot combined view on both big and small canvases
        for current_canvas in [self.combined_canvas, self.combined_small_canvas]:
            for data in all_functions_data:
                if self.show_function.isChecked():
                    current_canvas.axes.plot(data[1], data[2], color=data[3], linewidth=2, 
                                          label=f"f(x) = {data[0]}")
            
            # Set axis limits for combined view
            current_canvas.axes.set_xlabel('x')
            current_canvas.axes.set_ylabel('y')
            current_canvas.axes.set_title("Combined Functions")
            
            if self.legend.isChecked():
                current_canvas.axes.legend(loc='upper left', fontsize='small')
            
            # Apply theme settings
            self.apply_plot_theme(current_canvas.axes)
            
            # Apply axis limits if auto-scale is disabled
            self.apply_axis_limits(current_canvas.axes)
            
            # Draw the plots
            current_canvas.draw()
        
        # Plot analysis view on both big and small canvases
        for current_canvas in [self.analysis_canvas, self.analysis_small_canvas]:
            # Plot derivatives
            if self.show_derivative.isChecked():
                for data in all_derivatives_data:
                    current_canvas.axes.plot(data[2], data[3], color=data[4], linewidth=1.5, 
                                          linestyle='--', label=f"d/dx({data[0]})")
            
            # Plot critical points
            for point in all_critical_points:
                current_canvas.axes.plot(point[1], point[2], 'o', color=point[3], markersize=6)
                current_canvas.axes.annotate(f"({point[1]:.2f}, {point[2]:.2f})", 
                                          (point[1], point[2]), 
                                          textcoords="offset points", 
                                          xytext=(0,10), 
                                          ha='center')
            
            current_canvas.axes.set_xlabel('x')
            current_canvas.axes.set_ylabel('y')
            current_canvas.axes.set_title("Derivatives and Critical Points")
            
            if self.legend.isChecked():
                current_canvas.axes.legend(loc='upper left', fontsize='small')
            
            # Apply theme settings
            self.apply_plot_theme(current_canvas.axes)
            
            # Apply axis limits if auto-scale is disabled
            self.apply_axis_limits(current_canvas.axes)
            
            # Draw the plots
            current_canvas.draw()
    
    def plot_specific(self, plot_type):
        """Plot specific graph types (functions, derivatives, or integrals)"""
        expressions = [expr.strip() for expr in self.function_input.text().split(",") if expr.strip()]
        x_min = self.x_min_input.value()
        x_max = self.x_max_input.value()
        resolution = self.resolution_slider.value()
        
        x_range = np.linspace(x_min, x_max, resolution)
        x = symbols('x')
        
        # Clear canvases
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            self.set_y_scale(canvas.axes)
        
        # Colors for different functions
        colors = ['#3a86ff', '#ff3a5e', '#38b000', '#fcbf49', '#9d4edd', 
                 '#f72585', '#4cc9f0', '#fb8500', '#0077b6', '#7209b7']
        
        # Plot selected graph type
        for i, expr in enumerate(expressions):
            # Skip if function is hidden
            if i in self.function_visibility and not self.function_visibility[i]:
                continue
                
            parsed_expr, func = self.parse_function(expr)
            
            if parsed_expr is None or func is None:
                continue
                
            try:
                canvas = None
                if i == 0:
                    canvas = self.canvas1
                elif i == 1:
                    canvas = self.canvas2
                elif i == 2:
                    canvas = self.canvas3
                
                if canvas is None:
                    continue
                
                # Calculate and plot based on type
                if plot_type == "functions":
                    y_values = func(x_range)
                    y_values = np.nan_to_num(y_values, nan=0.0, posinf=1e10, neginf=-1e10)
                    
                    if self.normalize.isChecked():
                        y_max = max(abs(np.max(y_values)), abs(np.min(y_values)))
                        if y_max > 0:
                            y_values = y_values / y_max
                    
                    canvas.axes.plot(x_range, y_values, color=colors[i % len(colors)], 
                                   linewidth=2, label=f"f(x) = {expr}")
                    canvas.axes.set_title(f"Function: {expr}")
                
                elif plot_type == "derivatives":
                    derivative_expr = diff(parsed_expr, x)
                    derivative_func = lambdify(x, derivative_expr, 'numpy')
                    d_values = derivative_func(x_range)
                    d_values = np.nan_to_num(d_values, nan=0.0, posinf=1e10, neginf=-1e10)
                    
                    if self.normalize.isChecked():
                        d_max = max(abs(np.max(d_values)), abs(np.min(d_values)))
                        if d_max > 0:
                            d_values = d_values / d_max
                    
                    canvas.axes.plot(x_range, d_values, color=colors[i % len(colors)], 
                                   linewidth=2, label=f"f'(x) = {derivative_expr}")
                    canvas.axes.set_title(f"Derivative: {derivative_expr}")
                    
                    # Plot critical points
                    critical_points = []
                    for j in range(1, len(x_range) - 1):
                        if (d_values[j-1] * d_values[j+1] <= 0) or abs(d_values[j]) < 1e-6:
                            y_val = func(x_range[j])
                            critical_points.append((x_range[j], y_val))
                    
                    # Plot the critical points on function graph
                    y_values = func(x_range)
                    y_values = np.nan_to_num(y_values, nan=0.0, posinf=1e10, neginf=-1e10)
                    canvas.axes.plot(x_range, y_values, color=colors[i % len(colors)], 
                                   linewidth=1, linestyle=':', alpha=0.5)
                    
                    for cp in critical_points:
                        canvas.axes.plot(cp[0], cp[1], 'o', color=colors[i % len(colors)], 
                                       markersize=6)
                        canvas.axes.annotate(f"({cp[0]:.2f}, {cp[1]:.2f})", 
                                           (cp[0], cp[1]), 
                                           textcoords="offset points", 
                                           xytext=(0,10), 
                                           ha='center')
                
                elif plot_type == "integrals":
                    integral_expr = integrate(parsed_expr, x)
                    integral_func = lambdify(x, integral_expr, 'numpy')
                    int_values = integral_func(x_range)
                    int_values = np.nan_to_num(int_values, nan=0.0, posinf=1e10, neginf=-1e10)
                    
                    if self.normalize.isChecked():
                        int_max = max(abs(np.max(int_values)), abs(np.min(int_values)))
                        if int_max > 0:
                            int_values = int_values / int_max
                    
                    canvas.axes.plot(x_range, int_values, color=colors[i % len(colors)], 
                                   linewidth=2, label=f"∫f(x)dx = {integral_expr} + C")
                    canvas.axes.set_title(f"Integral: {integral_expr} + C")
                
                # Set axis labels
                canvas.axes.set_xlabel('x')
                canvas.axes.set_ylabel('y')
                
                if self.legend.isChecked():
                    canvas.axes.legend(loc='upper left', fontsize='small')
                
                # Apply theme settings
                self.apply_plot_theme(canvas.axes)
                
                # Apply axis limits if auto-scale is disabled
                self.apply_axis_limits(canvas.axes)
                
                # Also plot on combined view
                if self.combined_canvas is not None:
                    if plot_type == "functions":
                        self.combined_canvas.axes.plot(x_range, y_values, color=colors[i % len(colors)], 
                                                    linewidth=2, label=f"f(x) = {expr}")
                    elif plot_type == "derivatives":
                        self.combined_canvas.axes.plot(x_range, d_values, color=colors[i % len(colors)], 
                                                    linewidth=2, label=f"f'(x) = {derivative_expr}")
                    elif plot_type == "integrals":
                        self.combined_canvas.axes.plot(x_range, int_values, color=colors[i % len(colors)], 
                                                    linewidth=2, label=f"∫f(x)dx = {integral_expr} + C")
                    
                    self.combined_canvas.axes.set_xlabel('x')
                    self.combined_canvas.axes.set_ylabel('y')
                    self.combined_canvas.axes.set_title(f"Combined {plot_type.capitalize()}")
                    
                    if self.legend.isChecked():
                        self.combined_canvas.axes.legend(loc='upper left', fontsize='small')
                    
                    # Apply theme settings
                    self.apply_plot_theme(self.combined_canvas.axes)
                    
                    # Apply axis limits if auto-scale is disabled
                    self.apply_axis_limits(self.combined_canvas.axes)
                    
                    # Draw the plots
                    self.combined_canvas.draw()
                
                # Draw the plots
                canvas.draw()
            
            except Exception as e:
                print(f"Error plotting {plot_type} for function '{expr}': {e}")
    
    def apply_plot_theme(self, ax):
        """Apply the selected theme to a matplotlib axis"""
        theme = self.theme_combo.currentText()
        if theme == "Dark":
            ax.set_facecolor('#2e2e2e')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')
            if self.grid_lines.isChecked():
                ax.grid(True, linestyle='--', alpha=0.7, color='#555555')
        
        elif theme == "Seaborn":
            ax.set_facecolor('#f0f0f0')
            ax.tick_params(colors='#333333')
            ax.xaxis.label.set_color('#333333')
            ax.yaxis.label.set_color('#333333')
            ax.title.set_color('#333333')
            for spine in ax.spines.values():
                spine.set_color('#333333')
            if self.grid_lines.isChecked():
                ax.grid(True, linestyle='-', alpha=0.2, color='#333333')
        
        elif theme == "Science":
            ax.set_facecolor('white')
            ax.tick_params(colors='black')
            ax.xaxis.label.set_color('black')
            ax.yaxis.label.set_color('black')
            ax.title.set_color('black')
            for spine in ax.spines.values():
                spine.set_color('black')
                spine.set_linewidth(1.5)
            if self.grid_lines.isChecked():
                ax.grid(True, linestyle=':', alpha=0.3, color='black')
        
        elif theme == "High Contrast":
            ax.set_facecolor('black')
            ax.tick_params(colors='white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
            for spine in ax.spines.values():
                spine.set_color('white')
                spine.set_linewidth(2)
            if self.grid_lines.isChecked():
                ax.grid(True, linestyle='-', alpha=0.5, color='#ffffff')
    
    def clear_plots(self):
        """Clear all plots and reset to default state"""
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas, 
                      self.analysis_canvas, self.combined_small_canvas, self.analysis_small_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            canvas.axes.set_xlabel('x')
            canvas.axes.set_ylabel('y')
            canvas.draw()
        
        # Clear function canvases too
        for canvas in self.function_canvases:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            canvas.axes.set_xlabel('x')
            canvas.axes.set_ylabel('y')
            canvas.draw()
    
    def save_plots(self):
        """Save all plots to a directory"""
        try:
            # Get directory to save to
            save_dir = QFileDialog.getExistingDirectory(self, "Select Directory to Save Plots")
            
            if not save_dir:
                return
            
            # Get timestamp for filenames
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save all canvases
            count = 0
            for i, canvas in enumerate([self.canvas1, self.canvas2, self.canvas3, self.combined_canvas, 
                                      self.analysis_canvas]):
                # Skip empty plots
                if len(canvas.axes.lines) == 0 and len(canvas.axes.collections) == 0:
                    continue
                
                # Create filename
                if i == 0:
                    filename = f"function1_{timestamp}.png"
                elif i == 1:
                    filename = f"function2_{timestamp}.png"
                elif i == 2:
                    filename = f"function3_{timestamp}.png"
                elif i == 3:
                    filename = f"combined_{timestamp}.png"
                else:
                    filename = f"analysis_{timestamp}.png"
                
                # Save the figure
                full_path = os.path.join(save_dir, filename)
                canvas.figure.savefig(full_path, dpi=300, bbox_inches='tight')
                count += 1
            
            # Also save any dynamic function canvases
            for i, canvas in enumerate(self.function_canvases):
                # Skip empty plots
                if len(canvas.axes.lines) == 0 and len(canvas.axes.collections) == 0:
                    continue
                
                filename = f"dynamic_function{i+1}_{timestamp}.png"
                full_path = os.path.join(save_dir, filename)
                canvas.figure.savefig(full_path, dpi=300, bbox_inches='tight')
                count += 1
            
            # Show success message
            if count > 0:
                QMessageBox.information(self, "Save Successful", 
                                     f"Successfully saved {count} plots to:\n{save_dir}")
            else:
                QMessageBox.warning(self, "No Plots Saved", 
                                 "There were no plots to save. Please generate some plots first.")
        
        except Exception as e:
            QMessageBox.critical(self, "Error Saving Plots", f"An error occurred while saving plots: {e}")


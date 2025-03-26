import sys
import os
import numpy as np
from datetime import datetime
from sympy import symbols, sympify, diff, integrate, sin, cos, tan, exp, log, sqrt, pi
from sympy.utilities.lambdify import lambdify
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QGroupBox, QLabel, QLineEdit, QPushButton, QGridLayout, QSlider, 
                           QSpinBox, QComboBox, QCheckBox, QSplitter, QScrollArea, QFrame,
                           QTabWidget, QFileDialog, QMessageBox, QDoubleSpinBox, QSizePolicy,)
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
        self.entire_top_scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.entire_top_scrollarea.setStyleSheet("""
            QScrollBar:horizontal {
                height: 15px;
                background: #2e2e2e;
                border-radius: 6px;
                margin-left: 5px;
                margin-right: 5px; 
            }
            QScrollBar::handle:horizontal {
                background: #2e2e2e;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

        self.entire_top_scrollcontent = QWidget()
        self.entire_top_scrolllayout = QHBoxLayout(self.entire_top_scrollcontent)
        self.entire_top_scrolllayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entire_top_scrolllayout.setSpacing(10)
        self.entire_top_scrollarea.setWidget(self.entire_top_scrollcontent)
        entire_top_layout.addWidget(self.entire_top_scrollarea)
        entire_layout.addWidget(entire_top, stretch=1)  

        entire_top.setStyleSheet("""
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            background-color: #4e4e4e;
            margin-bottom: 10px;
        """)
        
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

        entire_bottom_left.setStyleSheet("""
            border-radius: 8px;
            background-color: #2e2e2e;
        """)

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

        entire_bottom_right.setStyleSheet("""
            border-radius: 8px;
            background-color: #2e2e2e;
        """)
        
        entire_bottom_layout.addWidget(entire_bottom_left)
        entire_bottom_layout.addWidget(entire_bottom_right)
        entire_layout.addWidget(entire_bottom, stretch=1) 
        
        # Individual function tabs
        self.individual_tab = QWidget()
        individual_layout = QGridLayout(self.individual_tab)
        
        # Create individual canvases with responsive sizing
        self.canvas1 = MplCanvas(width=6, height=6, dpi=100)
        self.canvas2 = MplCanvas(width=6, height=6, dpi=100)
        self.canvas3 = MplCanvas(width=6, height=6, dpi=100)
        
        # Set size policies for responsive resizing
        for canvas in [self.canvas1, self.canvas2, self.canvas3]:
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas.setMinimumSize(200, 150)
        
        # Create frames for each canvas
        canvas1_frame = QFrame()
        canvas2_frame = QFrame()
        canvas3_frame = QFrame()
        
        for frame in [canvas1_frame, canvas2_frame, canvas3_frame]:
            frame.setStyleSheet("""
                QFrame {
                    background-color: #3e3e3e;
                    border-radius: 8px;
                    border: 1px solid #555;
                }
            """)
            frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Add canvases to frames with layouts
        canvas1_layout = QVBoxLayout(canvas1_frame)
        canvas2_layout = QVBoxLayout(canvas2_frame)
        canvas3_layout = QVBoxLayout(canvas3_frame)
        
        canvas1_layout.addWidget(self.canvas1)
        canvas2_layout.addWidget(self.canvas2)
        canvas3_layout.addWidget(self.canvas3)
        
        # Add frames to grid layout with proper spacing
        individual_layout.addWidget(canvas1_frame, 0, 0)
        individual_layout.addWidget(canvas2_frame, 0, 1)
        individual_layout.addWidget(canvas3_frame, 1, 0)
        
        # Set layout spacing and margins
        individual_layout.setSpacing(10)
        individual_layout.setContentsMargins(10, 10, 10, 10)
        
        # Combined tab
        self.combined_tab = QWidget()
        combined_layout = QVBoxLayout(self.combined_tab)
        self.combined_canvas = MplCanvas(width=9, height=12, dpi=100)
        combined_layout.addWidget(self.combined_canvas)
        
        # Analysis tab
        self.analysis_tab = QWidget()
        analysis_layout = QVBoxLayout(self.analysis_tab)
        self.analysis_canvas = MplCanvas(width=9, height=12, dpi=100)
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

        # Add left spacer for centering
        self.entire_top_scrolllayout.addStretch(2)

        # Create a canvas for each function
        for i, expr in enumerate(expressions):
            container = QWidget()
            container.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            container_layout = QVBoxLayout(container)
            container_layout.setContentsMargins(10, 10, 10, 10)
            container_layout.setSpacing(10)
            
            # Create frame for the canvas
            canvas_frame = QFrame()
            canvas_frame.setMinimumSize(200, 150)  
            canvas_frame.setMaximumSize(420, 300)  
            canvas_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            canvas_frame_layout = QVBoxLayout(canvas_frame)
            canvas_frame_layout.setContentsMargins(0, 0, 0, 0)
            
            # Create canvas with responsive size
            canvas = MplCanvas(width=5, height=3.5, dpi=100)
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
            # Apply theme to the new canvas
            self.apply_plot_theme(canvas.axes)
            
            canvas_frame_layout.addWidget(canvas)
            self.function_canvases.append(canvas)
            
            # Add canvas frame to container
            container_layout.addWidget(canvas_frame)
            
            # Add label with word wrap
            label = QLabel(f"Function {i+1}: {expr}")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("""
                font-weight: bold; 
                margin-top: 5px;
                padding: 5px;
                background-color: rgba(58, 134, 255, 0.1);
                border-radius: 4px;
            """)
            label.setWordWrap(True)
            label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
            container_layout.addWidget(label)
            
            # Create a frame for the container
            frame = QFrame()
            frame.setObjectName(f"function_frame_{i}")
            frame.setStyleSheet("""
                QFrame {
                    background-color: #3e3e3e;
                    border-radius: 8px;
                    border: 1px solid #555;
                }
            """)
            frame.setLayout(container_layout)
            frame.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            
            # Add to layout
            self.entire_top_scrolllayout.addWidget(frame)

        # Add right spacer for centering
        self.entire_top_scrolllayout.addStretch(1)
        
        # Update function visibility checkboxes
        self.update_function_visibility_checkboxes(expressions)

        # Force layout update
        self.entire_top_scrollcontent.adjustSize()
    
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
        
        # Clear all canvases and apply theme
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas, 
                      self.analysis_canvas, self.combined_small_canvas, self.analysis_small_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            self.set_y_scale(canvas.axes)
            self.apply_plot_theme(canvas.axes)  # Apply theme to each canvas
        
        # Clear the function canvases and apply theme
        for canvas in self.function_canvases:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            self.set_y_scale(canvas.axes)
            self.apply_plot_theme(canvas.axes)  # Apply theme to each canvas
        
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
        
        # Clear canvases and apply theme
        for canvas in [self.canvas1, self.canvas2, self.canvas3, self.combined_canvas]:
            canvas.axes.clear()
            canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
            self.set_y_scale(canvas.axes)
            self.apply_plot_theme(canvas.axes)  # Apply theme to each canvas
        
        # Create dynamic canvases for the Entire View tab
        self.create_dynamic_canvases(expressions)
        
        # Apply theme to all dynamic canvases
        for canvas in self.function_canvases:
            self.apply_plot_theme(canvas.axes)
        
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
                # Get the individual canvas and the dynamic canvas
                canvas = None
                if i == 0:
                    canvas = self.canvas1
                elif i == 1:
                    canvas = self.canvas2
                elif i == 2:
                    canvas = self.canvas3
                
                dynamic_canvas = self.function_canvases[i] if i < len(self.function_canvases) else None
                
                if canvas is None:
                    continue
                
                # Plot on both individual and dynamic canvases
                for current_canvas in [canvas, dynamic_canvas]:
                    if current_canvas is None:
                        continue
                        
                    current_canvas.axes.clear()
                    current_canvas.axes.grid(self.grid_lines.isChecked(), linestyle='--', alpha=0.7)
                    self.set_y_scale(current_canvas.axes)
                    
                    # Calculate and plot based on type
                    if plot_type == "functions":
                        y_values = func(x_range)
                        y_values = np.nan_to_num(y_values, nan=0.0, posinf=1e10, neginf=-1e10)
                        
                        if self.normalize.isChecked():
                            y_max = max(abs(np.max(y_values)), abs(np.min(y_values)))
                            if y_max > 0:
                                y_values = y_values / y_max
                        
                        current_canvas.axes.plot(x_range, y_values, color=colors[i % len(colors)], 
                                              linewidth=2, label=f"f(x) = {expr}")
                    
                    elif plot_type == "derivatives":
                        derivative_expr = diff(parsed_expr, x)
                        derivative_func = lambdify(x, derivative_expr, 'numpy')
                        d_values = derivative_func(x_range)
                        d_values = np.nan_to_num(d_values, nan=0.0, posinf=1e10, neginf=-1e10)
                        
                        if self.normalize.isChecked():
                            d_max = max(abs(np.max(d_values)), abs(np.min(d_values)))
                            if d_max > 0:
                                d_values = d_values / d_max
                        
                        current_canvas.axes.plot(x_range, d_values, color=colors[i % len(colors)], 
                                              linewidth=2, label=f"f'(x) = {derivative_expr}")
                        
                        # Plot critical points
                        critical_points = []
                        for j in range(1, len(x_range) - 1):
                            if (d_values[j-1] * d_values[j+1] <= 0) or abs(d_values[j]) < 1e-6:
                                y_val = func(x_range[j])
                                critical_points.append((x_range[j], y_val))
                        
                        # Plot the critical points on function graph
                        y_values = func(x_range)
                        y_values = np.nan_to_num(y_values, nan=0.0, posinf=1e10, neginf=-1e10)
                        current_canvas.axes.plot(x_range, y_values, color=colors[i % len(colors)], 
                                              linewidth=1, linestyle=':', alpha=0.5)
                        
                        for cp in critical_points:
                            current_canvas.axes.plot(cp[0], cp[1], 'o', color=colors[i % len(colors)], 
                                                  markersize=6)
                            current_canvas.axes.annotate(f"({cp[0]:.2f}, {cp[1]:.2f})", 
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
                        
                        current_canvas.axes.plot(x_range, int_values, color=colors[i % len(colors)], 
                                              linewidth=2, label=f"∫f(x)dx = {integral_expr} + C")
                    
                    # Set axis labels and apply settings
                    current_canvas.axes.set_xlabel('x')
                    current_canvas.axes.set_ylabel('y')
                    
                    if self.legend.isChecked():
                        current_canvas.axes.legend(loc='upper left', fontsize='small')
                    
                    # Apply theme settings
                    self.apply_plot_theme(current_canvas.axes)
                    
                    # Apply axis limits if auto-scale is disabled
                    self.apply_axis_limits(current_canvas.axes)
                    
                    # Draw the plot
                    current_canvas.draw()
                
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
        
        else:  # Default theme
            ax.set_facecolor('white')
            ax.tick_params(colors='black')
            ax.xaxis.label.set_color('black')
            ax.yaxis.label.set_color('black')
            ax.title.set_color('black')
            for spine in ax.spines.values():
                spine.set_color('black')
                spine.set_linewidth(1)
            if self.grid_lines.isChecked():
                ax.grid(True, linestyle='--', alpha=0.7, color='#cccccc')
    
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
        """Save plots with customizable options"""
        from PyQt6.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QCheckBox, QComboBox, QLabel, QDialogButtonBox
        
        # Create a custom dialog for save options
        dialog = QDialog(self)
        dialog.setWindowTitle("Save Plot Options")

        dialog.setMinimumSize(270, 290)
        dialog.setMaximumSize(300, 300)

        layout = QVBoxLayout(dialog)
        
        # Plot selection checkboxes
        layout.addWidget(QLabel("Select plots to save:"))
        cb_function1 = QCheckBox("Function 1")
        cb_function2 = QCheckBox("Function 2")
        cb_function3 = QCheckBox("Function 3")
        cb_combined = QCheckBox("Combined View")
        cb_analysis = QCheckBox("Analysis View")
        
        # Check all by default
        for cb in [cb_function1, cb_function2, cb_function3, cb_combined, cb_analysis]:
            cb.setChecked(True)
            layout.addWidget(cb)
        
        # File format selection
        layout.addWidget(QLabel("File format:"))
        format_combo = QComboBox()
        format_combo.addItems(["PNG", "JPG", "SVG", "PDF"])
        layout.addWidget(format_combo)
        
        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        # Show dialog and get result
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        # Get selected file format
        file_format = format_combo.currentText().lower()
        
        # Ask user to select a directory
        save_dir = QFileDialog.getExistingDirectory(
            self, 
            "Select Directory to Save Plots",
            "",
            QFileDialog.Option.ShowDirsOnly
        )
        
        if not save_dir:
            return
        
        try:
            import os
            saved_files = []
            
            # Save selected plots
            if cb_function1.isChecked():
                filename = os.path.join(save_dir, f"function1.{file_format}")
                self.canvas1.fig.savefig(filename)
                saved_files.append(filename)
                
            if cb_function2.isChecked():
                filename = os.path.join(save_dir, f"function2.{file_format}")
                self.canvas2.fig.savefig(filename)
                saved_files.append(filename)
                
            if cb_function3.isChecked():
                filename = os.path.join(save_dir, f"function3.{file_format}")
                self.canvas3.fig.savefig(filename)
                saved_files.append(filename)
                
            if cb_combined.isChecked():
                filename = os.path.join(save_dir, f"combined_view.{file_format}")
                self.combined_canvas.fig.savefig(filename)
                saved_files.append(filename)
                
            if cb_analysis.isChecked():
                filename = os.path.join(save_dir, f"analysis_view.{file_format}")
                self.analysis_canvas.fig.savefig(filename)
                saved_files.append(filename)
            
            # Show success message
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self, 
                "Success", 
                f"Saved {len(saved_files)} plot(s) to:\n{save_dir}"
            )
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", f"Error saving plots: {e}")


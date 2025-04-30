# Calculus-Powered Graphing App

## Introduction
This project is a Python-based application designed to visualize mathematical functions along with their derivatives and integrals. It provides a hands-on approach to explore numerical methods, computational calculus, and interactive data visualization. Created as part of our calculus subject project, this tool helps explore the practical applications of differentiation and integration in data analysis, physics simulations, and mathematical exploration.

## Features
- Parse and evaluate mathematical expressions entered as strings
- Support for common mathematical functions (sin, cos, exp, log, tan, sqrt)
- Compute and visualize:
  - The original function
  - Derivatives (first or higher order)
  - Indefinite integrals
- Identify critical points where derivatives change sign
- Interactive graph display using Matplotlib
- Symbolic computation using SymPy for accurate mathematical analysis
- Conversion between symbolic expressions and numerical functions using NumPy

## Installation and Setup

### Requirements
- Python 3.6+
- Required packages:
  - numpy>=1.20.0
  - matplotlib>=3.5.0
  - sympy>=1.9.0
  - PyQt6>=6.0.0
  - setuptools==77.0.3

### Installation
1. Clone or download this repository to your local machine
2. Install the required dependencies:
```
pip install -r requirements.txt
```

### Running the Application
1. Copy all the code files to a directory
2. Run the main script:
```
python main.py
```
(Note: Adjust the filename according to your main script name)

## Usage Guide

### Basic Function Analysis
1. Enter a mathematical function in the input field (e.g., `x**2 - 4*x + 5`)
2. Set the desired x-range for visualization
3. Click "Plot" to generate the visualization

### Supported Mathematical Functions
- Trigonometric: `sin(x)`, `cos(x)`, `tan(x)`
- Exponential: `exp(x)`
- Logarithmic: `log(x)`
- Square root: `sqrt(x)`
- Constant: `pi`
- Basic arithmetic operations: +, -, *, /, **

### Example Expressions
- Quadratic function: `x**2 - 4*x + 4`
- Sine wave: `sin(x)`
- Exponential growth: `exp(x)`
- Combined expression: `sin(x) * exp(-0.1*x)`

## Implementation Details

The application uses:
- SymPy for symbolic computation and mathematical expression parsing
- NumPy for numerical calculations and array operations
- Matplotlib for plotting and visualization
- Lambda functions for efficient evaluation of mathematical expressions

## Future Enhancements
- Implement root finding for equations
- Add support for 3D function visualization
- Enable export of graphs as high-quality images
- Provide numerical analysis of functions (area under curve, etc.)
- Add animation features to visualize function transformations

## License
This project is for educational purposes and is open for further improvements.

## Contributors
- _Nu1L
  - Main Developer
- Kie
  - Moral Support
- DnJstr
  - Laugher
- piaamarie
  -[`Princess`, `Cutie`, `Pretty`, `Smart`]
- Lorenz
  - Kuya
- Jaybird
  - 2nd Kuya
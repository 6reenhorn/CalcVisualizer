from setuptools import setup, find_packages

setup(
    name="calcvisualizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "sympy",
        "PyQt6",
    ],
    entry_points={
        "console_scripts": [
            "calcvisualizer=main:main",
        ],
    },
)
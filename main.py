from calcvisualizer.ui.app import GraphingApp
from PyQt6.QtWidgets import QApplication
import sys

def main():
    app = QApplication(sys.argv)
    window = GraphingApp()
    window.showMaximized()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()



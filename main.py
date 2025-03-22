from app.ui import GraphingApp
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphingApp()
    window.show()
    sys.exit(app.exec())

from calcvisualizer.ui.app import GraphingApp
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QTimer
import sys
import time
from assets.assets import LOADING_ICON

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        
        # Remove window title and frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        self.setStyleSheet("""
            background-color: white;
            color: black;
        """)

        # Create layout
        layout = QVBoxLayout(self)
        
        # Create label for GIF
        self.label = QLabel(self)
        self.movie = QMovie(LOADING_ICON)  
        self.label.setMovie(self.movie)
        self.movie.start()
        
        # Add loading text
        self.loading_text = QLabel("Loading application...", self)
        self.loading_text.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.loading_text.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        # Add widgets to layout
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_text, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        
        self.center_on_screen()
    
    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

def main():
    app = QApplication(sys.argv)

    loading_screen = LoadingScreen()
    loading_screen.show()

    QApplication.processEvents()

    def finish_loading():
        window = GraphingApp()
        window.showMaximized()
        loading_screen.close()
    
    QTimer.singleShot(3000, finish_loading)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
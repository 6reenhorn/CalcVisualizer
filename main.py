from calcvisualizer.ui.app import GraphingApp
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtGui import QMovie, QPixmap
from PyQt6.QtCore import Qt, QTimer, QSize
import sys
from assets.assets import LOADING_ICON, WINDOW_ICON

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        
        # Remove window title and frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Enable transparency for the window
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Create a frame for the content with rounded corners
        self.frame = QFrame(self)
        self.frame.setStyleSheet("""
            QFrame#mainFrame {
                background-color: #3e3e3e;
                border-radius: 10px;
                color: black;
                border: 5px double #3e3e3e;
            }
            QLabel {
                border: none;
                background-color: transparent;
                color: #cfcfcf;
            }
        """)
        self.frame.setObjectName("mainFrame") 
        
        # Setup the main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.frame)
        
        # Create frame layout
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setSpacing(5)
        
        # Create a custom image label for the top
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(WINDOW_ICON))
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter)
        
        # Create horizontal layout for GIF and text
        horizontal_layout = QHBoxLayout()
        
        # Create label for GIF
        self.label = QLabel()
        self.movie = QMovie(LOADING_ICON)
        self.movie.setScaledSize(QSize(30, 30))
        self.label.setMovie(self.movie)
        self.movie.start()
        
        # Add loading text
        self.loading_text = QLabel("Loading application...")
        self.loading_text.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        # Add GIF and text to horizontal layout
        horizontal_layout.addWidget(self.label)
        horizontal_layout.addWidget(self.loading_text)
        horizontal_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        horizontal_layout.setSpacing(10)
        
        # Add widgets to frame layout
        frame_layout.addWidget(self.image_label)
        frame_layout.addLayout(horizontal_layout)
        
        self.center_on_screen()
    
    def center_on_screen(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2 - 50
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
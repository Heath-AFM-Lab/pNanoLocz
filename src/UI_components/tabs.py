from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabbed Interface Example")
        self.setGeometry(100, 100, 600, 400)
        
        # Create the main layout
        layout = QVBoxLayout()
        
        # Create the tab widget
        tabs = QTabWidget()
        
        # Create tabs
        home_tab = QWidget()
        level_tab = QWidget()
        detect_tab = QWidget()
        finealign_tab = QWidget()
        localize_tab = QWidget()
        
        # Add tabs to the widget
        tabs.addTab(home_tab, "Home")
        tabs.addTab(level_tab, "Level")
        tabs.addTab(detect_tab, "Detect")
        tabs.addTab(finealign_tab, "FineAlign")
        tabs.addTab(localize_tab, "Localize")
        
        # Set up the tab contents
        self.setupTab(home_tab, "Home Content", Qt.black)
        self.setupTab(level_tab, "Level Content", Qt.red)
        self.setupTab(detect_tab, "Detect Content", Qt.blue)
        self.setupTab(finealign_tab, "FineAlign Content", Qt.yellow)
        self.setupTab(localize_tab, "Localize Content", Qt.magenta)
        
        # Add tabs to the main layout
        layout.addWidget(tabs)
        
        # Set the main layout
        self.setLayout(layout)
        
    def setupTab(self, tab, text, color):
        tab_layout = QVBoxLayout()
        label = QLabel(text)
        palette = label.palette()
        palette.setColor(QPalette.WindowText, color)
        label.setPalette(palette)
        label.setAlignment(Qt.AlignCenter)
        tab_layout.addWidget(label)
        tab.setLayout(tab_layout)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

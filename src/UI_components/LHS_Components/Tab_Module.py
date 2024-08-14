from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLabel
)
from PyQt6.QtGui import QColor
from UI_components.LHS_Components.Tab_Modules import LevelingWidget
from core.Image_Storage_Module.Image_Storage_Class import MediaDataManager


class TabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildTabWidget()

    def buildTabWidget(self):
        media_data_manager = MediaDataManager()

        # Create the tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.home_tab = QWidget()
        self.level_tab = LevelingWidget()
        self.detect_tab = QWidget()
        self.finealign_tab = QWidget()
        self.localize_tab = QWidget()
        
        # Add tabs to the widget
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.level_tab, "Level")
        self.tabs.addTab(self.detect_tab, "Detect")
        self.tabs.addTab(self.finealign_tab, "FineAlign")
        self.tabs.addTab(self.localize_tab, "Localize")
        
        # Set up the tab contents
        self.setupTab(self.home_tab, "Home Content", QColor('black'))
        self.setupTab(self.detect_tab, "Detect Content", QColor('blue'))
        self.setupTab(self.finealign_tab, "FineAlign Content", QColor('orange'))
        self.setupTab(self.localize_tab, "Localize Content", QColor('magenta'))
        
        # Set layout to the current widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    # Function stands incomplete as priority is to develop a video player application first
    # TODO: develop the individual 5 tabs as per the MatLab NanoLocz app
    # This likely needs to be external
    def setupTab(self, tab, content, color):
        layout = QVBoxLayout()
        label = QLabel(content)
        label.setStyleSheet(f"color: {color.name()};")
        layout.addWidget(label)
        tab.setLayout(layout)



# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys
import os

if __name__ == '__main__':
    # TODO: remove once format correction is complete
    ICON_DIRECTORY = "../../../assets/icons"
    # Path to icon directory
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    tab = TabWidget()
    tab.show()
    sys.exit(app.exec())
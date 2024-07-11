import os
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from utils.constants import PATH_TO_ICON_DIRECTORY

class ParticleViewerAndControlWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildParticleViewerAndControlWidget()

    def buildParticleViewerAndControlWidget(self):
        # Set up layout
        self.layout = QVBoxLayout()

        self.iconLayout = QHBoxLayout()
        self.iconLayout.addStretch(1)

        # Add screenshot icon
        self.screenshotIcon = QPushButton()
        self.screenshotIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pop.png")))
        self.screenshotIcon.setIconSize(self.screenshotIcon.sizeHint())
        self.screenshotIcon.setToolTip("Screenshot video")
        self.screenshotIcon.setFixedSize(16, 16)
        self.iconLayout.addWidget(self.screenshotIcon)
        self.layout.addLayout(self.iconLayout)

        # Add particle viewer widget
        # TODO: replace placeholder QWidget with an actual particle viewer widget, also preferably using vispy
        self.particleViewerPlaceholder = QWidget()
        self.particleViewerPlaceholder.setFixedSize(480, 480)
        self.layout.addWidget(self.particleViewerPlaceholder)

        # Add a mock tab widget 
        self.particleViewerControlWidget = ParticleControlTabWidget()
        self.layout.addWidget(self.particleViewerControlWidget)

        # Set the layout for this widget
        self.setLayout(self.layout)

class ParticleControlTabWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildParticleControlTabWidget()

    def buildParticleControlTabWidget(self):
        # Create the tab widget
        self.tabs = QTabWidget()
        
        # Create tabs
        self.lineTab = QWidget()
        self.referenceTab = QWidget()
        self.lasmTab = QWidget()
        
        # Add tabs to the widget
        self.tabs.addTab(self.lineTab, "Line")
        self.tabs.addTab(self.referenceTab, "Reference")
        self.tabs.addTab(self.lasmTab, "LASM")

        # Set up the tab contents
        self.setupTab(self.lineTab, "Line Content")
        self.setupTab(self.referenceTab, "Reference Content")
        self.setupTab(self.lasmTab, "LASM Content")
        
        # Set layout to the current widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
    # Function stands incomplete as priority is to develop a video player application first
    # TODO: develop the individual 5 tabs as per the MatLab NanoLocz app
    # This likely needs to be external
    def setupTab(self, tab, content):
        layout = QVBoxLayout()
        label = QLabel(content)
        layout.addWidget(label)
        tab.setLayout(layout)

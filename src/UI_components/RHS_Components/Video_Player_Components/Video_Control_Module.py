import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel, 
    QLineEdit, QSlider
)
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtCore import Qt, pyqtSignal
from constants import PATH_TO_ICON_DIRECTORY


class VideoControlWidget(QWidget):
    specificVideoFrameGiven = pyqtSignal(int)
    playClicked = pyqtSignal()
    skipBackClicked = pyqtSignal()
    skipForwardClicked = pyqtSignal()
    fpsChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout()

        # Video control buttons
        self.buttonLayout = QHBoxLayout()

        self.frameSpinBox = QSpinBox()
        self.frameSpinBox.setMinimum(0)
        self.frameSpinBox.setMaximum(100000)
        self.frameSpinBox.setSingleStep(1)
        self.frameSpinBox.valueChanged.connect(lambda frameNo: self.specificVideoFrameGiven.emit(int(frameNo)))
        self.buttonLayout.addWidget(self.frameSpinBox)

        self.skipBackIcon = QPushButton()
        self.skipBackIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "start.png")))
        self.skipBackIcon.setIconSize(self.skipBackIcon.sizeHint())
        self.skipBackIcon.setToolTip("Skip to first frame")
        self.skipBackIcon.clicked.connect(self.skipBackClicked.emit)
        self.buttonLayout.addWidget(self.skipBackIcon)

        self.playIcon = QPushButton()
        self.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
        self.playIcon.setIconSize(self.playIcon.sizeHint())
        self.playIcon.setToolTip("Play")
        self.playIcon.clicked.connect(self.playClicked.emit)
        self.buttonLayout.addWidget(self.playIcon)

        self.skipForwardIcon = QPushButton()
        self.skipForwardIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "end.png")))
        self.skipForwardIcon.setIconSize(self.skipForwardIcon.sizeHint())
        self.skipForwardIcon.setToolTip("Skip to last frame")
        self.skipForwardIcon.clicked.connect(self.skipForwardClicked.emit)
        self.buttonLayout.addWidget(self.skipForwardIcon)

        self.fpsLabel = QLabel("Playback speed (FPS):")
        self.fpsTextBox = QLineEdit()
        self.fpsTextBox.setValidator(QIntValidator())
        self.fpsTextBox.textChanged.connect(lambda text: self.fpsChanged.emit(int(text)) if text.isdigit() else None)
        self.buttonLayout.addWidget(self.fpsLabel)
        self.buttonLayout.addWidget(self.fpsTextBox)

        self.layout.addLayout(self.buttonLayout)

        # Video slider
        self.videoSeekSlider = QSlider(Qt.Orientation.Horizontal)
        self.videoSeekSlider.setRange(0, 100)
        self.layout.addWidget(self.videoSeekSlider)

        self.setLayout(self.layout)
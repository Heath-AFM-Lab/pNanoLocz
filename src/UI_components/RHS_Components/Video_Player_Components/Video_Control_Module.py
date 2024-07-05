import re
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel, 
    QLineEdit, QSlider
)
from PyQt6.QtGui import QIcon, QIntValidator, QValidator
from PyQt6.QtCore import Qt, pyqtSignal
from constants import PATH_TO_ICON_DIRECTORY


class RangeValidator(QValidator):
    def validate(self, input_str, pos):
        # Empty input is considered intermediate state (not invalid)
        if not input_str:
            return (QValidator.State.Intermediate, input_str, pos)

        # Regular expression to match a single number or a range like "10-20"
        range_pattern = re.compile(r'^\d+(-\d+)?$')
        
        if range_pattern.match(input_str):
            return (QValidator.State.Acceptable, input_str, pos)
        else:
            return (QValidator.State.Invalid, input_str, pos)

    def fixup(self, input_str):
        # Optionally, implement any automatic fixes for invalid input
        return input_str
    

class VideoControlWidget(QWidget):
    specificVideoFrameGiven = pyqtSignal(int)
    playClicked = pyqtSignal()
    skipBackClicked = pyqtSignal()
    skipForwardClicked = pyqtSignal()
    fpsChanged = pyqtSignal(int)
    videoAlignButtonClicked = pyqtSignal()
    deleteFramesButtonClicked = pyqtSignal()

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
        # TODO: Update the range when a video has been loaded
        self.videoSeekSlider.setRange(0, 100)
        self.layout.addWidget(self.videoSeekSlider)

        # Add video align and delete frames widgets
        self.videoEditingLayout = QHBoxLayout()

        self.videoAlignButton = QPushButton("Align video")
        self.videoAlignButton.setIconSize(self.videoAlignButton.sizeHint())
        self.videoAlignButton.setToolTip("Align video frames")
        self.videoAlignButton.setFixedSize(self.videoAlignButton.sizeHint())
        self.videoAlignButton.clicked.connect(self.videoAlignButtonClicked.emit)
        self.videoEditingLayout.addWidget(self.videoAlignButton)

        self.videoEditingLayout.addStretch(1)

        # Delete frames consists of a label, text box and icon
        self.deleteFramesLabel = QLabel("Delete frames:")
        self.deleteFramesTextBox = QLineEdit()
        self.deleteFramesTextBox.setValidator(RangeValidator())

        # Add Delete frames icon
        self.deleteFramesButton = QPushButton()
        self.deleteFramesButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "bin.png")))
        self.deleteFramesButton.setIconSize(self.deleteFramesButton.sizeHint())  # Adjust icon size to button size
        self.deleteFramesButton.setToolTip("Delete frames")
        self.deleteFramesButton.clicked.connect(self.deleteFramesButtonClicked.emit)
        self.deleteFramesButton.setFixedSize(self.deleteFramesButton.sizeHint())

        self.videoEditingLayout.addWidget(self.deleteFramesLabel)
        self.videoEditingLayout.addWidget(self.deleteFramesTextBox)
        self.videoEditingLayout.addWidget(self.deleteFramesButton)

        self.layout.addLayout(self.videoEditingLayout)

        self.setLayout(self.layout)
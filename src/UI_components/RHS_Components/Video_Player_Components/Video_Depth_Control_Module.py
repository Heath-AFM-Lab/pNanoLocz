from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, 
    QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QUrl, pyqtSignal

from constants import PATH_TO_ICON_DIRECTORY

class VideoDepthControlWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setupUi()

        def setupUi(self):
            self.layout = QVBoxLayout()

            self.depthTypeDropdown = QComboBox()
            self.depthTypeDropdown.addItems(["Min Max", "Histogram", "Excl. outliers", "Manual"])
            self.depthTypeDropdown.setFixedSize(self.depthTypeDropdown.sizeHint())
            self.layout.addWidget(self.depthTypeDropdown)

            self.buttonLayout = QHBoxLayout()
            self.autoButton = QPushButton("Auto")
            self.buttonLayout.addWidget(self.autoButton)

            self.holdButton = QPushButton("Hold")
            self.buttonLayout.addWidget(self.holdButton)

            self.layout.addLayout(self.buttonLayout)

            self.minSpinLayout = QHBoxLayout()
            self.minSpinBox = QDoubleSpinBox()
            self.minSpinBox.setMinimum(0)
            self.minSpinBox.setMaximum(10000)
            self.minSpinBox.setSingleStep(0.01)
            self.minSpinBox.setFixedSize(self.minSpinBox.sizeHint())
            self.minSpinLabel = QLabel("Min height:")
            self.minSpinLayout.addWidget(self.minSpinLabel)
            self.minSpinLayout.addWidget(self.minSpinBox)

            self.maxSpinLayout = QHBoxLayout()
            self.maxSpinBox = QDoubleSpinBox()
            self.maxSpinBox.setMinimum(0)
            self.maxSpinBox.setMaximum(10000)
            self.maxSpinBox.setSingleStep(0.01)
            self.maxSpinBox.setFixedSize(self.maxSpinBox.sizeHint())
            self.maxSpinLabel = QLabel("Max height:")
            self.maxSpinLayout.addWidget(self.maxSpinLabel)
            self.maxSpinLayout.addWidget(self.maxSpinBox)

            self.layout.addLayout(self.minSpinLayout)
            self.layout.addLayout(self.maxSpinLayout)

            self.setLayout(self.layout)
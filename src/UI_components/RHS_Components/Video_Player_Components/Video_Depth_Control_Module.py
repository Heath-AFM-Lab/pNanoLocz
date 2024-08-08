from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, 
    QDoubleSpinBox, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from utils.constants import DEPTH_CONTROL_OPTIONS

class VideoDepthControlWidget(QWidget):
    new_depth_values = pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout()

        # Dropdown for depth control types
        self.depthTypeDropdown = QComboBox()
        self.depthTypeDropdown.addItems(DEPTH_CONTROL_OPTIONS)
        self.layout.addWidget(self.depthTypeDropdown)

        # Button layout
        self.buttonLayout = QHBoxLayout()
        self.autoButton = QPushButton("Auto")
        self.buttonLayout.addWidget(self.autoButton)
        self.holdButton = QPushButton("Hold")
        self.buttonLayout.addWidget(self.holdButton)
        self.layout.addLayout(self.buttonLayout)

        # Max spin box layout
        self.maxSpinLayout = QHBoxLayout()
        self.maxSpinBox = QDoubleSpinBox()
        self.maxSpinBox.setMinimum(-1000000)
        self.maxSpinBox.setMaximum(1000000)
        self.maxSpinBox.setSingleStep(0.01)
        self.maxSpinBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.maxSpinLabel = QLabel("Max height:")
        self.maxSpinLayout.addWidget(self.maxSpinLabel)
        self.maxSpinLayout.addWidget(self.maxSpinBox)

        # Min spin box layout
        self.minSpinLayout = QHBoxLayout()
        self.minSpinBox = QDoubleSpinBox()
        self.minSpinBox.setMinimum(-1000000)
        self.minSpinBox.setMaximum(1000000)
        self.minSpinBox.setSingleStep(0.01)
        self.minSpinBox.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.minSpinLabel = QLabel("Min height:")
        self.minSpinLayout.addWidget(self.minSpinLabel)
        self.minSpinLayout.addWidget(self.minSpinBox)

        # Adding min and max spin box layouts to main layout
        self.layout.addLayout(self.maxSpinLayout)
        self.layout.addLayout(self.minSpinLayout)
        self.layout.addStretch(1)  # Optional, for spacing

        # Connect signals to slots
        self.holdButton.clicked.connect(self.go_to_manual_depth_control)
        self.autoButton.clicked.connect(self.go_to_min_max_depth_control)
        self.minSpinBox.valueChanged.connect(self.validate_min_max_spin_boxes)
        self.maxSpinBox.valueChanged.connect(self.validate_min_max_spin_boxes)

        self.setLayout(self.layout)

    def go_to_manual_depth_control(self):
        self.depthTypeDropdown.setCurrentText("Manual")

    def go_to_min_max_depth_control(self):
        self.depthTypeDropdown.setCurrentText("Min Max")

    def validate_min_max_spin_boxes(self):
        self.minSpinBox.blockSignals(True)
        self.maxSpinBox.blockSignals(True)

        min_value = self.minSpinBox.value()
        max_value = self.maxSpinBox.value()

        if min_value > max_value:
            # Prevent the minimum value from exceeding the maximum value
            if self.sender() == self.minSpinBox:
                self.minSpinBox.setValue(max_value)
            else:
                self.maxSpinBox.setValue(min_value)

        self.minSpinBox.blockSignals(False)
        self.maxSpinBox.blockSignals(False)

        min_value = self.minSpinBox.value()
        max_value = self.maxSpinBox.value()

        self.new_depth_values.emit(min_value, max_value)

        
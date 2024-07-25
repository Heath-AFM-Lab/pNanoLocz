from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PyQt6.QtCore import pyqtSignal


class VisualRepresentationWidget(QWidget):
    # Instantiate signals
    scaleBarCheckboxChecked = pyqtSignal(bool)
    zScaleCheckboxChecked = pyqtSignal(bool)
    timescaleCheckboxChecked = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout()

        self.scaleBarCheckbox = QCheckBox("Scale bar")
        self.scaleBarCheckbox.setToolTip("Enable or disable Scale bar")
        self.scaleBarCheckbox.clicked.connect(self.scaleBarCheckboxChecked.emit)
        self.layout.addWidget(self.scaleBarCheckbox)
    
        self.zScaleCheckbox = QCheckBox("Z-scale")
        self.zScaleCheckbox.setToolTip("Enable or disable Z-scale")
        self.zScaleCheckbox.clicked.connect(self.zScaleCheckboxChecked.emit)
        self.layout.addWidget(self.zScaleCheckbox)

        self.timescaleCheckbox = QCheckBox("Timescale")
        self.timescaleCheckbox.setToolTip("Enable or disable Timescale")
        self.timescaleCheckbox.clicked.connect(self.timescaleCheckboxChecked.emit)
        self.layout.addWidget(self.timescaleCheckbox)
        
        self.setLayout(self.layout)
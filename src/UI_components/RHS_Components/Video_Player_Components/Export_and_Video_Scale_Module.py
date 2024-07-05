
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox

class ExportAndVideoScaleWidget(QWidget):
    # TODO: figure out how to do the signals and or slots for this section.


    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.layout = QHBoxLayout()

        self.exportButton = QPushButton("Export")
        self.exportButton.setToolTip("Export data plot")
        self.exportButton.setFixedSize(self.exportButton.sizeHint())
        self.layout.addWidget(self.exportButton)

        self.exportTargetPlotDropdown = QComboBox()
        self.exportTargetPlotDropdown.addItems(["Plot 1", "Plot 2", "Data"])
        self.exportTargetPlotDropdown.setFixedSize(self.exportTargetPlotDropdown.sizeHint())
        self.layout.addWidget(self.exportTargetPlotDropdown)

        self.fileFormatDropdown = QComboBox()
        self.fileFormatDropdown.addItems([".tiff", ".gif", ".avi", ".png", ".jpeg", ".pdf", ".txt", ".csv", ".xlsx", "MATLAB workspace"])
        self.fileFormatDropdown.setFixedSize(self.fileFormatDropdown.sizeHint())
        self.layout.addWidget(self.fileFormatDropdown)

        self.layout.addStretch(1)

        self.scaleVideoDropdown = QComboBox()
        self.scaleVideoDropdown.addItems(["Original", "1 to 1"])
        self.scaleVideoDropdown.setFixedSize(self.scaleVideoDropdown.sizeHint())
        self.layout.addWidget(self.scaleVideoDropdown)

        self.force1To1Button = QPushButton("Force 1:1")
        self.force1To1Button.setToolTip("Force image and video scaling to 1:1")
        self.force1To1Button.setFixedSize(self.force1To1Button.sizeHint())
        self.layout.addWidget(self.force1To1Button)

        self.setLayout(self.layout)
# Dropdown_Module.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox
from PyQt6.QtCore import pyqtSignal

class DropdownWidget(QWidget):
    channelChanged = pyqtSignal(str)  # Signal to emit when channel changes

    def __init__(self):
        super().__init__()
        self.buildDropdownWidgets()
    
    def buildDropdownWidgets(self):
        dropdownLayout = QHBoxLayout()

        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["All files", "Processed"]) 
        self.dropdown1.setFixedSize(self.dropdown1.sizeHint())
        dropdownLayout.addWidget(self.dropdown1)

        self.dropdown2 = QComboBox()
        self.dropdown2.setFixedSize(self.dropdown2.sizeHint())
        dropdownLayout.addWidget(self.dropdown2)

        self.dropdown3 = QComboBox()
        self.dropdown3.addItems(["Stack off", "Stack on", "Intercalate"]) 
        self.dropdown3.setFixedSize(self.dropdown3.sizeHint())
        dropdownLayout.addWidget(self.dropdown3)

        dropdownLayout.addStretch(1)
        self.setLayout(dropdownLayout)

        self.dropdown1.currentIndexChanged.connect(self.onDropdown1IndexChanged)
        self.dropdown2.currentIndexChanged.connect(self.onDropdown2IndexChanged)
        self.dropdown3.currentIndexChanged.connect(self.onDropdown3IndexChanged)

    def onDropdown1IndexChanged(self):
        pass

    def onDropdown2IndexChanged(self):
        self.channelChanged.emit(self.dropdown2.currentText())  # Emit signal when channel changes
        
    def onDropdown3IndexChanged(self):
        pass

    def updateChannels(self, channels):
        self.dropdown2.clear()
        self.dropdown2.addItems(channels)

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    dropdown = DropdownWidget()
    dropdown.show()
    sys.exit(app.exec())

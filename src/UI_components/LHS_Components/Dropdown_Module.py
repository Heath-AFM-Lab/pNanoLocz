from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox

class DropdownWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildDropdownWidgets()
    
    # The variable names are poor, change them using Ctrl + F if you like 
    def buildDropdownWidgets(self):
        # Create a QHBoxLayout to contain the dropdowns
        dropdownLayout = QHBoxLayout()

        # Dropdown 1
        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["All files", "Processed"])  # Add items to the first dropdown
        self.dropdown1.setFixedSize(self.dropdown1.sizeHint())
        dropdownLayout.addWidget(self.dropdown1)

        # Dropdown 2
        self.dropdown2 = QComboBox()
        self.dropdown2.addItems(["Height"])  # Add items to the second dropdown
        self.dropdown2.setFixedSize(self.dropdown2.sizeHint())
        dropdownLayout.addWidget(self.dropdown2)

        # Dropdown 3
        self.dropdown3 = QComboBox()
        self.dropdown3.addItems(["Stack off", "Stack on", "Intercalate"])  # Add items to the third dropdown
        self.dropdown3.setFixedSize(self.dropdown3.sizeHint())
        dropdownLayout.addWidget(self.dropdown3)

        # Push dropdowns to LHS
        dropdownLayout.addStretch(1)

        # Set layout to the current widget
        self.setLayout(dropdownLayout)

        # Set names and signals of all buttons and checkbox
        self.dropdown1.currentIndexChanged.connect(self.onDropdown1IndexChanged)
        self.dropdown2.currentIndexChanged.connect(self.onDropdown2IndexChanged)
        self.dropdown3.currentIndexChanged.connect(self.onDropdown3IndexChanged)

    def onDropdown1IndexChanged(self):
        # TODO: Complete dropdown1 function
        pass

    def onDropdown2IndexChanged(self):
        # TODO: Complete dropdown2 function
        pass
        
    def onDropdown3IndexChanged(self):
        # TODO: Complete dropdown3 function
        pass


# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dropdown = DropdownWidget()
    dropdown.show()
    sys.exit(app.exec())

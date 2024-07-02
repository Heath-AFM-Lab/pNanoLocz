from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox
# from src.constants import PATH_TO_ICON_DIRECTORY


class dropdownWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildDropdownWidgets()
    
    # The variable names are poor, change them using Ctrl + F if you like 
    def buildDropdownWidgets(self):
        # Create a QHBoxLayout to contain the dropdowns
        dropdownLayout = QHBoxLayout()

        # Dropdown 1
        dropdown1 = QComboBox()
        dropdown1.addItems(["All files", "Processed"])  # Add items to the first dropdown
        dropdown1.setFixedSize(dropdown1.sizeHint())
        dropdownLayout.addWidget(dropdown1)
        

        # Dropdown 2
        dropdown2 = QComboBox()
        dropdown2.addItems(["Height"])  # Add items to the second dropdown
        dropdown2.setFixedSize(dropdown2.sizeHint())
        dropdownLayout.addWidget(dropdown2)
        

        # Dropdown 3
        dropdown3 = QComboBox()
        dropdown3.addItems(["Stack off", "Stack on", "Intercalate"])  # Add items to the third dropdown
        dropdown3.setFixedSize(dropdown3.sizeHint())
        dropdownLayout.addWidget(dropdown3)

        # Push dropdowns to LHS
        dropdownLayout.addStretch(1)

        # Create a container widget and set the layout
        dropdownWidget = QWidget()
        dropdownWidget.setLayout(dropdownLayout)

        # Set layout to the current widget
        self.setLayout(dropdownLayout)

        # Set names and signals of all buttons and checkbox
        dropdown1.currentIndexChanged.connect(self.onDropdown1IndexChanged)
        dropdown2.currentIndexChanged.connect(self.onDropdown2IndexChanged)
        dropdown3.currentIndexChanged.connect(self.onDropdown3IndexChanged)

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
    dropdown = dropdownWidget()
    dropdown.show()
    sys.exit(app.exec())

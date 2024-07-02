import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTableWidget, 
    QTableWidgetItem
)
from PyQt6.QtCore import Qt
# from src.constants import PATH_TO_ICON_DIRECTORY



class fileDetailingSystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildFileDetailingSystem()
    
    
    def buildFileDetailingSystem(self) -> QWidget:
        # Create a QHBoxLayout to contain the file selector and details box
        fileDetailingLayout = QHBoxLayout()

        # Create the widget to list the files
        fileListWidget = QListWidget()
        fileDetailingLayout.addWidget(fileListWidget)

        # Create a widget to show details of the file
        # Create the table
        fileDetailsWidget = QTableWidget()
        fileDetailsWidget.setRowCount(8)
        fileDetailsWidget.setColumnCount(2)
        
        # Set the headers
        fileDetailsWidget.setHorizontalHeaderLabels(['Parameter', 'Value'])
        
        # List of parameters
        parameters = [
            "Num Imgs", "X-Range (nm)", "Speed (fps)", "Line/s (Hz)",
            "y pixels", "x pixels", "Pixel/nm", "Channel"
        ]
        
        # TODO: Populate the table properly
        # THESE ARE TEMPORARY UNTIL A FULL FILE/FOLDER SYSTEM CAN BE IMPLEMENTED
        for i, param in enumerate(parameters):
            item = QTableWidgetItem(param)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item read-only
            fileDetailsWidget.setItem(i, 0, item)
            fileDetailsWidget.setItem(i, 1, QTableWidgetItem('0' if param != 'Channel' else 'unknown'))

        # Disable scroll bars
        fileDetailsWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        fileDetailsWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Adjust the size of the columns to fit the contents
        fileDetailsWidget.resizeColumnsToContents()
        fileDetailsWidget.resizeRowsToContents()

        # Calculate minimum width based on content
        column_width = fileDetailsWidget.verticalHeader().width()   # Account for header width and frame
        for column in range(fileDetailsWidget.columnCount()):
            column_width += fileDetailsWidget.columnWidth(column)

        # Set fixed width and calculate required height
        fileDetailsWidget.setFixedWidth(column_width)
        total_height = sum(fileDetailsWidget.rowHeight(1) for i in range(fileDetailsWidget.rowCount() + 1))     # A slightly scuffed line taking in the height of the first line only (dont edit the font of any textbox)
        fileDetailsWidget.setFixedHeight(total_height + 2 * fileDetailsWidget.frameWidth())
        
        # Add the table to the layout, pushed to the top left corner
        fileDetailslayout = QVBoxLayout()
        fileDetailslayout.addWidget(fileDetailsWidget)
        fileDetailslayout.addStretch(1)
        fileDetailingLayout.addLayout(fileDetailslayout)

        # Set layout to the current widget
        self.setLayout(fileDetailingLayout)

    def onAutosaveClick(self):
        # TODO: Complete Autosave function
        pass

    def onSaveButtonClick(self):
        # TODO: Complete save button function
        pass

# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    # TODO: remove once format correction is complete
    ICON_DIRECTORY = "../../../assets/icons"
    # Path to icon directory
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    file_detail = fileDetailingSystemWidget()
    file_detail.show()
    sys.exit(app.exec())

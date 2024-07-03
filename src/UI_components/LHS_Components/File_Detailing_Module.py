import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTableWidget, 
    QTableWidgetItem
)
from PyQt6.QtCore import Qt
class FileDetailingSystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildFileDetailingSystem()

    def buildFileDetailingSystem(self):
        # Create a QHBoxLayout to contain the file selector and details box
        fileDetailingLayout = QHBoxLayout()

        # Create the widget to list the files
        self.fileListWidget = QListWidget()
        fileDetailingLayout.addWidget(self.fileListWidget)

        # Create a widget to show details of the file
        # Create the table
        self.fileDetailsWidget = QTableWidget()
        self.fileDetailsWidget.setRowCount(8)
        self.fileDetailsWidget.setColumnCount(2)
        
        # Set the headers
        self.fileDetailsWidget.setHorizontalHeaderLabels(['Parameter', 'Value'])
        
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
            self.fileDetailsWidget.setItem(i, 0, item)
            self.fileDetailsWidget.setItem(i, 1, QTableWidgetItem('0' if param != 'Channel' else 'unknown'))

        # Disable scroll bars
        self.fileDetailsWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.fileDetailsWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Adjust the size of the columns to fit the contents
        self.fileDetailsWidget.resizeColumnsToContents()
        self.fileDetailsWidget.resizeRowsToContents()

        # Calculate minimum width based on content
        column_width = self.fileDetailsWidget.verticalHeader().width()   # Account for header width and frame
        for column in range(self.fileDetailsWidget.columnCount()):
            column_width += self.fileDetailsWidget.columnWidth(column)

        # Set fixed width and calculate required height
        self.fileDetailsWidget.setFixedWidth(column_width)
        total_height = sum(self.fileDetailsWidget.rowHeight(1) for i in range(self.fileDetailsWidget.rowCount() + 1))     # A slightly scuffed line taking in the height of the first line only (dont edit the font of any textbox)
        self.fileDetailsWidget.setFixedHeight(total_height + 2 * self.fileDetailsWidget.frameWidth())
        
        # Add the table to the layout, pushed to the top left corner
        fileDetailslayout = QVBoxLayout()
        fileDetailslayout.addWidget(self.fileDetailsWidget)
        fileDetailslayout.addStretch(1)
        fileDetailingLayout.addLayout(fileDetailslayout)

        # Set layout to the current widget
        self.setLayout(fileDetailingLayout)

        # Set names and signals of all widgets
        self.fileListWidget.itemDoubleClicked.connect(self.onFileItemDoubleClick)
        self.fileDetailsWidget.cellClicked.connect(self.onFileDetailCellClick)

    def onFileItemDoubleClick(self, item):
        # TODO: Complete load file function
        print(f"File item double-clicked: {item.text()}")

    def onFileDetailCellClick(self, row, column):
        # TODO: Handle file detail cell click
        print(f"Cell clicked at row {row}, column {column}")

# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    # TODO: remove once format correction is complete
    ICON_DIRECTORY = "../../../assets/icons"
    # Path to icon directory
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    file_detail = FileDetailingSystemWidget()
    file_detail.show()
    sys.exit(app.exec())


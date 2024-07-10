import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QTableWidget, 
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
        column_width = self.fileDetailsWidget.verticalHeader().width()
        for column in range(self.fileDetailsWidget.columnCount()):
            column_width += self.fileDetailsWidget.columnWidth(column)

        self.fileDetailsWidget.setFixedWidth(column_width)
        total_height = sum(self.fileDetailsWidget.rowHeight(1) for i in range(self.fileDetailsWidget.rowCount() + 1))
        self.fileDetailsWidget.setFixedHeight(total_height + 2 * self.fileDetailsWidget.frameWidth())

        fileDetailslayout = QVBoxLayout()
        fileDetailslayout.addWidget(self.fileDetailsWidget)
        fileDetailslayout.addStretch(1)
        fileDetailingLayout.addLayout(fileDetailslayout)

        self.setLayout(fileDetailingLayout)

        self.fileListWidget.itemDoubleClicked.connect(self.onFileItemDoubleClick)
        self.fileDetailsWidget.cellClicked.connect(self.onFileDetailCellClick)

        # Adjust size of file list widget in proportion to file details widget
        # self.fileListWidget.setFixedWidth(self.fileDetailsWidget.sizeHint().width())

    def onFileItemDoubleClick(self, item):
        print(f"File item double-clicked: {item.text()}")

    def onFileDetailCellClick(self, row, column):
        print(f"Cell clicked at row {row}, column {column}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_detail = FileDetailingSystemWidget()
    file_detail.show()
    sys.exit(app.exec())

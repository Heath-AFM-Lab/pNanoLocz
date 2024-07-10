import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt
from utils.Folder_Opener_Module.folderOpener import FolderOpener

class FileDetailingSystemWidget(QWidget):
    def __init__(self, folderOpener: FolderOpener):
        super().__init__()
        self.folderOpener = folderOpener
        self.buildFileDetailingSystem()

    def buildFileDetailingSystem(self):
        # Create a QHBoxLayout to contain the file selector and details box
        fileDetailingLayout = QHBoxLayout(self)

        # Create the widget to list the files
        self.fileTreeView = QTreeView(self)
        self.fileSystemModel = QFileSystemModel(self)
        self.fileTreeView.setModel(self.fileSystemModel)

        # Adjust column width for better file name display
        self.fileTreeView.setColumnWidth(0, 250)  # Adjust the width as needed

        # Add the file tree view to the main layout
        fileDetailingLayout.addWidget(self.fileTreeView)

        # Create a widget to show details of the file
        self.fileDetailsWidget = QTableWidget(self)
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

        # Connect the signal from FolderOpener to populateFileTree method
        self.folderOpener.folderReceived.connect(self.populateFileTree)

    def populateFileTree(self, folder_path):
        # TODO: Remove print statement
        print(f"Populating file tree with: {folder_path}")
        self.fileSystemModel.setRootPath(folder_path)
        self.fileTreeView.setRootIndex(self.fileSystemModel.index(folder_path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_detail = FileDetailingSystemWidget()
    file_detail.show()
    sys.exit(app.exec())

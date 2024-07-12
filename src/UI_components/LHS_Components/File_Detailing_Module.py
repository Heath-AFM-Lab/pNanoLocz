import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt
from utils.Folder_Opener_Module.folderOpener import FolderOpener
from PyQt6.QtCore import QSortFilterProxyModel

class CustomFileFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, extensions, parent=None):
        super().__init__(parent)
        self.extensions = extensions

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(source_row, 0, source_parent)
        if not index.isValid():
            return False

        file_path = self.sourceModel().filePath(index)
        if self.sourceModel().isDir(index):
            return True

        return any(file_path.endswith(ext) for ext in self.extensions)


class CustomFileSystemModel(QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class FileDetailingSystemWidget(QWidget):
    def __init__(self, folderOpener: FolderOpener):
        super().__init__()
        self.folderOpener = folderOpener
        self.buildFileDetailingSystem()

    def buildFileDetailingSystem(self):
        fileDetailingLayout = QHBoxLayout(self)

        self.fileTreeView = QTreeView(self)
        
        # Use the custom file system model
        self.fileSystemModel = CustomFileSystemModel(parent=self)
        
        # Use the custom filter proxy model with the desired extensions
        self.fileFilterProxyModel = CustomFileFilterProxyModel(
            extensions=['.asd', '.ibw', '.spm', '.jpk', '.gwy', '.aris', '.nhf'], parent=self
        )
        self.fileFilterProxyModel.setSourceModel(self.fileSystemModel)
        
        self.fileTreeView.setModel(self.fileFilterProxyModel)
        self.fileTreeView.setColumnWidth(0, 250)
        fileDetailingLayout.addWidget(self.fileTreeView)

        self.fileDetailsWidget = QTableWidget(self)
        self.fileDetailsWidget.setRowCount(8)
        self.fileDetailsWidget.setColumnCount(2)
        self.fileDetailsWidget.setHorizontalHeaderLabels(['Parameter', 'Value'])

        parameters = [
            "Num Imgs", "X-Range (nm)", "Speed (fps)", "Line/s (Hz)",
            "y pixels", "x pixels", "Pixel/nm", "Channel"
        ]

        for i, param in enumerate(parameters):
            item = QTableWidgetItem(param)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.fileDetailsWidget.setItem(i, 0, item)
            self.fileDetailsWidget.setItem(i, 1, QTableWidgetItem('0' if param != 'Channel' else 'unknown'))

        self.fileDetailsWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.fileDetailsWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.fileDetailsWidget.resizeColumnsToContents()
        self.fileDetailsWidget.resizeRowsToContents()

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
        self.folderOpener.folderReceived.connect(self.populateFileTree)

    def populateFileTree(self, folder_path):
        self.fileSystemModel.setRootPath(folder_path)
        self.fileTreeView.setRootIndex(self.fileFilterProxyModel.mapFromSource(self.fileSystemModel.index(folder_path)))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    folderOpener = FolderOpener()
    file_detail = FileDetailingSystemWidget(folderOpener)
    file_detail.show()
    sys.exit(app.exec())

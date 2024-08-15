import sys
from collections import Counter
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from utils.Folder_Opener_Module.Folder_Opener import FolderOpener
from utils.file_reader.File_Reader import loadFileData
import os
from utils.constants import FILE_EXTS
from core.Image_Storage_Module.Image_Storage_Class import MediaDataManager

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

    def lessThan(self, left, right):
        left_data = self.sourceModel().data(left, Qt.ItemDataRole.DisplayRole)
        right_data = self.sourceModel().data(right, Qt.ItemDataRole.DisplayRole)

        if left.column() == 1:  # Assuming size is in column 1
            left_size = self._convert_to_bytes(left_data)
            right_size = self._convert_to_bytes(right_data)
            return left_size < right_size

        return super().lessThan(left, right)

    def _convert_to_bytes(self, size_str):
        if size_str.endswith(" KiB"):
            return float(size_str.replace(" KiB", "")) * 1024
        elif size_str.endswith(" MiB"):
            return float(size_str.replace(" MiB", "")) * 1024 * 1024
        elif size_str.endswith(" GiB"):
            return float(size_str.replace(" GiB", "")) * 1024 * 1024 * 1024
        elif size_str.endswith(" B"):
            return float(size_str.replace(" B", ""))
        else:
            return 0

class CustomFileSystemModel(QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and index.column() == 1:
            file_path = self.filePath(index)
            if self.isDir(index):
                size = self._calculate_folder_size(file_path)
                return self._human_readable_size(size)
        return super().data(index, role)

    def _calculate_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_size

    def _human_readable_size(self, size, decimal_places=2):
        for unit in ['B', 'KiB', 'MiB', 'GiB']:
            if size < 1024.0:
                return f"{size:.{decimal_places}f} {unit}"
            size /= 1024.0


class FileDetailingSystemWidget(QWidget):
    def __init__(self, folderOpener: FolderOpener):
        super().__init__()
        # self.dropDown = DropdownWidget.dropdown2
        self.folderOpener = folderOpener
        self.buildFileDetailingSystem()

    def buildFileDetailingSystem(self):
        self.media_data_manager = MediaDataManager()
        fileDetailingLayout = QHBoxLayout(self)

        self.fileTreeView = QTreeView(self)
        self.fileSystemModel = CustomFileSystemModel(parent=self)
        self.fileFilterProxyModel = CustomFileFilterProxyModel(
            extensions= FILE_EXTS, parent=self
        )
        self.fileFilterProxyModel.setSourceModel(self.fileSystemModel)

        self.fileTreeView.setModel(self.fileFilterProxyModel)
        self.fileTreeView.setColumnWidth(0, 250)
        self.fileTreeView.setSortingEnabled(True)
        self.fileTreeView.doubleClicked.connect(self.onFileDoubleClicked)  # Connect double click event

        self.fileTreeView.header().sortIndicatorChanged.connect(self.onSortIndicatorChanged)
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
        self.fileDetailsWidget.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)
        self.adjustTableSize()

        fileDetailslayout = QVBoxLayout()
        fileDetailslayout.addWidget(self.fileDetailsWidget)
        fileDetailslayout.addStretch(1)
        fileDetailingLayout.addLayout(fileDetailslayout)

        self.setLayout(fileDetailingLayout)
        self.folderOpener.folderReceived.connect(self.populateFileTree)
        self.media_data_manager.new_file_loaded.connect(self.load_table_data)



    ###     DATA TABLE RELATED FUNCTIONS    ###
    def load_table_data(self):
        self.fileDetailsWidget.setItem(0, 1, QTableWidgetItem(str(self.media_data_manager.get_frames_amount())))
        self.fileDetailsWidget.setItem(1, 1, QTableWidgetItem(str(round(self.media_data_manager.get_initial_x_range(), 4))))
        self.fileDetailsWidget.setItem(2, 1, QTableWidgetItem(str(round(self.media_data_manager.get_fps_speed(), 4))))
        self.fileDetailsWidget.setItem(3, 1, QTableWidgetItem(str(round(self.media_data_manager.get_line_frequency(), 4))))
        self.fileDetailsWidget.setItem(4, 1, QTableWidgetItem(str(self.media_data_manager.get_y_dims())))
        self.fileDetailsWidget.setItem(5, 1, QTableWidgetItem(str(self.media_data_manager.get_x_dims())))
        self.fileDetailsWidget.setItem(6, 1, QTableWidgetItem(str(round(self.media_data_manager.get_initial_pix_nm_scaling(), 4))))
        self.fileDetailsWidget.setItem(7, 1, QTableWidgetItem(str(self.media_data_manager.get_cw_channel())))
        self.adjustTableSize()

    def adjustTableSize(self):
        # Resize columns to content
        self.fileDetailsWidget.resizeColumnsToContents()
        
        # Resize rows to content
        self.fileDetailsWidget.resizeRowsToContents()
        
        # Calculate total width and height
        width = self.fileDetailsWidget.verticalHeader().width() + 4  # Add some padding
        for i in range(self.fileDetailsWidget.columnCount()):
            width += self.fileDetailsWidget.columnWidth(i)
        
        height = self.fileDetailsWidget.horizontalHeader().height() + 4  # Add some padding
        for i in range(self.fileDetailsWidget.rowCount()):
            height += self.fileDetailsWidget.rowHeight(i)
        
        # Set the table widget size
        self.fileDetailsWidget.setFixedSize(width, height)


    ###     FILE SYSTEM RELATED FUNCTIONS    ###
    def onSortIndicatorChanged(self, logicalIndex, order):
        self.fileTreeView.sortByColumn(logicalIndex, order)

    def populateFileTree(self, folder_path):
        self.fileSystemModel.setRootPath(folder_path)
        self.fileTreeView.setRootIndex(self.fileFilterProxyModel.mapFromSource(self.fileSystemModel.index(folder_path)))

    def onFileDoubleClicked(self, index):
        file_path = self.fileSystemModel.filePath(self.fileFilterProxyModel.mapToSource(index))
        # This will automatically establish a new class to store the file data and metadata to
        # Call upon the class name MediaDataManager to access the values anywhere in the code
        # Repeated calls of this function will wipe any currently saved data
        loadFileData(file_path)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    folderOpener = FolderOpener()
    file_detail = FileDetailingSystemWidget(folderOpener)
    file_detail.show()
    sys.exit(app.exec())
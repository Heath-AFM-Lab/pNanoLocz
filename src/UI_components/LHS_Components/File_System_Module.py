import os
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QCheckBox, QVBoxLayout, QFileDialog, QTreeView, QDialog, QDialogButtonBox, QLabel)
from PyQt6.QtGui import QIcon, QFileSystemModel
from PyQt6.QtCore import Qt

from constants import PATH_TO_ICON_DIRECTORY

class FileSystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildFileManagementIcons()
        self.buildFileExplorerPane()

    def buildFileManagementIcons(self):
        fileManagementLayout = QHBoxLayout()

        self.autosaveCheckbox = QCheckBox("Autosave")
        self.autosaveCheckbox.setToolTip("Enable or disable autosave")
        fileManagementLayout.addWidget(self.autosaveCheckbox)

        self.saveButton = QPushButton()
        self.saveButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "save.png")))
        self.saveButton.setIconSize(self.saveButton.sizeHint())
        self.saveButton.setToolTip("Save")
        self.saveButton.setFixedSize(self.saveButton.sizeHint())
        fileManagementLayout.addWidget(self.saveButton)

        self.openFolderButton = QPushButton()
        self.openFolderButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "open.png")))
        self.openFolderButton.setIconSize(self.openFolderButton.sizeHint())
        self.openFolderButton.setToolTip("Open Folder")
        self.openFolderButton.setFixedSize(self.openFolderButton.sizeHint())
        fileManagementLayout.addWidget(self.openFolderButton)

        self.navigateOutOfDirectoryButton = QPushButton()
        self.navigateOutOfDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "up.png")))
        self.navigateOutOfDirectoryButton.setIconSize(self.navigateOutOfDirectoryButton.sizeHint())
        self.navigateOutOfDirectoryButton.setToolTip("Navigate out of Directory")
        self.navigateOutOfDirectoryButton.setFixedSize(self.navigateOutOfDirectoryButton.sizeHint())
        fileManagementLayout.addWidget(self.navigateOutOfDirectoryButton)

        self.navigateIntoDirectoryButton = QPushButton()
        self.navigateIntoDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "down.png")))
        self.navigateIntoDirectoryButton.setIconSize(self.navigateIntoDirectoryButton.sizeHint())
        self.navigateIntoDirectoryButton.setToolTip("Navigate into Directory")
        self.navigateIntoDirectoryButton.setFixedSize(self.navigateIntoDirectoryButton.sizeHint())
        fileManagementLayout.addWidget(self.navigateIntoDirectoryButton)

        fileManagementLayout.addStretch(1)

        # Create a main layout and add both file management icons and file explorer pane
        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(fileManagementLayout)
        self.setLayout(mainLayout)

        self.autosaveCheckbox.clicked.connect(self.onAutosaveClicked)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.openFolderButton.clicked.connect(self.onOpenFolderButtonClicked)
        self.navigateOutOfDirectoryButton.clicked.connect(self.onNavigateOutButtonClicked)
        self.navigateIntoDirectoryButton.clicked.connect(self.onNavigateInButtonClicked)

    def buildFileExplorerPane(self):
        self.fileTreeView = QTreeView()
        self.fileSystemModel = QFileSystemModel()
        self.fileSystemModel.setRootPath('')
        self.fileTreeView.setModel(self.fileSystemModel)
        self.fileTreeView.setRootIndex(self.fileSystemModel.index(''))

        # Adjust column width for better file name display
        self.fileTreeView.setColumnWidth(0, 250)  # Adjust the width as needed

        # Add the file tree view to the main layout
        self.layout().addWidget(self.fileTreeView)

    def onAutosaveClicked(self):
        pass

    def onSaveButtonClicked(self):
        pass

    def onOpenFolderButtonClicked(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Select a folder or a session file")

        layout = QVBoxLayout()
        label = QLabel("Select a folder or a session file")
        layout.addWidget(label)

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(lambda: self.openFolder(dialog))
        buttonBox.rejected.connect(dialog.reject)

        layout.addWidget(buttonBox)
        dialog.setLayout(layout)
        dialog.exec()

    def openFolder(self, dialog):
        dialog.accept()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            print(f"Selected folder: {folder_path}")
            self.populateFileTree(folder_path)

    def populateFileTree(self, folder_path):
        print(f"Populating file tree with: {folder_path}")
        self.fileSystemModel.setRootPath(folder_path)
        self.fileTreeView.setRootIndex(self.fileSystemModel.index(folder_path))

    def onNavigateInButtonClicked(self):
        pass

    def onNavigateOutButtonClicked(self):
        pass


if __name__ == '__main__':
    ICON_DIRECTORY = "../../../assets/icons"
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    file_system = FileSystemWidget()
    file_system.show()
    sys.exit(app.exec())

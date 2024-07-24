import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QPushButton, QCheckBox, QVBoxLayout
from PyQt6.QtGui import QIcon
from utils.Folder_Opener_Module.Folder_Opener import FolderOpener
from utils.constants import PATH_TO_ICON_DIRECTORY

class FileSystemWidget(QWidget):
    def __init__(self, folderOpener: FolderOpener):
        super().__init__()
        self.folderOpener = folderOpener
        self.buildFileManagementIcons()

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

    def onAutosaveClicked(self):
        pass

    def onSaveButtonClicked(self):
        pass

    def onOpenFolderButtonClicked(self):
        self.folderOpener.exec()

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

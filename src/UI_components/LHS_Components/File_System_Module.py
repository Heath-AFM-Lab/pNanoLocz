import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox
from PyQt6.QtGui import QIcon
from utils.constants import PATH_TO_ICON_DIRECTORY

class FileSystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildFileManagementIcons()
    
    def buildFileManagementIcons(self):
        # Create a QHBoxLayout to contain the icons
        fileManagementLayout = QHBoxLayout()

        # Add Autosave Checkbox
        self.autosaveCheckbox = QCheckBox("Autosave")
        self.autosaveCheckbox.setToolTip("Enable or disable autosave")
        fileManagementLayout.addWidget(self.autosaveCheckbox)

        # Add Save Icon
        self.saveButton = QPushButton()
        self.saveButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "save.png")))
        self.saveButton.setIconSize(self.saveButton.sizeHint())  # Adjust icon size to button size
        self.saveButton.setToolTip("Save")
        self.saveButton.setFixedSize(self.saveButton.sizeHint())
        fileManagementLayout.addWidget(self.saveButton)

        # Add Open Folder icon
        self.openFolderButton = QPushButton()
        self.openFolderButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "open.png")))
        self.openFolderButton.setIconSize(self.openFolderButton.sizeHint())  # Adjust icon size to button size
        self.openFolderButton.setToolTip("Open Folder")
        self.openFolderButton.setFixedSize(self.openFolderButton.sizeHint())
        fileManagementLayout.addWidget(self.openFolderButton)

        # Add Navigate out of Directory icon
        self.navigateOutOfDirectoryButton = QPushButton()
        self.navigateOutOfDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "up.png")))
        self.navigateOutOfDirectoryButton.setIconSize(self.navigateOutOfDirectoryButton.sizeHint())  # Adjust icon size to button size
        self.navigateOutOfDirectoryButton.setToolTip("Navigate out of Directory")
        self.navigateOutOfDirectoryButton.setFixedSize(self.navigateOutOfDirectoryButton.sizeHint())
        fileManagementLayout.addWidget(self.navigateOutOfDirectoryButton)

        # Add Navigate into Directory icon
        self.navigateIntoDirectoryButton = QPushButton()
        self.navigateIntoDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "down.png")))
        self.navigateIntoDirectoryButton.setIconSize(self.navigateIntoDirectoryButton.sizeHint())  # Adjust icon size to button size
        self.navigateIntoDirectoryButton.setToolTip("Navigate into Directory")
        self.navigateIntoDirectoryButton.setFixedSize(self.navigateIntoDirectoryButton.sizeHint())
        fileManagementLayout.addWidget(self.navigateIntoDirectoryButton)

        # Add stretch to push all widgets to LHS
        fileManagementLayout.addStretch(1)

        # Set layout to the current widget
        self.setLayout(fileManagementLayout)

        # Set names and signals of all buttons and checkbox
        self.autosaveCheckbox.clicked.connect(self.onAutosaveClicked)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.openFolderButton.clicked.connect(self.onOpenFolderButtonClicked)
        self.navigateOutOfDirectoryButton.clicked.connect(self.onNavigateOutButtonClicked)
        self.navigateIntoDirectoryButton.clicked.connect(self.onNavigateInButtonClicked)

    def onAutosaveClicked(self):
        # TODO: Complete Autosave function
        pass

    def onSaveButtonClicked(self):
        # TODO: Complete save button function
        pass
        
    def onOpenFolderButtonClicked(self):
        # TODO: Complete Open Folder function
        pass
    
    def onNavigateInButtonClicked(self):
        # TODO: Complete Navigate Into file function
        pass
    
    def onNavigateOutButtonClicked(self):
        # TODO: Complete Navigate Into file function
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
    file_system = FileSystemWidget()
    file_system.show()
    sys.exit(app.exec())

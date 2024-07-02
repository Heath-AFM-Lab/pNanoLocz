import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QCheckBox
from PyQt6.QtGui import QIcon
# from src.constants import PATH_TO_ICON_DIRECTORY

# TODO: remove once format correction is complete
ICON_DIRECTORY = "../../../assets/icons"
# Path to icon directory
PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))

class fileSystemWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildFileManagementIcons()
    
    
    def buildFileManagementIcons(self):
        # Create a QHBoxLayout to contain the icons
        fileManagementLayout = QHBoxLayout()

        # Add Autosave Checkbox
        autosaveCheckbox = QCheckBox("Autosave")
        autosaveCheckbox.setToolTip("Enable or disable autosave")
        fileManagementLayout.addWidget(autosaveCheckbox)

        # Add Save Icon
        saveButton = QPushButton()
        saveButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "save.png")))
        saveButton.setIconSize(saveButton.sizeHint())  # Adjust icon size to button size
        saveButton.setToolTip("Save")
        saveButton.setFixedSize(saveButton.sizeHint())
        fileManagementLayout.addWidget(saveButton)

        # Add Open Folder icon
        openFolderButton = QPushButton()
        openFolderButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "open.png")))
        openFolderButton.setIconSize(openFolderButton.sizeHint())  # Adjust icon size to button size
        openFolderButton.setToolTip("Open Folder")
        openFolderButton.setFixedSize(openFolderButton.sizeHint())
        fileManagementLayout.addWidget(openFolderButton)

        # Add Navigate out of Directory icon
        navigateOutOfDirectoryButton = QPushButton()
        navigateOutOfDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "up.png")))
        navigateOutOfDirectoryButton.setIconSize(navigateOutOfDirectoryButton.sizeHint())  # Adjust icon size to button size
        navigateOutOfDirectoryButton.setToolTip("Navigate out of Directory")
        navigateOutOfDirectoryButton.setFixedSize(navigateOutOfDirectoryButton.sizeHint())
        fileManagementLayout.addWidget(navigateOutOfDirectoryButton)

        # Add Navigate into Directory icon
        navigateIntoDirectoryButton = QPushButton()
        navigateIntoDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "down.png")))
        navigateIntoDirectoryButton.setIconSize(navigateIntoDirectoryButton.sizeHint())  # Adjust icon size to button size
        navigateIntoDirectoryButton.setToolTip("Navigate into Directory")
        navigateIntoDirectoryButton.setFixedSize(navigateIntoDirectoryButton.sizeHint())
        fileManagementLayout.addWidget(navigateIntoDirectoryButton)

        # Add stretch to push all widgets to LHS
        fileManagementLayout.addStretch(1)

        # Set layout to the current widget
        self.setLayout(fileManagementLayout)

        # Set names and signals of all buttons and checkbox
        autosaveCheckbox.clicked.connect(self.onAutosaveClick)
        saveButton.clicked.connect(self.onSaveButtonClick)
        openFolderButton.clicked.connect(self.onOpenFolderButtonClick)
        navigateOutOfDirectoryButton.clicked.connect(self.onNavigateOutButtonClick)
        navigateIntoDirectoryButton.clicked.connect(self.onNavigateInButtonClick)

    def onAutosaveClick(self):
        # TODO: Complete Autosave function
        pass

    def onSaveButtonClick(self):
        # TODO: Complete save button function
        pass
        
    def onOpenFolderButtonClick(self):
        # TODO: Complete Open Folder function
        pass
    
    def onNavigateInButtonClick(self):
        # TODO: Complete Navigate Into file function
        pass
    
    def onNavigateOutButtonClick(self):
        # TODO: Complete Navigate Into file function
        pass

# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_system = fileSystemWidget()
    file_system.show()
    sys.exit(app.exec())

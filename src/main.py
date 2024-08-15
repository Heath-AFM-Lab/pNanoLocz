import sys
import os
from PyQt6.QtWidgets import (
    QSizePolicy, QWidget, QApplication, QMainWindow, QFileDialog, 
    QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QAction, QIcon
from UI_components import LHSWidgets, RHSWidgets
from utils.constants import PATH_TO_ICON_DIRECTORY
from utils.Folder_Opener_Module.Folder_Opener import FolderOpener

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Instantiate classes
        self.folderOpener = FolderOpener()

        # Set up layout
        appLayout = QHBoxLayout()

        # Remove margins and spacing
        appLayout.setContentsMargins(0, 0, 0, 0)
        appLayout.setSpacing(0)

        # Create and add LHS and RHS components
        self.lhs_component = LHSWidgets(FolderOpener())
        self.rhs_component = RHSWidgets()
        appLayout.addWidget(self.lhs_component)
        appLayout.addWidget(self.rhs_component)

        # Set size policy with stretch factors on the RHS widgets
        rhsPolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        rhsPolicy.setHorizontalStretch(16)
        self.rhs_component.setSizePolicy(rhsPolicy)

        # Set LHS, RHS component names
        self.lhs_component.setObjectName("lhs_component")
        self.rhs_component.setObjectName("rhs_component")

        # Create a container widget and set the layout
        container = QWidget()
        container.setLayout(appLayout)
        self.setCentralWidget(container)

        # Set the window to be maximized
        self.showMaximized()

        # Create menu for application
        self.createMenu()

        # Add icon and title to main window
        self.setWindowIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pNanoLocz.png")))
        self.setWindowTitle("pNanoLocz")

        # Connect widgets
        self.rhs_component.videoPlayerWidgets.update_external_widgets.connect(self.lhs_component.fileDetailingWidgets.update_table_data)

    def createMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        self.createFileMenuActions(fileMenu)

    def createFileMenuActions(self, fileMenu):
        self.createAction(fileMenu, 'Open', 'Ctrl+O', self.openFile)
        self.createAction(fileMenu, 'Save', 'Ctrl+S', self.saveFile)
        fileMenu.addSeparator()
        self.createAction(fileMenu, 'Exit', 'Ctrl+Q', self.close)

    def createAction(self, menu, text, shortcut, slot):
        action = QAction(text, self)
        action.setShortcut(shortcut)
        action.triggered.connect(slot)
        menu.addAction(action)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            try:
                with open(fileName, 'r') as file:
                    self.label.setText(file.read())
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def saveFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            try:
                with open(fileName, 'w') as file:
                    file.write(self.label.text())
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec())

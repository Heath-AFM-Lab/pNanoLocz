import sys
import os
from PyQt6.QtWidgets import (
    QSizePolicy, QWidget, QApplication, QMainWindow, QFileDialog, 
    QMessageBox, QHBoxLayout
)
from PyQt6.QtGui import QAction, QIcon
from UI_components import LHSWidgets, RHSWidgets
<<<<<<< HEAD
from utils.constants import PATH_TO_ICON_DIRECTORY
=======
from utils.Folder_Opener_Module.folderOpener import FolderOpener
>>>>>>> c7025005f58f4216a4cf2f56ecd43b99a0fe8769

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
        lhsComponent = LHSWidgets(FolderOpener())
        rhsComponent = RHSWidgets()
        appLayout.addWidget(lhsComponent)
        appLayout.addWidget(rhsComponent)

        # Set size policy with stretch factors on the RHS widgets
        # lhsComponent.setFixedWidth(lhsComponent.sizeHint().width())
        # lhsPolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # lhsPolicy.setHorizontalStretch(5)
        # lhsComponent.setSizePolicy(lhsPolicy)

        rhsPolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        rhsPolicy.setHorizontalStretch(16)
        rhsComponent.setSizePolicy(rhsPolicy)

        # Set LHS, RHS component names
        lhsComponent.setObjectName("lhs_component")
        rhsComponent.setObjectName("rhs_component")

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

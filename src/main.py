import sys
from PyQt6.QtWidgets import (QSizePolicy, QWidget, QApplication, QMainWindow, 
    QFileDialog, QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QAction
from UI_components import LHSWidgets, RHSWidgets

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set up layout
        appLayout = QHBoxLayout()

        # Remove margins and spacing
        appLayout.setContentsMargins(0, 0, 0, 0)
        appLayout.setSpacing(0)

        # Create and add LHS and RHS components
        lhsComponent = LHSWidgets()
        rhsComponent = RHSWidgets()
        lhsComponent.setFixedWidth(lhsComponent.sizeHint().width())
        appLayout.addWidget(lhsComponent)
        appLayout.addWidget(rhsComponent)

        # Set LHS, RHS component names
        lhsComponent.setObjectName("lhs_component")
        rhsComponent.setObjectName("rhs_component")

        # Create a container widget and set the layout
        container = QWidget()
        container.setLayout(appLayout)
        self.setCentralWidget(container)

        # Set size policy for the main window
        size_policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setSizePolicy(size_policy)

        # Create menu for application
        self.createMenu()
    
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

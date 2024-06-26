import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QFileDialog, QMessageBox
from PyQt6.QtGui import QIcon

# Icon directory relative to current working directory
ICON_DIRECTORY = "../../assets/icons"


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('NanoLocz')
        self.setGeometry(300, 300, 400, 300)

        self.label = QLabel('Hello, World!', self)
        self.setCentralWidget(self.label)

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
    
    
    
    
    
    
    
    # def initUI(self):


    #     # Create a label
    #     self.label = QLabel('Hello, World!', self)
    #     self.setCentralWidget(self.label)

    #     # Create the menubar
    #     menubar = self.menuBar()

    #     # Add the File menu
    #     fileMenu = menubar.addMenu('File')

    #     # Create actions for the File menu
    #     openAction = QAction(QIcon(), 'Open', self)
    #     openAction.setShortcut('Ctrl+O')
    #     openAction.triggered.connect(self.openFile)

    #     saveAction = QAction(QIcon(), 'Save', self)
    #     saveAction.setShortcut('Ctrl+S')
    #     saveAction.triggered.connect(self.saveFile)

    #     exitAction = QAction(QIcon(), 'Exit', self)
    #     exitAction.setShortcut('Ctrl+Q')
    #     exitAction.triggered.connect(self.close)

    #     # Add actions to the File menu
    #     fileMenu.addAction(openAction)
    #     fileMenu.addAction(saveAction)
    #     fileMenu.addSeparator()
    #     fileMenu.addAction(exitAction)

    #     # Set the main window properties
    #     self.setWindowTitle('My PyQt5 App with Menu')
    #     self.setGeometry(300, 300, 400, 300)


    # def openFile(self):
    #     options = QFileDialog.Options()
    #     options |= QFileDialog.ReadOnly
    #     fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options)
    #     if fileName:
    #         try:
    #             with open(fileName, 'r') as file:
    #                 self.label.setText(file.read())
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", str(e))

    # def saveFile(self):
    #     options = QFileDialog.Options()
    #     fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)
    #     if fileName:
    #         try:
    #             with open(fileName, 'w') as file:
    #                 file.write(self.label.text())
    #         except Exception as e:
    #             QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
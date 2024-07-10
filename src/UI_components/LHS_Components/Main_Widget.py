import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from File_System_Module import FileSystemWidget
from File_Detailing_Module import FileDetailingSystemWidget

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        
        # Instantiate the widgets
        self.fileSystemWidget = FileSystemWidget()
        self.fileDetailingSystemWidget = FileDetailingSystemWidget()

        # Add fileSystemWidget's tree view directly to fileDetailingLayout
        fileSystemAndDetailLayout = QHBoxLayout()
        fileSystemAndDetailLayout.addWidget(self.fileSystemWidget.fileTreeView)
        fileSystemAndDetailLayout.addWidget(self.fileDetailingSystemWidget.fileDetailsWidget)

        # Add file management icons at the top
        mainLayout.addLayout(self.fileSystemWidget.layout())
        mainLayout.addLayout(fileSystemAndDetailLayout)

        self.setLayout(mainLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec())

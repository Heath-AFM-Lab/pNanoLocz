# Main_Widget.py

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from File_System_Module import FileSystemWidget
from File_Detailing_Module import FileDetailingSystemWidget
from Dropdown_Module import DropdownWidget

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()

        self.dropdown = DropdownWidget()
        self.fileSystemWidget = FileSystemWidget()
        self.fileDetailingSystemWidget = FileDetailingSystemWidget()

        # Link the file detailing system to update the dropdown
        self.fileDetailingSystemWidget.dropdown = self.dropdown

        # Connect channel change signal to the file detailing system
        self.dropdown.channelChanged.connect(self.fileDetailingSystemWidget.onChannelChanged)

        fileSystemAndDetailLayout = QHBoxLayout()
        fileSystemAndDetailLayout.addWidget(self.fileSystemWidget.fileTreeView)
        fileSystemAndDetailLayout.addWidget(self.fileDetailingSystemWidget.fileDetailsWidget)

        mainLayout.addWidget(self.dropdown)
        mainLayout.addLayout(fileSystemAndDetailLayout)

        self.setLayout(mainLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_widget = MainWidget()
    main_widget.show()
    sys.exit(app.exec())

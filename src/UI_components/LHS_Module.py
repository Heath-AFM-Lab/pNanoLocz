import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from UI_components.LHS_Components import DropdownWidget, FileDetailingSystemWidget, FileSystemWidget, TabWidget, ToggleableWidget






# class GrayButton(QPushButton):
#     def __init__(self, text, parent=None):
#         super().__init__(text, parent)
#         self.setStyleSheet('QPushButton { background-color: #f0f0f0; }'
#                            'QPushButton:pressed { background-color: #d0d0d0; }')


class LHSWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.buildLHS()

    # Function builds the left hand side of the NanoLocz program
    def buildLHS(self):
        # Build the widgets and layouts
        self.layout = QVBoxLayout(self)

        fileManagementIconsWidget = FileSystemWidget()
        dropdownWidgets = DropdownWidget()
        fileDetailingWidgets = FileDetailingSystemWidget()
        toggleableWidgets = ToggleableWidget()
        tabWidgets = TabWidget()

        self.layout.addWidget(fileManagementIconsWidget)
        self.layout.addWidget(dropdownWidgets)
        self.layout.addWidget(fileDetailingWidgets)
        self.layout.addWidget(toggleableWidgets)
        self.layout.addWidget(tabWidgets)

        self.setLayout(self.layout)        

    
# TODO: remove once finished
if __name__ == '__main__':
    app = QApplication(sys.argv)
    lhs_widgets = LHSWidgets()
    lhs_widgets.show()
    sys.exit(app.exec())
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from UI_components.LHS_Components import DropdownWidget, FileDetailingSystemWidget, FileSystemWidget, TabWidget, ToggleableWidget

class LHSWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.buildLHS()

    # Function builds the left hand side of the NanoLocz program
    def buildLHS(self):
        # Build the widgets and layouts
        self.layout = QVBoxLayout(self)

        self.fileManagementIconsWidget = FileSystemWidget()
        self.dropdownWidgets = DropdownWidget()
        self.fileDetailingWidgets = FileDetailingSystemWidget()
        self.toggleableWidgets = ToggleableWidget()
        self.tabWidgets = TabWidget()

        self.layout.addWidget(self.fileManagementIconsWidget)
        self.layout.addWidget(self.dropdownWidgets)
        self.layout.addWidget(self.fileDetailingWidgets)
        self.layout.addWidget(self.toggleableWidgets)
        self.layout.addWidget(self.tabWidgets)

        self.setLayout(self.layout)        

    
# TODO: remove once finished
if __name__ == '__main__':
    app = QApplication(sys.argv)
    lhs_widgets = LHSWidgets()
    lhs_widgets.show()
    sys.exit(app.exec())
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox
from core.cmaps import CMAPS

class VideoDropdownWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoDropdownWidgets()


    def buildVideoDropdownWidgets(self):
        # Create a QHBoxLayout to contain the dropdowns
        dropdownLayout = QHBoxLayout()

        # Change preview dropdown
        self.previewDropdown = QComboBox()
        self.previewDropdown.addItems(["Target", "Preview"])
        self.previewDropdown.setFixedSize(self.previewDropdown.sizeHint())
        dropdownLayout.addWidget(self.previewDropdown)

        # Change colour scale dropdown
        self.colourScaleDropdown = QComboBox()
        self.colourScaleDropdown.addItems(CMAPS.keys())
        self.colourScaleDropdown.setFixedSize(self.colourScaleDropdown.sizeHint())
        dropdownLayout.addWidget(self.colourScaleDropdown)

        # Change view modes dropdown
        self.viewModesDropdown = QComboBox()
        self.viewModesDropdown.addItems(["2D surface", "3D surface", "Co-ordinates"])
        self.viewModesDropdown.setFixedSize(self.viewModesDropdown.sizeHint())
        dropdownLayout.addWidget(self.viewModesDropdown)

        # Switch view dropdown
        self.switchViewDropdown = QComboBox()
        self.switchViewDropdown.addItems(["None", "Mask", "Line Profile", "Detections", "Localisations"])
        self.switchViewDropdown.setFixedSize(self.switchViewDropdown.sizeHint())
        dropdownLayout.addWidget(self.switchViewDropdown)

        # Change view modes dropdown
        self.rawOrInterpolatedDropdown = QComboBox()
        self.rawOrInterpolatedDropdown.addItems(["Original", "Interpolated"])
        self.rawOrInterpolatedDropdown.setFixedSize(self.rawOrInterpolatedDropdown.sizeHint())
        dropdownLayout.addWidget(self.rawOrInterpolatedDropdown)

        # Add spacing
        dropdownLayout.addSpacing(20)

        # Add last dropdown (it seems to just be "Off", but edited later once video is processed)
        # TODO: investigate the rest of the items that are meant to be in here
        # and rename this variable using Ctrl + F to find and replace
        self.dropdown6 = QComboBox()
        self.dropdown6.addItems(["Off"])
        self.dropdown6.setFixedSize(self.dropdown6.sizeHint())
        dropdownLayout.addWidget(self.dropdown6)

        # Push all dropdowns to the LHS
        dropdownLayout.addStretch(1)

        # Set layout to the current widget
        self.setLayout(dropdownLayout)

        # Set signals of all widgets
        self.previewDropdown.currentIndexChanged.connect(self.onPreviewDropdownChanged)
        self.colourScaleDropdown.currentIndexChanged.connect(self.onColourScaleDropdownChanged)
        self.viewModesDropdown.currentIndexChanged.connect(self.onViewModesDropdownChanged)
        self.switchViewDropdown.currentIndexChanged.connect(self.onSwitchViewDropdownChanged)
        self.rawOrInterpolatedDropdown.currentIndexChanged.connect(self.onRawOrInterpolatedDropdownChanged)
        self.dropdown6.currentIndexChanged.connect(self.onDropdown6Changed)

    def onPreviewDropdownChanged(self, index):
        # TODO: Handle preview dropdown change
        pass

    def onColourScaleDropdownChanged(self, index):
        # TODO: Handle colour scale dropdown change
        pass

    def onViewModesDropdownChanged(self, index):
        # TODO: Handle view modes dropdown change
        pass

    def onSwitchViewDropdownChanged(self, index):
        # TODO: Handle switch view dropdown change
        pass

    def onRawOrInterpolatedDropdownChanged(self, index):
        # TODO: Handle raw or interpolated dropdown change
        pass

    def onDropdown6Changed(self, index):
        # TODO: Handle dropdown6 change
        pass


# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys, os

if __name__ == '__main__':
    # TODO: remove once format correction is complete
    ICON_DIRECTORY = "../../../assets/icons"
    # Path to icon directory
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    file_system = VideoDropdownWidget()
    file_system.show()
    sys.exit(app.exec())
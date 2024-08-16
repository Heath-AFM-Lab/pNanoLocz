from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox
from core.Colormaps_Module.Colormaps import CMAPS
from core.Image_Storage_Module.Media_Data_Manager_Class import MediaDataManager

class VideoDropdownWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoDropdownWidgets()


    def buildVideoDropdownWidgets(self):
        # Create a QHBoxLayout to contain the dropdowns
        self.media_data_manager = MediaDataManager()
        dropdownLayout = QHBoxLayout()

        # Change preview dropdown
        self.view_mode_dropdown = QComboBox()
        self.view_mode_dropdown.addItems(self.media_data_manager.get_mode_list())
        self.view_mode_dropdown.setFixedSize(self.view_mode_dropdown.sizeHint())
        dropdownLayout.addWidget(self.view_mode_dropdown)

        # Change colour scale dropdown
        self.colourScaleDropdown = QComboBox()
        self.colourScaleDropdown.addItems(CMAPS.keys())
        self.colourScaleDropdown.setFixedSize(self.colourScaleDropdown.sizeHint())
        dropdownLayout.addWidget(self.colourScaleDropdown)

        # Change view modes dropdown
        self.surfaceOptionsDropdown = QComboBox()
        self.surfaceOptionsDropdown.addItems(["2D surface", "3D surface", "Co-ordinates"])
        self.surfaceOptionsDropdown.setFixedSize(self.surfaceOptionsDropdown.sizeHint())
        dropdownLayout.addWidget(self.surfaceOptionsDropdown)

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
        self.view_mode_dropdown.currentTextChanged.connect(self.on_view_mode_changed)
        self.colourScaleDropdown.currentIndexChanged.connect(self.onColourScaleDropdownChanged)
        self.surfaceOptionsDropdown.currentIndexChanged.connect(self.onViewModesDropdownChanged)
        self.switchViewDropdown.currentIndexChanged.connect(self.onSwitchViewDropdownChanged)
        self.rawOrInterpolatedDropdown.currentIndexChanged.connect(self.onRawOrInterpolatedDropdownChanged)
        self.dropdown6.currentIndexChanged.connect(self.onDropdown6Changed)

        # Signals coming from the media data manager
        self.media_data_manager.current_mode_changed.connect(self.set_current_mode)

    def on_view_mode_changed(self, mode):
        self.media_data_manager.set_mode(mode=mode)

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
    
    def set_current_mode(self, mode):
        self.view_mode_dropdown.setCurrentText(mode)

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
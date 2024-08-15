import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QComboBox, 
    QSpinBox
)
from core.Image_Storage_Module.Media_Data_Manager_Class import MediaDataManager

class ToggleableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildToggleableWidgets()

    def buildToggleableWidgets(self):
        media_data_manager = MediaDataManager()
        
        # Building 2 QHBoxLayouts to construct 1 QVBoxLayout, and saving that as a widget
        topHorizontalLayout = QHBoxLayout()
        bottomHorizontalLayout = QHBoxLayout()
        toggleableWidgetsLayout = QVBoxLayout()

        # Fill top row with check boxes
        # Add Auto play Checkbox
        self.autoplayCheckbox = QCheckBox("Auto play")
        self.autoplayCheckbox.setToolTip("Enable or disable Auto play")
        topHorizontalLayout.addWidget(self.autoplayCheckbox)

        # Add Bi-directional data Checkbox
        self.biDirectionalDataCheckbox = QCheckBox("Bi-directional data")
        self.biDirectionalDataCheckbox.setToolTip("Bi-directional scan - How to check: Trace will appear as smoothed ReTrace")
        topHorizontalLayout.addWidget(self.biDirectionalDataCheckbox)

        # Add stretch pushes togglable checkboxes away from view preview button
        topHorizontalLayout.addStretch(1)

        # Add button to toggle preview
        self.togglePreviewButton = QPushButton("Preview On/Off")
        topHorizontalLayout.addWidget(self.togglePreviewButton)


        # Fill bottom row with toggleable switch and frames
        # Add Load all frames Checkbox
        self.loadAllFrames = QCheckBox("Load all frames")
        self.loadAllFrames.setToolTip("Disable to select quantity of frames to load")
        self.loadAllFrames.setChecked(True)

        bottomHorizontalLayout.addWidget(self.loadAllFrames)

        # Add spin box for quantity of frames 
        # NEEDS TO BE CHANGED TO FIT THE ACTUAL NUMBER OF FRAMES BY SLOT
        # TODO: Add a label next to the frameSpinBox to indicate what the spinbox does
        self.frameSpinBox = QSpinBox()
        self.frameSpinBox.setMinimum(0)
        self.frameSpinBox.setMaximum(100000)
        self.frameSpinBox.setSingleStep(1)
        self.frameSpinBox.setEnabled(False)
        self.frameSpinBox.setFixedSize(self.frameSpinBox.sizeHint())
        bottomHorizontalLayout.addWidget(self.frameSpinBox)

        # Separate (by space) frames selection from frames/particles view
        bottomHorizontalLayout.addStretch(1)

        # Add dropdown for either frames or particles
        # We can implement the toggle switch but for the concept we will keep it simple
        self.particlesOrFramesDropdown = QComboBox()
        self.particlesOrFramesDropdown.addItems(["Frames", "Particles"])
        bottomHorizontalLayout.addWidget(self.particlesOrFramesDropdown)
        
        # Store all layouts to the vertical layout
        toggleableWidgetsLayout.addLayout(topHorizontalLayout)
        toggleableWidgetsLayout.addLayout(bottomHorizontalLayout)

        # Set layout to the current widget
        self.setLayout(toggleableWidgetsLayout)

        # Set names and signals of all widgets
        self.autoplayCheckbox.stateChanged.connect(self.onAutoplayStateChanged)
        self.biDirectionalDataCheckbox.clicked.connect(self.onBiDirectionalDataClicked)
        self.togglePreviewButton.clicked.connect(self.onTogglePreviewButtonClicked)
        self.loadAllFrames.clicked.connect(self.onLoadAllFramesClicked)
        self.frameSpinBox.valueChanged.connect(self.onFrameSpinBoxValueChanged)
        self.particlesOrFramesDropdown.currentIndexChanged.connect(self.onParticlesOrFramesDropdownChanged)


    def onAutoplayStateChanged(self, state):
        # TODO: Handle autoplay checkbox state change
        pass

    def onBiDirectionalDataClicked(self, checked):
        # TODO: Handle bi-directional data checkbox click
        pass

    def onTogglePreviewButtonClicked(self):
        # TODO: Handle preview button click
        pass

    def onLoadAllFramesClicked(self, checked):
        # Handle load all frames checkbox click
        self.frameSpinBox.setEnabled(not checked)

    def onFrameSpinBoxValueChanged(self, value):
        # TODO: Handle frame spin box value change
        pass

    def onParticlesOrFramesDropdownChanged(self, index):
        # TODO: Handle particles or frames dropdown index change
        pass




# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys

# TODO: remove once finished
if __name__ == '__main__':
    ICON_DIRECTORY = "../../../assets/icons"
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    toggleable_widget = ToggleableWidget()
    toggleable_widget.show()
    sys.exit(app.exec())

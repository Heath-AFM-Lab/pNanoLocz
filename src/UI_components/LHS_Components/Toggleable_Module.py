import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, 
    QSpinBox, QLabel, QComboBox
)
from core.Image_Storage_Module.Media_Data_Manager_Class import MediaDataManager

class ToggleableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildToggleableWidgets()

    def buildToggleableWidgets(self):
        self.media_data_manager = MediaDataManager()
        
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
        self.view_mode_button = QPushButton("Preview on")
        self.view_mode_button.clicked.connect(self.toggle_view_mode)
        topHorizontalLayout.addWidget(QLabel("View mode selection:"))
        topHorizontalLayout.addWidget(self.view_mode_button)

        # Fill bottom row with toggleable switch and frames
        # Add Load all frames Checkbox
        self.loadAllFrames = QCheckBox("Load all frames")
        self.loadAllFrames.setToolTip("Disable to select quantity of frames to load")
        self.loadAllFrames.setChecked(True)

        bottomHorizontalLayout.addWidget(self.loadAllFrames)

        # Add spin box for quantity of frames 
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
        self.loadAllFrames.clicked.connect(self.onLoadAllFramesClicked)
        self.frameSpinBox.valueChanged.connect(self.onFrameSpinBoxValueChanged)
        self.particlesOrFramesDropdown.currentIndexChanged.connect(self.onParticlesOrFramesDropdownChanged)

        # Signals coming from the media data manager
        self.media_data_manager.current_mode_changed.connect(self.set_current_mode)

    def toggle_view_mode(self):
        # Toggle between 'Target' and 'Preview'
        current_mode = self.media_data_manager.get_mode()
        new_mode = "Preview" if current_mode == "Target" else "Target"
        self.media_data_manager.set_mode(new_mode)
        self.update_view_mode_button_text(new_mode)

    def update_view_mode_button_text(self, mode):
        # Update button text based on the current mode
        if mode == "Target":
            self.view_mode_button.setText("Preview on")
        else:
            self.view_mode_button.setText("Preview off")

    def onAutoplayStateChanged(self, state):
        # TODO: Handle autoplay checkbox state change
        pass

    def onBiDirectionalDataClicked(self, checked):
        # TODO: Handle bi-directional data checkbox click
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

    def set_current_mode(self, mode):
        self.update_view_mode_button_text(mode)

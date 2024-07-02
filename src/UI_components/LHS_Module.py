import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QListWidget, QComboBox, QTableWidget, 
    QTableWidgetItem, QSpinBox, QTabWidget, QLabel
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from constants import ICON_DIRECTORY
# from src.UI_components.LHS_Components.





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

        fileManagementIconsWidget = self.buildFileManagementIcons()
        dropdownWidgets = self.buildDropdownWidgets()
        fileDetailingWidgets = self.buildFileDetailingSystem()
        toggleableWidgets = self.buildToggleableWidgets()
        tabWidgets = self.buildTabWidget()

        self.layout.addWidget(fileManagementIconsWidget)
        self.layout.addWidget(dropdownWidgets)
        self.layout.addWidget(fileDetailingWidgets)
        self.layout.addWidget(toggleableWidgets)
        self.layout.addWidget(tabWidgets)

        self.setLayout(self.layout)

    def buildFileDetailingSystem(self) -> QWidget:
        # Create a QHBoxLayout to contain the file selector and details box
        fileDetailingLayout = QHBoxLayout()

        # Create the widget to list the files
        fileListWidget = QListWidget()
        fileDetailingLayout.addWidget(fileListWidget)

        # Create a widget to show details of the file
        # Create the table
        fileDetailsWidget = QTableWidget()
        fileDetailsWidget.setRowCount(8)
        fileDetailsWidget.setColumnCount(2)
        
        # Set the headers
        fileDetailsWidget.setHorizontalHeaderLabels(['Parameter', 'Value'])
        
        # List of parameters
        parameters = [
            "Num Imgs", "X-Range (nm)", "Speed (fps)", "Line/s (Hz)",
            "y pixels", "x pixels", "Pixel/nm", "Channel"
        ]
        
        # TODO: Populate the table properly
        # THESE ARE TEMPORARY UNTIL A FULL FILE/FOLDER SYSTEM CAN BE IMPLEMENTED
        for i, param in enumerate(parameters):
            item = QTableWidgetItem(param)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the item read-only
            fileDetailsWidget.setItem(i, 0, item)
            fileDetailsWidget.setItem(i, 1, QTableWidgetItem('0' if param != 'Channel' else 'unknown'))

        # Disable scroll bars
        fileDetailsWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        fileDetailsWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Adjust the size of the columns to fit the contents
        fileDetailsWidget.resizeColumnsToContents()
        fileDetailsWidget.resizeRowsToContents()

        # Calculate minimum width based on content
        column_width = fileDetailsWidget.verticalHeader().width()   # Account for header width and frame
        for column in range(fileDetailsWidget.columnCount()):
            column_width += fileDetailsWidget.columnWidth(column)

        # Set fixed width and calculate required height
        fileDetailsWidget.setFixedWidth(column_width)
        total_height = sum(fileDetailsWidget.rowHeight(1) for i in range(fileDetailsWidget.rowCount() + 1))     # A slightly scuffed line taking in the height of the first line only (dont edit the font of any textbox)
        fileDetailsWidget.setFixedHeight(total_height + 2 * fileDetailsWidget.frameWidth())
        
        # Add the table to the layout, pushed to the top left corner
        fileDetailslayout = QVBoxLayout()
        fileDetailslayout.addWidget(fileDetailsWidget)
        fileDetailslayout.addStretch(1)
        fileDetailingLayout.addLayout(fileDetailslayout)

        # Create a container widget and set the layout
        fileDetailingWidget = QWidget()
        fileDetailingWidget.setLayout(fileDetailingLayout)
        
        return fileDetailingWidget


    def buildToggleableWidgets(self) -> QWidget:
        # Building 2 QHBoxLayouts to construct 1 QVBoxLayout, and saving that as a widget
        topHorizontalLayout = QHBoxLayout()
        bottomHorizontalLayout = QHBoxLayout()
        toggleableWidgetsLayout = QVBoxLayout()

        # Fill top row with check boxes
        # Add Auto play Checkbox
        autoplayCheckbox = QCheckBox("Auto play")
        autoplayCheckbox.setToolTip("Enable or disable Auto play")
        topHorizontalLayout.addWidget(autoplayCheckbox)

        # Add Bi-directional data Checkbox
        biDirectionalDataCheckbox = QCheckBox("Bi-directional data")
        biDirectionalDataCheckbox.setToolTip("Bi-directional scan - How to check: Trace will appear as smoothed ReTrace")
        topHorizontalLayout.addWidget(biDirectionalDataCheckbox)

        # Add stretch pushes togglable checkboxes away from view preview button
        topHorizontalLayout.addStretch(1)

        # Add button to toggle preview
        # This is a custom button coming from an inhereted class QPushButton. It should be accompanied with the function buildToggleableWidgets() unless otherwise discussed (in reference to some stylesheet)
        # Custom button commented out
        # We can change this to actually change text. I havent coded any slots or signals yet
        togglePreviewButton = QPushButton("Preview On/Off")
        topHorizontalLayout.addWidget(togglePreviewButton)


        # Fill bottom row with toggleable switch and frames
        # Add Load all frames Checkbox
        loadAllFrames = QCheckBox("Load all frames")
        loadAllFrames.setToolTip("Disable to select quantity of frames to load")
        loadAllFrames.setChecked(True)
        loadAllFrames.clicked.connect(self.onLoadAllFramesClicked)
        loadAllFrames.setObjectName("loadAllFramesCheckbox")
        bottomHorizontalLayout.addWidget(loadAllFrames)

        # Add spin box for quantity of frames 
        # NEEDS TO BE CHANGED TO FIT THE ACTUAL NUMBER OF FRAMES BY SLOT
        # TODO: Add a label next to the frameSpinBox to indicate what the spinbox does
        frameSpinBox = QSpinBox()
        frameSpinBox.setMinimum(0)
        frameSpinBox.setMaximum(100000)
        frameSpinBox.setSingleStep(1)
        frameSpinBox.setObjectName("frameSpinBox")
        frameSpinBox.setEnabled(False)
        frameSpinBox.setFixedSize(frameSpinBox.sizeHint())
        bottomHorizontalLayout.addWidget(frameSpinBox)

        # Separate (by space) frames selection from frames/particles view
        bottomHorizontalLayout.addStretch(1)

        # Add dropdown for either frames or particles
        # We can implement the toggle switch (I have the code) but for the concept we will keep it simple

        particlesOrFramesDropdown = QComboBox()
        particlesOrFramesDropdown.addItems(["Frames", "Particles"])
        bottomHorizontalLayout.addWidget(particlesOrFramesDropdown)

        
        # Store all layouts to the vertical layout
        toggleableWidgetsLayout.addLayout(topHorizontalLayout)
        toggleableWidgetsLayout.addLayout(bottomHorizontalLayout)

        # Create a container widget and set the layout
        toggleableWidgetsWidget = QWidget()
        toggleableWidgetsWidget.setLayout(toggleableWidgetsLayout)

        return toggleableWidgetsWidget


    
    def onLoadAllFramesClicked(self, checked):
        loadAllFramesCheckbox = self.findChild(QCheckBox, "loadAllFramesCheckbox")
        frameSpinBox = self.findChild(QSpinBox, "frameSpinBox")

        if loadAllFramesCheckbox and frameSpinBox:
            frameSpinBox.setEnabled(not checked)
        


    def buildTabWidget(self):
        # Create the tab widget
        tabs = QTabWidget()
        
        # Create tabs
        home_tab = QWidget()
        level_tab = QWidget()
        detect_tab = QWidget()
        finealign_tab = QWidget()
        localize_tab = QWidget()
        
        # Add tabs to the widget
        tabs.addTab(home_tab, "Home")
        tabs.addTab(level_tab, "Level")
        tabs.addTab(detect_tab, "Detect")
        tabs.addTab(finealign_tab, "FineAlign")
        tabs.addTab(localize_tab, "Localize")
        
        # Set up the tab contents
        self.setupTab(home_tab, "Home Content", QColor('black'))
        self.setupTab(level_tab, "Level Content", QColor('red'))
        self.setupTab(detect_tab, "Detect Content", QColor('blue'))
        self.setupTab(finealign_tab, "FineAlign Content", QColor('orange'))
        self.setupTab(localize_tab, "Localize Content", QColor('magenta'))
        
        return tabs
    
    # Function stands incomplete as priority is to develop a video player application first
    # TODO: develop the individual 5 tabs as per the MatLab NanoLocz app
    def setupTab(self, tab, content, color):
        layout = QVBoxLayout()
        label = QLabel(content)
        label.setStyleSheet(f"color: {color.name()};")
        layout.addWidget(label)
        
        tab.setLayout(layout)
    
# TODO: remove once finished
if __name__ == '__main__':
    app = QApplication(sys.argv)
    lhs_widgets = LHSWidgets()
    lhs_widgets.show()
    sys.exit(app.exec())
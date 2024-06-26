import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QListWidget, QComboBox, QTableWidget, 
    QTableWidgetItem, QSpinBox, QTabWidget, QLabel
)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt

# Icon directory relative to current working directory
ICON_DIRECTORY = "../../assets/icons"

# Path to icon directory
PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))



class GrayButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet('QPushButton { background-color: #f0f0f0; }'
                           'QPushButton:pressed { background-color: #d0d0d0; }')


class LHSWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.buildLHS()

    # Function builds the left hand side of the NanoLocz program
    def buildLHS(self) -> QWidget:
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

    def buildFileManagementIcons(self) -> QWidget:
        # Create a QHBoxLayout to contain the icons
        fileManagementLayout = QHBoxLayout()

        # Add Autosave Checkbox
        autosaveCheckbox = QCheckBox("Autosave")
        autosaveCheckbox.setToolTip("Enable or disable autosave")
        fileManagementLayout.addWidget(autosaveCheckbox)

        # Add Save Icon
        saveButton = QPushButton()
        saveButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "save.png")))
        saveButton.setIconSize(saveButton.sizeHint())  # Adjust icon size to button size
        saveButton.setToolTip("Save")
        fileManagementLayout.addWidget(saveButton)

        # Add Open Folder icon
        openFolderButton = QPushButton()
        openFolderButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "open.png")))
        openFolderButton.setIconSize(openFolderButton.sizeHint())  # Adjust icon size to button size
        openFolderButton.setToolTip("Open Folder")
        fileManagementLayout.addWidget(openFolderButton)

        # Add Navigate out of Directory icon
        navigateOutOfDirectoryButton = QPushButton()
        navigateOutOfDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "up.png")))
        navigateOutOfDirectoryButton.setIconSize(navigateOutOfDirectoryButton.sizeHint())  # Adjust icon size to button size
        navigateOutOfDirectoryButton.setToolTip("Navigate out of Directory")
        fileManagementLayout.addWidget(navigateOutOfDirectoryButton)

        # Add Navigate into Directory icon
        navigateIntoDirectoryButton = QPushButton()
        navigateIntoDirectoryButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "down.png")))
        navigateIntoDirectoryButton.setIconSize(navigateIntoDirectoryButton.sizeHint())  # Adjust icon size to button size
        navigateIntoDirectoryButton.setToolTip("Navigate into Directory")
        fileManagementLayout.addWidget(navigateIntoDirectoryButton)

        # Create a container widget and set the layout
        fileManagementWidget = QWidget()
        fileManagementWidget.setLayout(fileManagementLayout)

        return fileManagementWidget

    def buildDropdownWidgets(self) -> QWidget:
        # Create a QHBoxLayout to contain the dropdowns
        dropdownLayout = QHBoxLayout()

        # Dropdown 1
        dropdown1 = QComboBox()
        dropdown1.addItems(["All files", "Processed"])  # Add items to the first dropdown
        dropdownLayout.addWidget(dropdown1)

        # Dropdown 2
        dropdown2 = QComboBox()
        dropdown2.addItems(["Height"])  # Add items to the second dropdown
        dropdownLayout.addWidget(dropdown2)

        # Dropdown 3
        dropdown3 = QComboBox()
        dropdown3.addItems(["Stack off", "Stack On", "Intercalate"])  # Add items to the third dropdown
        dropdownLayout.addWidget(dropdown3)

        # Create a container widget and set the layout
        dropdownWidget = QWidget()
        dropdownWidget.setLayout(dropdownLayout)

        return dropdownWidget

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
        
        # Populate the table
        # THESE ARE TEMPORARY UNTIL A FULL FILE/FOLDER SYSTEM CAN BE IMPLEMENTED
        for i, param in enumerate(parameters):
            item = QTableWidgetItem(param)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the item read-only
            fileDetailsWidget.setItem(i, 0, item)
            fileDetailsWidget.setItem(i, 1, QTableWidgetItem('0' if param != 'Channel' else 'unknown'))

        # Disable scroll bars
        fileDetailsWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        fileDetailsWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
        
        # Add the table to the layout
        fileDetailingLayout.addWidget(fileDetailsWidget)

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
        # We can change this to actually change text. I havent coded any slots or signals yet
        togglePreviewButton = GrayButton("Preview On/Off")
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
    
    def setupTab(self, tab, content, color):
        layout = QVBoxLayout()
        label = QLabel(content)
        label.setStyleSheet(f"color: {color.name()};")
        layout.addWidget(label)
        
        # Add more widgets if needed
        button = QPushButton("Button in " + content)
        layout.addWidget(button)
        
        tab.setLayout(layout)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lhs_widgets = LHSWidgets()
    lhs_widgets.show()
    sys.exit(app.exec_())
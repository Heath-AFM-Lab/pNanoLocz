import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from constants import PATH_TO_ICON_DIRECTORY

class VideoEditingIconsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoEditingIcons()
    
    def buildVideoEditingIcons(self):
        # Create a QHBoxLayout to contain the icons
        videoEditingIconsLayout = QHBoxLayout()

        # Add Settings Icon
        self.settingsButton = QPushButton()
        self.settingsButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "settings.png")))
        self.settingsButton.setIconSize(self.settingsButton.sizeHint())  # Adjust icon size to button size
        self.settingsButton.setToolTip("Settings")
        self.settingsButton.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.settingsButton)

        # Add Reset Icon
        self.resetButton = QPushButton("Reset")
        self.resetButton.setToolTip("Reset annotated video to original")
        self.resetButton.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.resetButton)

        # Add Data tips Icon 
        self.dataTipsButton = QPushButton()
        self.dataTipsButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "multi_point.png")))
        self.dataTipsButton.setIconSize(self.dataTipsButton.sizeHint())  # Adjust icon size to button size
        self.dataTipsButton.setToolTip("Data tips")
        self.dataTipsButton.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.dataTipsButton)

        # Add Draw reference area Icon 
        self.drawReferenceAreaIcon = QPushButton()
        self.drawReferenceAreaIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "roi_sq.png")))
        self.drawReferenceAreaIcon.setIconSize(self.drawReferenceAreaIcon.sizeHint())  # Adjust icon size to button size
        self.drawReferenceAreaIcon.setToolTip("Draw reference area")
        self.drawReferenceAreaIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.drawReferenceAreaIcon)

        # Add Height profile over time Icon 
        self.heightProfileOverTimeIcon = QPushButton()
        self.heightProfileOverTimeIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "ZProfile.png")))
        self.heightProfileOverTimeIcon.setIconSize(self.heightProfileOverTimeIcon.sizeHint())  # Adjust icon size to button size
        self.heightProfileOverTimeIcon.setToolTip("Height profile over time")
        self.heightProfileOverTimeIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.heightProfileOverTimeIcon)

        # Add Line profile Icon 
        self.lineProfileIcon = QPushButton()
        self.lineProfileIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "line.png")))
        self.lineProfileIcon.setIconSize(self.lineProfileIcon.sizeHint())  # Adjust icon size to button size
        self.lineProfileIcon.setToolTip("Line profile")
        self.lineProfileIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.lineProfileIcon)

        # Add Zoom Icon 
        self.zoomIcon = QPushButton()
        self.zoomIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "zoomin.png")))
        self.zoomIcon.setIconSize(self.zoomIcon.sizeHint())  # Adjust icon size to button size
        self.zoomIcon.setToolTip("Zoom")
        self.zoomIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.zoomIcon)

        # There seems to be a very small gap in the NanoLocz program between these widgets
        # Not sure if intentional
        videoEditingIconsLayout.addSpacing(10)

        # Add Crop Icon 
        self.cropIcon = QPushButton()
        self.cropIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "crop.png")))
        self.cropIcon.setIconSize(self.cropIcon.sizeHint())  # Adjust icon size to button size
        self.cropIcon.setToolTip("Crop")
        self.cropIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.cropIcon)

        # Add Kymograph from line profile Icon
        self.kymographIcon = QPushButton()
        self.kymographIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "kymo.png")))
        self.kymographIcon.setIconSize(self.kymographIcon.sizeHint())  # Adjust icon size to button size
        self.kymographIcon.setToolTip("Kymograph from line profile")
        self.kymographIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.kymographIcon)

        # Add Image montage Icon
        self.imageMontageIcon = QPushButton()
        self.imageMontageIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "montage.png")))
        self.imageMontageIcon.setIconSize(self.imageMontageIcon.sizeHint())  # Adjust icon size to button size
        self.imageMontageIcon.setToolTip("Image montage")
        self.imageMontageIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.imageMontageIcon)

        # Add View data Icon
        self.viewDataIcon = QPushButton()
        self.viewDataIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "plotter.png")))
        self.viewDataIcon.setIconSize(self.viewDataIcon.sizeHint())  # Adjust icon size to button size
        self.viewDataIcon.setToolTip("View data")
        self.viewDataIcon.setFixedSize(38, 38)
        videoEditingIconsLayout.addWidget(self.viewDataIcon)

        # Add stretch to push all widgets to LHS
        videoEditingIconsLayout.addStretch(1)

        # Set layout to the current widget
        self.setLayout(videoEditingIconsLayout)

        # Set names and signals of all buttons and checkbox
        self.settingsButton.clicked.connect(self.onSettingsButtonClicked)
        self.resetButton.clicked.connect(self.onResetButtonClicked)
        self.dataTipsButton.clicked.connect(self.onDataTipsButtonClicked)
        self.drawReferenceAreaIcon.clicked.connect(self.onDrawReferenceAreaIconClicked)
        self.heightProfileOverTimeIcon.clicked.connect(self.onHeightProfileOverTimeIconClicked)
        self.lineProfileIcon.clicked.connect(self.onLineProfileIconClicked)
        self.zoomIcon.clicked.connect(self.onZoomIconClicked)
        self.cropIcon.clicked.connect(self.onCropIconClicked)
        self.kymographIcon.clicked.connect(self.onKymographIconClicked)
        self.imageMontageIcon.clicked.connect(self.onImageMontageIconClicked)
        self.viewDataIcon.clicked.connect(self.onViewDataIconClicked)


    def onSettingsButtonClicked(self):
        # TODO: Complete Settings function
        pass

    def onResetButtonClicked(self):
        # TODO: Complete Reset button function
        pass
        
    def onDataTipsButtonClicked(self):
        # TODO: Complete Data Tips function
        pass
    
    def onDrawReferenceAreaIconClicked(self):
        # TODO: Complete Draw Reference Area function
        pass
    
    def onHeightProfileOverTimeIconClicked(self):
        # TODO: Complete Height Profile Over Time function
        pass

    def onLineProfileIconClicked(self):
        # TODO: Complete Navigate Into file function
        pass

    def onZoomIconClicked(self):
        # TODO: Complete Zoom function
        pass

    def onCropIconClicked(self):
        # TODO: Complete Crop function
        pass
    
    def onKymographIconClicked(self):
        # TODO: Complete Kymograph function
        pass

    def onImageMontageIconClicked(self):
        # TODO: Complete Image Montage function
        pass


    def onViewDataIconClicked(self):
        # TODO: Complete View Data function
        pass





# TODO: remove once finished
from PyQt6.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    # TODO: remove once format correction is complete
    ICON_DIRECTORY = "../../../assets/icons"
    # Path to icon directory
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    file_system = VideoEditingIconsWidget()
    file_system.show()
    sys.exit(app.exec())

import sys
import os
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QListWidget, QComboBox, QTableWidget, 
    QTableWidgetItem, QSpinBox, QTabWidget, QLabel, QLineEdit, QSlider
)
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QIcon, QIntValidator, QValidator
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QSizePolicy



# Icon directory relative to current working directory
# TODO: change back relative to main.py (Remove ..)
ICON_DIRECTORY = "../../assets/icons"

# Path to icon directory
PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))

class RHSWidgets(QWidget):
    def __init__(self):
        super().__init__()
        self.buildLHS()

    # Function builds the left hand side of the NanoLocz program
    def buildLHS(self) -> QWidget:
        # Build the widgets and layouts
        self.layout = QVBoxLayout(self)

        videoEditingIconsWidget = self.buildVideoEditingIcons()
        videoDropdownWidgets = self.buildVideoDropdownWidgets()
        videoPlayerWidgets = self.buildVideoPlayerWidgets()
        # videoAndParticleControlWidgets = self.buildVideoAndParticleControlWidgets()

        self.layout.addWidget(videoEditingIconsWidget)
        self.layout.addWidget(videoDropdownWidgets)
        self.layout.addWidget(videoPlayerWidgets)
        # self.layout.addWidget(videoAndParticleControlWidgets)
        
        self.setLayout(self.layout)

    def buildVideoEditingIcons(self) -> QWidget:
        # Create a QHBoxLayout to contain the icons
        videoEditingIcons = QHBoxLayout()

        # Add Settings Icon
        settingsButton = QPushButton()
        settingsButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "settings.png")))
        settingsButton.setIconSize(settingsButton.sizeHint())  # Adjust icon size to button size
        settingsButton.setToolTip("Settings")
        settingsButton.setFixedSize(38, 38)

        videoEditingIcons.addWidget(settingsButton)

        # Add Reset Icon
        resetButton = QPushButton("Reset")
        resetButton.setIconSize(resetButton.sizeHint())  # Adjust icon size to button size
        resetButton.setToolTip("Reset annotated video to original")
        resetButton.setFixedSize(38, 38)
        videoEditingIcons.addWidget(resetButton)

        # Add Data tips Icon 
        dataTipsButton = QPushButton()
        dataTipsButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "multi_point.png")))
        dataTipsButton.setIconSize(dataTipsButton.sizeHint())  # Adjust icon size to button size
        dataTipsButton.setToolTip("Data tips")
        dataTipsButton.setFixedSize(38, 38)
        videoEditingIcons.addWidget(dataTipsButton)

        # Add Draw reference area Icon 
        drawReferenceAreaIcon = QPushButton()
        drawReferenceAreaIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "roi_sq.png")))
        drawReferenceAreaIcon.setIconSize(drawReferenceAreaIcon.sizeHint())  # Adjust icon size to button size
        drawReferenceAreaIcon.setToolTip("Draw reference area")
        drawReferenceAreaIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(drawReferenceAreaIcon)

        # Add Height profile over time Icon 
        heightProfileOverTimeIcon = QPushButton()
        heightProfileOverTimeIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "ZProfile.png")))
        heightProfileOverTimeIcon.setIconSize(heightProfileOverTimeIcon.sizeHint())  # Adjust icon size to button size
        heightProfileOverTimeIcon.setToolTip("Height profile over time")
        heightProfileOverTimeIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(heightProfileOverTimeIcon)

        # Add Line profile Icon 
        lineProfileIcon = QPushButton()
        lineProfileIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "line.png")))
        lineProfileIcon.setIconSize(lineProfileIcon.sizeHint())  # Adjust icon size to button size
        lineProfileIcon.setToolTip("Line profile")
        lineProfileIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(lineProfileIcon)

        # Add Zoom Icon 
        zoomIcon = QPushButton()
        zoomIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "zoomin.png")))
        zoomIcon.setIconSize(zoomIcon.sizeHint())  # Adjust icon size to button size
        zoomIcon.setToolTip("Zoom")
        zoomIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(zoomIcon)

        # There seems to be a very small gap in the NanoLocz program between these widgets
        # Not sure if intentional
        videoEditingIcons.addSpacing(10)

        # Add Crop Icon 
        cropIcon = QPushButton()
        cropIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "crop.png")))
        cropIcon.setIconSize(cropIcon.sizeHint())  # Adjust icon size to button size
        cropIcon.setToolTip("Crop")
        cropIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(cropIcon)

        # Add Kymograph from line profile Icon
        kymographIcon = QPushButton()
        kymographIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "kymo.png")))
        kymographIcon.setIconSize(kymographIcon.sizeHint())  # Adjust icon size to button size
        kymographIcon.setToolTip("Kymograph from line profile")
        kymographIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(kymographIcon)

        # Add Image montage Icon
        imageMontageIcon = QPushButton()
        imageMontageIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "montage.png")))
        imageMontageIcon.setIconSize(imageMontageIcon.sizeHint())  # Adjust icon size to button size
        imageMontageIcon.setToolTip("Image montage")
        imageMontageIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(imageMontageIcon)

        # Add View data Icon
        viewDataIcon = QPushButton()
        viewDataIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "plotter.png")))
        viewDataIcon.setIconSize(viewDataIcon.sizeHint())  # Adjust icon size to button size
        viewDataIcon.setToolTip("View data")
        viewDataIcon.setFixedSize(38, 38)
        videoEditingIcons.addWidget(viewDataIcon)

        # Add stretch to push all widgets to LHS
        videoEditingIcons.addStretch(1)

        # Create a container widget and set the layout
        videoEditingWidget = QWidget()
        videoEditingWidget.setLayout(videoEditingIcons)

        return videoEditingWidget


    def buildVideoDropdownWidgets(self) -> QWidget:
        # Create a QHBoxLayout to contain the dropdowns
        dropdownLayout = QHBoxLayout()

        # Change preview dropdown
        previewDropdown = QComboBox()
        previewDropdown.addItems(["Target", "Preview"])
        previewDropdown.setFixedSize(previewDropdown.sizeHint())
        dropdownLayout.addWidget(previewDropdown)

        # Chane colour scale dropdown
        # TODO: add more if need more
        colourScaleDropdown = QComboBox()
        colourScaleDropdown.addItems(["AFM brown", "AFM dark gold", "AFD gold", "Fire", "Rainbow"])
        colourScaleDropdown.setFixedSize(colourScaleDropdown.sizeHint())
        dropdownLayout.addWidget(colourScaleDropdown)

        # Change view modes dropdown
        viewModesDropdown = QComboBox()
        viewModesDropdown.addItems(["2D surface", "3D surface", "Co-ordinates"])
        viewModesDropdown.setFixedSize(viewModesDropdown.sizeHint())
        dropdownLayout.addWidget(viewModesDropdown)

        # Switch view dropdown
        switchViewDropdown = QComboBox()
        switchViewDropdown.addItems(["None", "Mask", "Line Profile", "Detections", "Localisations"])
        switchViewDropdown.setFixedSize(switchViewDropdown.sizeHint())
        dropdownLayout.addWidget(switchViewDropdown)

        # Change view modes dropdown
        rawOrInterpolatedDropdown = QComboBox()
        rawOrInterpolatedDropdown.addItems(["Original", "Interpolated"])
        rawOrInterpolatedDropdown.setFixedSize(rawOrInterpolatedDropdown.sizeHint())
        dropdownLayout.addWidget(rawOrInterpolatedDropdown)

        # Add spacing
        dropdownLayout.addSpacing(20)

        # Add last dropdown (it seems to just be "Off", but edited later once video is processed)
        # TODO: investigate the rest of the items that are meant to be in here
        dropdown5 = QComboBox()
        dropdown5.addItems(["Off"])
        dropdown5.setFixedSize(dropdown5.sizeHint())
        dropdownLayout.addWidget(dropdown5)

        # Push all dropdowns to the LHS
        dropdownLayout.addStretch(1)

        # Create a container widget and set the layout
        dropdownWidget = QWidget()
        dropdownWidget.setLayout(dropdownLayout)

        return dropdownWidget

    def buildVideoPlayerWidgets(self) -> QWidget:
        # Set up layout to store image and video player
        mediaLayout = QVBoxLayout()

        # Adding the Icon to a QHBoxLayout to push the button the screenshot button to the RHS
        iconLayout = QHBoxLayout()
        iconLayout.addStretch(1)

        # Add the video player screenshot Icon
        screenshootIcon = QPushButton()
        screenshootIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pop.png")))
        screenshootIcon.setIconSize(screenshootIcon.sizeHint())
        screenshootIcon.setToolTip("Screenshot video")
        screenshootIcon.setFixedSize(16, 16)
        iconLayout.addWidget(screenshootIcon)

        # Add result to the final layout
        mediaLayout.addLayout(iconLayout)

        # Add some spacing between the screenshot icon and video player
        mediaLayout.addStretch(1)

        # Set up media player to view AFM videos
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Load a sample video file (replace with your actual video path)
        videoFile = "fire.mp4"
        videoPath = QUrl.fromLocalFile(videoFile)
        # self.mediaPlayer.setMedia(videoPath)

        mediaLayout.addWidget(self.videoWidget)

        self.mediaPlayer.play()

        # Set up video control widgets
        mediaControlWidget = self.buildVideoControlWidget()
        # visualRepresentationWidget = self.buildVisualRepresetationWidget()
        # videoDepthControlWidget = self.buildVideoDepthControlWidget()
        # exportAndVideoScaleWidget = self.buildExportAndVideoScaleWidget()

        # Compose all widgets
        videoControlLayout = QHBoxLayout()
        videoControlLayout.addWidget(mediaControlWidget)
        # videoControlLayout.addWidget(visualRepresentationWidget)
        # videoControlLayout.addWidget(videoDepthControlWidget)

        mediaLayout.addLayout(videoControlLayout)
        # mediaLayout.addWidget(exportAndVideoScaleWidget)

        mediaWidget = QWidget()
        mediaWidget.setLayout(mediaLayout)

        return mediaWidget
    

    def buildVideoControlWidget(self) -> QWidget:
        # Set Layouts
        videoControlLayout = QVBoxLayout()
        videoControlButtonLayout = QHBoxLayout()
        videoEditingLayout = QHBoxLayout()

        # Set up layout for video control buttons
        # Add spin box for quantity of frames 
        # TODO: NEEDS TO BE CHANGED TO FIT THE ACTUAL NUMBER OF FRAMES BY SLOT
        frameSpinBox = QSpinBox()
        frameSpinBox.setMinimum(0)
        frameSpinBox.setMaximum(100000)
        frameSpinBox.setSingleStep(1)
        frameSpinBox.setFixedSize(frameSpinBox.sizeHint())
        videoControlButtonLayout.addWidget(frameSpinBox)

        # Add spacing to separate play, skip buttons
        videoControlButtonLayout.addStretch(1)

        # Add skip back, play, skip forward icons
        skipBackIcon = QPushButton()
        skipBackIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "start.png")))
        skipBackIcon.setIconSize(skipBackIcon.sizeHint())  # Adjust icon size to button size
        skipBackIcon.setToolTip("Skip to first frame")
        skipBackIcon.setFixedSize(skipBackIcon.sizeHint())
        videoControlButtonLayout.addWidget(skipBackIcon)

        # TODO: get this to change from play to pause and vice versa (icon is pause.png)
        playIcon = QPushButton()
        playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
        playIcon.setIconSize(playIcon.sizeHint())  # Adjust icon size to button size
        playIcon.setToolTip("Play")
        playIcon.setFixedSize(playIcon.sizeHint())
        videoControlButtonLayout.addWidget(playIcon)

        skipForwardIcon = QPushButton()
        skipForwardIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "end.png")))
        skipForwardIcon.setIconSize(skipForwardIcon.sizeHint())  # Adjust icon size to button size
        skipForwardIcon.setToolTip("Skip to last frame")
        skipForwardIcon.setFixedSize(skipForwardIcon.sizeHint())
        videoControlButtonLayout.addWidget(skipForwardIcon)

        # Add spacing
        videoControlButtonLayout.addStretch(1)

        # Add FPS text box
        fpsLabel = QLabel("Playback speed (FPS):")
        fpsTextBox = QLineEdit()
        fpsTextBox.setValidator(QIntValidator())
        videoControlButtonLayout.addWidget(fpsLabel)
        videoControlButtonLayout.addWidget(fpsTextBox)

        videoControlLayout.addLayout(videoControlButtonLayout)

        # Add video slider
        videoSeekSlider = QSlider(Qt.Orientation.Horizontal)
        videoSeekSlider.setRange(0, 100)
        # seekSlider.sliderMoved.connect(self.set_position)
        videoControlLayout.addWidget(videoSeekSlider)

        # Add video align and delete frames widgets
        videoAlignButton = QPushButton("Align video")
        videoAlignButton.setIconSize(videoAlignButton.sizeHint())
        videoAlignButton.setToolTip("Align video frames")
        videoAlignButton.setFixedSize(videoAlignButton.sizeHint())
        videoEditingLayout.addWidget(videoAlignButton)

        videoEditingLayout.addStretch(1)

        # Delete frames consists of a label, text box and icon
        deleteFramesLabel = QLabel("Delete frames:")
        deleteFramesTextBox = QLineEdit()
        deleteFramesTextBox.setValidator(RangeValidator())

        # Add Delete frames icon
        deleteFramesButton = QPushButton()
        deleteFramesButton.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "bin.png")))
        deleteFramesButton.setIconSize(deleteFramesButton.sizeHint())  # Adjust icon size to button size
        deleteFramesButton.setToolTip("Delete frames")
        deleteFramesButton.setFixedSize(deleteFramesButton.sizeHint())

        videoEditingLayout.addWidget(deleteFramesLabel)
        videoEditingLayout.addWidget(deleteFramesTextBox)
        videoEditingLayout.addWidget(deleteFramesButton)

        videoControlLayout.addLayout(videoEditingLayout)

        # Set final widget and return
        videoControlWidget = QWidget()
        videoControlWidget.setLayout(videoControlLayout)

        return videoControlWidget

        
    def buildVisualRepresetationWidget(self) -> QWidget:
        pass

    def buildVideoDepthControlWidget(self) -> QWidget:
        pass

    def buildExportAndVideoScaleWidget(self) -> QWidget:
        pass



    def buildVideoAndParticleControlWidgets(self) -> QWidget:
        pass

# Range validator for the "delete frames" input (attached to the video controls widget)
class RangeValidator(QValidator):
    def validate(self, input_str, pos):
        # Empty input is considered intermediate state (not invalid)
        if not input_str:
            return (QValidator.State.Intermediate, input_str, pos)

        # Regular expression to match a single number or a range like "10-20"
        range_pattern = re.compile(r'^\d+(-\d+)?$')
        
        if range_pattern.match(input_str):
            return (QValidator.State.Acceptable, input_str, pos)
        else:
            return (QValidator.State.Invalid, input_str, pos)

    def fixup(self, input_str):
        # Optionally, implement any automatic fixes for invalid input
        return input_str



# TODO: remove once finished
if __name__ == '__main__':
    app = QApplication(sys.argv)
    lhs_widgets = RHSWidgets()
    lhs_widgets.show()
    sys.exit(app.exec())
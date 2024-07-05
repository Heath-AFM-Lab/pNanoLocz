import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QCheckBox, QComboBox, 
    QSpinBox, QLabel, QLineEdit, QSlider, QDoubleSpinBox
)
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QIcon, QIntValidator
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtWidgets import QSizePolicy
from constants import PATH_TO_ICON_DIRECTORY

class VideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoPlayerWidgets()

    def buildVideoPlayerWidgets(self):
        # Set up video player layout 
        self.mediaLayout = QVBoxLayout()

        self.iconLayout = QHBoxLayout()
        self.iconLayout.addStretch(1)

        # Add screenshot icon
        self.screenshotIcon = QPushButton()
        self.screenshotIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pop.png")))
        self.screenshotIcon.setIconSize(self.screenshotIcon.sizeHint())
        self.screenshotIcon.setToolTip("Screenshot video")
        self.screenshotIcon.setFixedSize(16, 16)
        self.iconLayout.addWidget(self.screenshotIcon)

        # Set up video player widget
        # TODO: convert video player widget to vispy widget
        self.mediaLayout.addLayout(self.iconLayout)
        self.mediaLayout.addStretch(1)

        self.videoPlayerContainer = QWidget()
        self.videoPlayerContainer.setFixedSize(640, 480)

        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget()
        self.videoWidget.setMinimumSize(self.videoPlayerContainer.size())
        self.videoWidget.setMaximumSize(self.videoPlayerContainer.size())
        self.videoWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # TODO: Eliminate this video
        videoFile = "UI_Components/RHS_Components/fire.mp4"
        videoPath = QUrl.fromLocalFile(videoFile)
        self.mediaPlayer.setSource(videoPath)

        self.mediaLayout.addWidget(self.videoWidget)
        self.mediaPlayer.play()

        # Initialise the rest of the widgets
        self.videoControlWidget = self.VideoControlWidget()
        self.visualRepresentationWidget = self.VisualRepresentationWidget()
        self.videoDepthControlWidget = self.VideoDepthControlWidget()
        self.exportAndVideoScaleWidget = self.ExportAndVideoScaleWidget()

        # Connect singlas to slots (video player done for now)
        self.videoControlWidget.playClicked.connect(self.playPauseVideo)
        self.videoControlWidget.skipBackClicked.connect(self.skipBackward)
        self.videoControlWidget.skipForwardClicked.connect(self.skipForward)
        self.videoControlWidget.fpsChanged.connect(self.changePlaybackRate)
        self.videoControlWidget.specificVideoFrameGiven.connect(self.goToFrameNo)
        self.videoControlWidget.videoSeekSlider.valueChanged.connect(self.setVideoPosition)
        self.mediaPlayer.positionChanged.connect(self.updateSliderPosition)
        self.mediaPlayer.durationChanged.connect(self.updateSliderRange)

        # Compose all widgets
        videoControlLayout = QHBoxLayout()
        videoControlLayout.addWidget(self.videoControlWidget)
        videoControlLayout.addWidget(self.visualRepresentationWidget)
        videoControlLayout.addStretch(1)
        videoControlLayout.addWidget(self.videoDepthControlWidget)

        self.mediaLayout.addLayout(videoControlLayout)
        self.mediaLayout.addWidget(self.exportAndVideoScaleWidget)

        self.setLayout(self.mediaLayout)

    def playPauseVideo(self):
        if self.mediaPlayer.isPlaying():
            self.mediaPlayer.pause()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pause.png")))
            self.videoControlWidget.playIcon.setToolTip("Pause")
        else:
            self.mediaPlayer.play()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
            self.videoControlWidget.playIcon.setToolTip("Play")

    def skipForward(self):
        new_position = self.mediaPlayer.position() + 10000  # 10 seconds forward
        self.mediaPlayer.setPosition(new_position)

    def skipBackward(self):
        new_position = self.mediaPlayer.position() - 10000  # 10 seconds forward
        self.mediaPlayer.setPosition(new_position)

    # TODO: Chnage all FPS stuff to suit the vispy module
    def changePlaybackRate(self, fps):
        self.mediaPlayer.setPlaybackRate(fps / 30.0)  # Adjusting the rate assuming 30 FPS as normal speed

    def goToFrameNo(self, frameNo):
        fps = 30  # Assuming 30 FPS
        position = frameNo * 1000 / fps  # Convert frame number to milliseconds
        self.mediaPlayer.setPosition(int(position))

    def setVideoPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def updateSliderPosition(self, position):
        self.videoControlWidget.videoSeekSlider.blockSignals(True)
        self.videoControlWidget.videoSeekSlider.setValue(position)
        self.videoControlWidget.videoSeekSlider.blockSignals(False)

    def updateSliderRange(self, duration):
        self.videoControlWidget.videoSeekSlider.setRange(0, duration)



    class VideoControlWidget(QWidget):
        specificVideoFrameGiven = pyqtSignal(int)
        playClicked = pyqtSignal()
        skipBackClicked = pyqtSignal()
        skipForwardClicked = pyqtSignal()
        fpsChanged = pyqtSignal(int)

        def __init__(self):
            super().__init__()
            self.setupUi()

        def setupUi(self):
            self.layout = QVBoxLayout()

            # Video control buttons
            self.buttonLayout = QHBoxLayout()

            self.frameSpinBox = QSpinBox()
            self.frameSpinBox.setMinimum(0)
            self.frameSpinBox.setMaximum(100000)
            self.frameSpinBox.setSingleStep(1)
            self.frameSpinBox.valueChanged.connect(lambda frameNo: self.specificVideoFrameGiven.emit(int(frameNo)))
            self.buttonLayout.addWidget(self.frameSpinBox)

            self.skipBackIcon = QPushButton()
            self.skipBackIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "start.png")))
            self.skipBackIcon.setIconSize(self.skipBackIcon.sizeHint())
            self.skipBackIcon.setToolTip("Skip to first frame")
            self.skipBackIcon.clicked.connect(self.skipBackClicked.emit)
            self.buttonLayout.addWidget(self.skipBackIcon)

            self.playIcon = QPushButton()
            self.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
            self.playIcon.setIconSize(self.playIcon.sizeHint())
            self.playIcon.setToolTip("Play")
            self.playIcon.clicked.connect(self.playClicked.emit)
            self.buttonLayout.addWidget(self.playIcon)

            self.skipForwardIcon = QPushButton()
            self.skipForwardIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "end.png")))
            self.skipForwardIcon.setIconSize(self.skipForwardIcon.sizeHint())
            self.skipForwardIcon.setToolTip("Skip to last frame")
            self.skipForwardIcon.clicked.connect(self.skipForwardClicked.emit)
            self.buttonLayout.addWidget(self.skipForwardIcon)

            self.fpsLabel = QLabel("Playback speed (FPS):")
            self.fpsTextBox = QLineEdit()
            self.fpsTextBox.setValidator(QIntValidator())
            self.fpsTextBox.textChanged.connect(lambda text: self.fpsChanged.emit(int(text)) if text.isdigit() else None)
            self.buttonLayout.addWidget(self.fpsLabel)
            self.buttonLayout.addWidget(self.fpsTextBox)

            self.layout.addLayout(self.buttonLayout)

            # Video slider
            self.videoSeekSlider = QSlider(Qt.Orientation.Horizontal)
            self.videoSeekSlider.setRange(0, 100)
            self.layout.addWidget(self.videoSeekSlider)

            self.setLayout(self.layout)

    class VisualRepresentationWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setupUi()

        def setupUi(self):
            self.layout = QVBoxLayout()

            self.scaleBarCheckbox = QCheckBox("Scale bar")
            self.scaleBarCheckbox.setToolTip("Enable or disable Scale bar")
            self.layout.addWidget(self.scaleBarCheckbox)
        
            self.zScaleCheckbox = QCheckBox("Z-scale")
            self.zScaleCheckbox.setToolTip("Enable or disable Z-scale")
            self.layout.addWidget(self.zScaleCheckbox)

            self.autosaveCheckbox = QCheckBox("Autosave")
            self.autosaveCheckbox.setToolTip("Enable or disable autosave")
            self.layout.addWidget(self.autosaveCheckbox)

            self.layout.addStretch(1)

            self.setLayout(self.layout)

    class VideoDepthControlWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setupUi()

        def setupUi(self):
            self.layout = QVBoxLayout()

            self.depthTypeDropdown = QComboBox()
            self.depthTypeDropdown.addItems(["Min Max", "Histogram", "Excl. outliers", "Manual"])
            self.depthTypeDropdown.setFixedSize(self.depthTypeDropdown.sizeHint())
            self.layout.addWidget(self.depthTypeDropdown)

            self.buttonLayout = QHBoxLayout()
            self.autoButton = QPushButton("Auto")
            self.buttonLayout.addWidget(self.autoButton)

            self.holdButton = QPushButton("Hold")
            self.buttonLayout.addWidget(self.holdButton)

            self.layout.addLayout(self.buttonLayout)

            self.minSpinLayout = QHBoxLayout()
            self.minSpinBox = QDoubleSpinBox()
            self.minSpinBox.setMinimum(0)
            self.minSpinBox.setMaximum(10000)
            self.minSpinBox.setSingleStep(0.01)
            self.minSpinBox.setFixedSize(self.minSpinBox.sizeHint())
            self.minSpinLabel = QLabel("Min height:")
            self.minSpinLayout.addWidget(self.minSpinLabel)
            self.minSpinLayout.addWidget(self.minSpinBox)

            self.maxSpinLayout = QHBoxLayout()
            self.maxSpinBox = QDoubleSpinBox()
            self.maxSpinBox.setMinimum(0)
            self.maxSpinBox.setMaximum(10000)
            self.maxSpinBox.setSingleStep(0.01)
            self.maxSpinBox.setFixedSize(self.maxSpinBox.sizeHint())
            self.maxSpinLabel = QLabel("Max height:")
            self.maxSpinLayout.addWidget(self.maxSpinLabel)
            self.maxSpinLayout.addWidget(self.maxSpinBox)

            self.layout.addLayout(self.minSpinLayout)
            self.layout.addLayout(self.maxSpinLayout)

            self.setLayout(self.layout)

    class ExportAndVideoScaleWidget(QWidget):
        def __init__(self):
            super().__init__()
            self.setupUi()

        def setupUi(self):
            self.layout = QHBoxLayout()

            self.exportButton = QPushButton("Export")
            self.exportButton.setToolTip("Export data plot")
            self.exportButton.setFixedSize(self.exportButton.sizeHint())
            self.layout.addWidget(self.exportButton)

            self.exportTargetPlotDropdown = QComboBox()
            self.exportTargetPlotDropdown.addItems(["Plot 1", "Plot 2", "Data"])
            self.exportTargetPlotDropdown.setFixedSize(self.exportTargetPlotDropdown.sizeHint())
            self.layout.addWidget(self.exportTargetPlotDropdown)

            self.fileFormatDropdown = QComboBox()
            self.fileFormatDropdown.addItems([".tiff", ".gif", ".avi", ".png", ".jpeg", ".pdf", ".txt", ".csv", ".xlsx", "MATLAB workspace"])
            self.fileFormatDropdown.setFixedSize(self.fileFormatDropdown.sizeHint())
            self.layout.addWidget(self.fileFormatDropdown)

            self.layout.addStretch(1)

            self.scaleVideoDropdown = QComboBox()
            self.scaleVideoDropdown.addItems(["Original", "1 to 1"])
            self.scaleVideoDropdown.setFixedSize(self.scaleVideoDropdown.sizeHint())
            self.layout.addWidget(self.scaleVideoDropdown)

            self.force1To1Button = QPushButton("Force 1:1")
            self.force1To1Button.setToolTip("Force image and video scaling to 1:1")
            self.force1To1Button.setFixedSize(self.force1To1Button.sizeHint())
            self.layout.addWidget(self.force1To1Button)

            self.setLayout(self.layout)

if __name__ == "__main__":
    # TODO: remove once format correction is complete
    ICON_DIRECTORY = "../../../assets/icons"
    # Path to icon directory
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    videoPlayerWidget = VideoPlayerWidget()
    videoPlayerWidget.show()
    sys.exit(app.exec())

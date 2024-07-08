import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QSizePolicy
from UI_components.RHS_Components.Video_Player_Components import VideoControlWidget, VideoDepthControlWidget, VisualRepresentationWidget, ExportAndVideoScaleWidget
from constants import PATH_TO_ICON_DIRECTORY

class VideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoPlayerWidgets()

    def buildVideoPlayerWidgets(self):
        # Set up video player layout 
        self.mediaLayout = QVBoxLayout()
        # Remove margins and spacing
        self.mediaLayout.setContentsMargins(0, 0, 0, 0)
        self.mediaLayout.setSpacing(0)

        self.iconLayout = QHBoxLayout()
        self.iconLayout.addStretch(1)

        # Add screenshot icon
        self.screenshotIcon = QPushButton()
        self.screenshotIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pop.png")))
        self.screenshotIcon.setIconSize(self.screenshotIcon.sizeHint())
        self.screenshotIcon.setToolTip("Screenshot video")
        self.screenshotIcon.setFixedSize(16, 16)
        self.iconLayout.addWidget(self.screenshotIcon)
        self.mediaLayout.addLayout(self.iconLayout)

        # Set up video player widget
        # TODO: convert video player widget to vispy widget
        self.videoPlayerContainer = QWidget()
        # self.videoPlayerContainer.setFixedSize(640, 480)

        videoPlayerSizePolicy = QSizePolicy()
        videoPlayerSizePolicy.setHeightForWidth(True)
        videoPlayerSizePolicy.setWidthForHeight(True)
        videoPlayerSizePolicy.setHorizontalPolicy(QSizePolicy.Policy.Expanding)
        videoPlayerSizePolicy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
        self.videoPlayerContainer.setSizePolicy(videoPlayerSizePolicy)
        
        
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget = QVideoWidget()
        # self.videoWidget.setMinimumSize(self.videoPlayerContainer.size())
        # self.videoWidget.setMaximumSize(self.videoPlayerContainer.size())
        # self.videoWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.videoWidget.setSizePolicy(videoPlayerSizePolicy)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # TODO: Eliminate this video
        videoFile = "UI_Components/RHS_Components/fire.mp4"
        videoPath = QUrl.fromLocalFile(videoFile)
        self.mediaPlayer.setSource(videoPath)

        self.mediaLayout.addWidget(self.videoWidget)
        self.mediaPlayer.play()

        # self.videoPlayerContainer.addWidget(self.video)

        # Initialise the rest of the widgets
        self.videoControlWidget = VideoControlWidget()
        self.visualRepresentationWidget = VisualRepresentationWidget()
        self.videoDepthControlWidget = VideoDepthControlWidget()
        self.exportAndVideoScaleWidget = ExportAndVideoScaleWidget()

        # Connect signals to slots (video player done for now)
        self.videoControlWidget.playClicked.connect(self.playPauseVideo)
        self.videoControlWidget.skipBackClicked.connect(self.skipBackward)
        self.videoControlWidget.skipForwardClicked.connect(self.skipForward)
        self.videoControlWidget.fpsChanged.connect(self.changePlaybackRate)
        self.videoControlWidget.specificVideoFrameGiven.connect(self.goToFrameNo)
        self.videoControlWidget.videoSeekSlider.valueChanged.connect(self.setVideoPosition)
        self.mediaPlayer.positionChanged.connect(self.updateSliderPosition)
        self.mediaPlayer.durationChanged.connect(self.updateSliderRange)

        # Fix all sizes
        self.videoControlWidget.setFixedSize(self.videoControlWidget.sizeHint())
        self.visualRepresentationWidget.setFixedSize(self.visualRepresentationWidget.sizeHint())
        self.videoDepthControlWidget.setFixedSize(self.videoDepthControlWidget.sizeHint())
        self.exportAndVideoScaleWidget.setFixedSize(self.exportAndVideoScaleWidget.sizeHint())

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

if __name__ == "__main__":
    # TODO: remove once format correction is complete
    ICON_DIRECTORY = "../../../assets/icons"
    # Path to icon directory
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    videoPlayerWidget = VideoPlayerWidget()
    videoPlayerWidget.show()
    sys.exit(app.exec())

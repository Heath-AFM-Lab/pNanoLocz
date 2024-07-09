import sys
import os
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from vispy import app, scene
from UI_components.RHS_Components.Video_Player_Components import VideoControlWidget, VideoDepthControlWidget, VisualRepresentationWidget, ExportAndVideoScaleWidget
from constants import PATH_TO_ICON_DIRECTORY

class VideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.buildVideoPlayerWidgets()
        self.loadFrames()
        self.frame_index = 0

        # Timer to update the frames
        self.timer = app.Timer('auto', connect=self.update_frame, start=True)

    def buildVideoPlayerWidgets(self):
        # Set up video player layout 
        self.mediaLayout = QVBoxLayout()
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

        # Set up Vispy canvas
        self.videoPlayerContainer = QWidget()
        self.vispyCanvas = scene.SceneCanvas(keys='interactive', parent=self.videoPlayerContainer)
        self.mediaLayout.addWidget(self.vispyCanvas.native)

        self.view = self.vispyCanvas.central_widget.add_view()
        self.view.camera = 'panzoom'

        self.setLayout(self.mediaLayout)

        # Initialize the rest of the widgets
        self.videoControlWidget = VideoControlWidget()
        self.visualRepresentationWidget = VisualRepresentationWidget()
        self.videoDepthControlWidget = VideoDepthControlWidget()
        self.exportAndVideoScaleWidget = ExportAndVideoScaleWidget()

        # Connect signals to slots
        self.videoControlWidget.playClicked.connect(self.playPauseVideo)
        self.videoControlWidget.skipBackClicked.connect(self.skipBackward)
        self.videoControlWidget.skipForwardClicked.connect(self.skipForward)
        self.videoControlWidget.fpsChanged.connect(self.changePlaybackRate)
        self.videoControlWidget.specificVideoFrameGiven.connect(self.goToFrameNo)
        self.videoControlWidget.videoSeekSlider.valueChanged.connect(self.setVideoPosition)
        self.videoControlWidget.videoSeekSlider.sliderReleased.connect(self.sliderReleased)

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

    def loadFrames(self):
        # Example: Generate random frames
        self.frames = [np.random.randint(0, 256, (600, 800, 3), dtype=np.uint8) for _ in range(100)]
        self.image_visual = scene.visuals.Image(self.frames[0], parent=self.view.scene, interpolation='nearest')

    def update_frame(self, event):
        # Update the image visual with the new frame
        self.image_visual.set_data(self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.vispyCanvas.update()

        # Update the slider position
        self.videoControlWidget.videoSeekSlider.blockSignals(True)
        self.videoControlWidget.videoSeekSlider.setValue(self.frame_index)
        self.videoControlWidget.videoSeekSlider.blockSignals(False)

    def playPauseVideo(self):
        if self.timer.running:
            self.timer.stop()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "play.png")))
            self.videoControlWidget.playIcon.setToolTip("Play")
        else:
            self.timer.start()
            self.videoControlWidget.playIcon.setIcon(QIcon(os.path.join(PATH_TO_ICON_DIRECTORY, "pause.png")))
            self.videoControlWidget.playIcon.setToolTip("Pause")

    def skipForward(self):
        self.frame_index = min(self.frame_index + 30, len(self.frames) - 1)  # Skip 30 frames forward

    def skipBackward(self):
        self.frame_index = max(self.frame_index - 30, 0)  # Skip 30 frames backward

    def changePlaybackRate(self, fps):
        self.timer.interval = 1.0 / fps

    def goToFrameNo(self, frameNo):
        self.frame_index = frameNo % len(self.frames)

    def setVideoPosition(self, position):
        self.frame_index = position

    def sliderReleased(self):
        self.update_frame(None)

if __name__ == "__main__":
    # Path to icon directory
    ICON_DIRECTORY = "../../../assets/icons"
    PATH_TO_ICON_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), ICON_DIRECTORY))
    app = QApplication(sys.argv)
    videoPlayerWidget = VideoPlayerWidget()
    videoPlayerWidget.show()
    sys.exit(app.exec())
